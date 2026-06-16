# Copyright (C) 2022 - 2026 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
Helper functions for mapping Granta MI material model JSON data to material model attributes.

The Granta MI models API provides a models object which contains a list of property objects.
Each models object can contain one or more of the following properties::

    {
        "name": "<property name>",
        "symbol": "<symbol>",          # optional
        "unit": "<unit string>",       # optional
        "numericValue": <float>,       # for numeric properties
        "stringValue": "<str>",        # for string properties
        "boolValue": <bool>            # for boolean properties
    }

:func:`get_property_with_unit` understands this structure.
"""

import logging
from typing import Any, Final

from ansys.units import Quantity

from ansys.materials.manager.parsers._common import ModelInfo

_logger = logging.getLogger(__name__)

_GRANTA_MI_UNIT_MAP: Final[dict[str, str]] = {
    "kg/m^3": "kg m^-3",
    "Pa": "Pa",
    "W/m.\N{DEGREE SIGN}C": "W m^-1 K^-1",
    "J/kg.\N{DEGREE SIGN}C": "J kg^-1 K^-1",
    "strain/\N{DEGREE SIGN}C": "K^-1",
}
"""
Maps Granta MI unit strings to their ``ansys.units`` equivalents.

Entries cover all confirmed model properties returned by Granta MI.
"""


def get_property_with_unit(model_data: dict, property_name: str) -> tuple[Any, str | None]:
    """
    Extract a property value and its Granta MI unit string.

    Parameters
    ----------
    model_data : dict
        A model section dict from the REST response.
    property_name : str
        The ``"name"`` field to search for.

    Returns
    -------
    tuple[Any, str | None]
        ``(value, unit_string)`` where *unit_string* is the raw Granta MI unit
        (e.g. ``"kg/m^3"``) or ``None`` if the property has no unit or is not
        a numeric property.
    """
    for prop in model_data.get("properties", []):
        if prop.get("name") == property_name:
            numeric = prop.get("numericValue")
            if numeric is not None:
                return numeric, prop.get("unit")
            for value_key in ("stringValue", "boolValue"):
                value = prop.get(value_key)
                if value is not None:
                    return value, None
    return None, None


def _make_quantity(value: float, granta_unit: str | None) -> Quantity:
    """
    Wrap a scalar float in a :class:`~ansys.units.Quantity`.

    The Granta MI unit string is translated via :data:`_GRANTA_MI_UNIT_MAP`
    before constructing the :class:`~ansys.units.Quantity`.

    Parameters
    ----------
    value : float
        The numeric value to wrap.
    granta_unit : str | None
        The Granta MI unit string (e.g. ``"kg/m^3"``), or ``None`` for
        dimensionless quantities.

    Returns
    -------
    Quantity
        A ``Quantity`` wrapping *value*.

    Raises
    ------
    KeyError
        If *granta_unit* is not ``None`` and has no entry in :data:`_GRANTA_MI_UNIT_MAP`.
    """
    if granta_unit is None:
        mapped_unit = ""
    else:
        try:
            mapped_unit = _GRANTA_MI_UNIT_MAP[granta_unit]
        except KeyError as e:
            raise KeyError(f"No mapping available for Granta MI unit symbol {granta_unit}.") from e
    return Quantity(value=[value], units=mapped_unit)


def map_json_to_model_attributes(model_data: dict, model_info: ModelInfo) -> dict[str, Any]:
    """
    Map a JSON model object to model attribute names using a :class:`ModelInfo`.

    If *model_info* supplies a ``method_read`` callable it is called with *model_data* and
    must return ``(attribute_names, values)`` as parallel sequences.  Otherwise, the
    ``labels`` / ``attributes`` lists on *model_info* are used for a property-name lookup
    against the ``"properties"`` array in *model_data*.

    Parameters
    ----------
    model_data : dict
        The model section dict from the REST response.
    model_info : ModelInfo
        The mapping configuration from ``MATERIAL_MODEL_MAP``.

    Returns
    -------
    dict[str, Any]
        Mapping of attribute names to their values extracted from *model_data*.
    """
    if model_info.method_read is not None:
        attribute_names, values = model_info.method_read(model_data)
        return dict(zip(attribute_names, values))

    if not model_info.labels or not model_info.attributes:
        return {}

    result: dict[str, Any] = {}
    for label, attribute in zip(model_info.labels, model_info.attributes):
        value, unit = get_property_with_unit(model_data, label)
        if value is not None:
            if isinstance(value, (int, float)):
                try:
                    value = _make_quantity(value, unit)
                except KeyError:
                    _logger.warning(
                        "No unit mapping for Granta MI unit %r on property '%s'. "
                        "Skipping this property.",
                        unit,
                        label,
                    )
                    continue
            result[attribute] = value
    return result
