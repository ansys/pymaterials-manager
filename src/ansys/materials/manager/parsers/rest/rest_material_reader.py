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

import json
import logging
import warnings

from ansys.materials.manager.models._common.material_model import MaterialModel
from ansys.materials.manager.models.material import Material
from ansys.materials.manager.parsers._common import ModelInfo
from ansys.materials.manager.parsers.rest._exceptions import GrantaMIError
from ansys.materials.manager.parsers.rest._rest_model_map import (
    MATERIAL_MODEL_MAP,
    MODEL_ID_INFO_MAP,
    MODEL_ID_MAP,
)
from ansys.materials.manager.parsers.rest._rest_reader import (
    get_dimensionality,
    map_json_to_model_attributes,
)

_logger = logging.getLogger(__name__)

"""
Granta MI model IDs used to represent metadata.

These have no MaterialModel counterpart and are intentionally skipped without a warning.
"""
_METADATA_ONLY_MODEL_IDS: frozenset[str] = frozenset(
    {
        "classification",
        "description",
        "rendering",
    }
)


def _pick_by_dimensionality(
    model_class: type,
    entries: list[tuple[str, dict, "ModelInfo | None"]],
) -> tuple[str, dict, "ModelInfo | None"] | None:
    """
    Select the highest-dimensionality entry from a group of candidates for the same model class.

    When only one entry is present it is returned directly.  When multiple entries exist, the one
    with the most independent (free-parameter) columns wins.  If two entries tie on dimensionality
    a warning is logged and ``None`` is returned (no model is populated to avoid ambiguity).

    Parameters
    ----------
    model_class : type
        The :class:`~.MaterialModel` subclass shared by all entries (used for log messages).
    entries : list[tuple[str, dict, ModelInfo | None]]
        Each item is ``(model_id, model_data, model_info)`` for a candidate section.

    Returns
    -------
    tuple[str, dict, ModelInfo | None] | None
        The selected entry, or ``None`` when there is a tie or no entries.
    """
    if not entries:
        return None
    if len(entries) == 1:
        return entries[0]

    scored = [(get_dimensionality(data), model_id, data, info) for model_id, data, info in entries]
    max_dim = max(s[0] for s in scored)
    winners = [s for s in scored if s[0] == max_dim]

    if len(winners) > 1:
        tied_ids = [s[1] for s in winners]
        _logger.warning(
            "Multiple model sections for %s have equal dimensionality (%d): %s. "
            "Skipping all to avoid ambiguity.",
            model_class.__name__,
            max_dim,
            tied_ids,
        )
        return None

    winning_dim, winning_id, winning_data, winning_info = winners[0]
    losers = [s[1] for s in scored if s[0] < winning_dim]
    _logger.debug(
        "Selected modelId='%s' (dimensionality=%d) over %s for %s.",
        winning_id,
        winning_dim,
        losers,
        model_class.__name__,
    )
    return winning_id, winning_data, winning_info


class RestMaterialReader:
    """
    Convert a Granta MI Material Models API JSON response into a collection of Material objects.

    The dict returned by
    :meth:`~ansys.materials.manager.parsers.rest.rest_session_client.RestSessionClient.fetch_data`
    wraps the model JSON payload in an outer JSON of the form
    ``{"value": "<json-string>", "id": <int>}``m, where the ``"value"`` field is JSON-encoded.
    This envelope is unwrapped automatically by :meth:`_iter_materials`.

    Parameters
    ----------
    raw_data : dict
        Parsed JSON response from the ``…/sessions/{id}/data`` endpoint.
    """

    def __init__(self, raw_data: dict) -> None:
        """Initialize the reader with raw JSON data."""
        self._raw_data = raw_data

    def convert_materials(self) -> dict[str, Material]:
        """
        Convert the raw JSON data into :class:`~.Material` objects.

        Iterates over each material record in the response and delegates to
        :meth:`visit_material`.

        Returns
        -------
        dict[str, Material]
            Mapping of material name to the populated
            :class:`~ansys.materials.manager.models.material.Material` object.
        """
        materials: dict[str, Material] = {}
        material_index = 1

        _logger.debug("Beginning material conversion from REST response.")
        for material_data in self._iter_materials(self._raw_data):
            material = self.visit_material(material_data, material_index)
            materials[material.name] = material
            material_index += 1

        _logger.info("Converted %d material(s) from REST response.", len(materials))
        return materials

    def visit_material(self, material_data: dict, material_index: int) -> Material:
        """
        Create an individual :class:`~ansys.materials.manager.models.material.Material`.

        Parameters
        ----------
        material_data : dict
            A single Granta MI material model object.
        material_index : int
            1-based position of this material in the response, used only for log messages.

        Returns
        -------
        Material
            A populated ``Material`` object.
        """
        try:
            name = material_data["materialName"]
            material_id = material_data["materialId"]
        except KeyError as exc:
            raise GrantaMIError(
                f"Material record is missing required field {exc}. "
                "The server response may be malformed."
            ) from exc
        _logger.debug("Processing material #%d: '%s' (id=%s).", material_index, name, material_id)

        # Collect all candidates per model class so we can resolve conflicts by dimensionality.
        candidates: dict[type, list[tuple[str, dict, ModelInfo | None]]] = {}
        for model_class, model_id, model_data, model_info in self._iter_model_sections(
            material_data
        ):
            candidates.setdefault(model_class, []).append((model_id, model_data, model_info))

        models: list[MaterialModel] = []
        for model_class, entries in candidates.items():
            selected = _pick_by_dimensionality(model_class, entries)
            if selected is None:
                continue
            _, section_data, model_info = selected
            model = self.visit_material_model(model_class, section_data, model_info)
            if model is not None:
                models.append(model)

        _logger.debug("Material '%s': populated %d model(s).", name, len(models))
        return Material(name=name, material_id=material_id, models=models)

    @staticmethod
    def visit_material_model(
        model_class: type,
        model_data: dict,
        model_info: ModelInfo | None = None,
    ) -> MaterialModel | None:
        """
        Instantiate and populate a single :class:`~.MaterialModel`.

        Looks up *model_class* in :data:`~.MATERIAL_MODEL_MAP` unless a *model_info* override
        is supplied directly (used when the caller has already resolved the per-ID mapping).
        If no mapping is found, a warning is emitted and ``None`` is returned.

        Parameters
        ----------
        model_class : type
            The :class:`~.MaterialModel` subclass to instantiate.
        model_data : dict
            The model section dict from the Granta MI REST response.
        model_info : ModelInfo | None
            Optional pre-resolved :class:`~.ModelInfo`.  When ``None``, the mapping is
            looked up from :data:`~.MATERIAL_MODEL_MAP`.

        Returns
        -------
        MaterialModel | None
            A populated model instance, or ``None`` if *model_class* has no registered mapping.
        """
        if model_info is None:
            model_info = MATERIAL_MODEL_MAP.get(model_class)
        if model_info is None:
            warnings.warn(
                f"No REST mapping registered for material model "
                f"'{model_class.__name__}'. Skipping. "
                f"Add an entry to MATERIAL_MODEL_MAP in "
                f"ansys.materials.manager.parsers.rest._rest_model_map.",
                stacklevel=2,
            )
            return None

        attribute_map = map_json_to_model_attributes(model_data, model_info)
        _logger.debug(
            "Populating %s with attributes: %s.", model_class.__name__, list(attribute_map.keys())
        )
        instance = model_class()
        for attr, value in attribute_map.items():
            setattr(instance, attr, value)
        return instance

    @staticmethod
    def _iter_materials(raw_data: dict):
        r"""
        Yield individual material record dicts from the top-level response.

        The Granta MI REST API wraps the materials JSON as a string inside a ``"value"`` key
        (i.e. ``{"value": "{\"materials\":[...]}", "id": 1}``).  This method unwraps that
        envelope before iterating over the ``"materials"`` array.

        Parameters
        ----------
        raw_data : dict
            The full parsed JSON response from the ``…/sessions/{id}/data`` endpoint.

        Yields
        ------
        dict
            One material record dict per iteration.

        Warnings
        --------
        The ``raw_data`` parameter is the 'outer' response. It should contain a JSON-encoded
        string which must be parsed to yield the actual material model data.
        """
        if "value" in raw_data and isinstance(raw_data["value"], str):
            _logger.debug("Unwrapping double-encoded JSON 'value' envelope.")
            try:
                raw_data = json.loads(raw_data["value"])
            except json.JSONDecodeError as exc:
                raise GrantaMIError(
                    "The Granta MI session response contained a 'value' field that could not "
                    "be parsed as JSON. The server response may be malformed."
                ) from exc
        material_records = raw_data.get("materials", [])
        _logger.debug("Found %d material record(s) in response.", len(material_records))
        for material_data in material_records:
            yield material_data

    @staticmethod
    def _iter_model_sections(material_data: dict):
        """
        Yield ``(model_class, model_id, model_data, model_info)`` tuples for a material record.

        Dispatches on the ``"modelId"`` field of each entry in the ``"models"`` array using
        :data:`~ansys.materials.manager.parsers.rest._rest_model_map.MODEL_ID_MAP`.
        The :class:`~ansys.materials.manager.parsers._common.ModelInfo` is resolved by
        checking :data:`~.MODEL_ID_INFO_MAP` first (per-ID override, e.g. for tabular variants)
        and falling back to :data:`~.MATERIAL_MODEL_MAP` (class-level default).

        Model sections whose ``"modelId"`` is not registered are silently skipped or warned
        depending on whether they appear in :data:`~._METADATA_ONLY_MODEL_IDS`.

        Parameters
        ----------
        material_data : dict
            A single material record from the Granta MI REST response.

        Yields
        ------
        tuple[type, str, dict, ModelInfo | None]
            The resolved model class, its Granta MI model ID, its model section dict, and
            the resolved :class:`~.ModelInfo` (may be ``None`` if no mapping is registered).
        """
        for model_section in material_data.get("models", []):
            model_id = model_section.get("modelId")
            model_class = MODEL_ID_MAP.get(model_id)
            if model_class is not None:
                model_info = MODEL_ID_INFO_MAP.get(model_id) or MATERIAL_MODEL_MAP.get(model_class)
                _logger.debug("Dispatching modelId='%s' → %s.", model_id, model_class.__name__)
                yield model_class, model_id, model_section, model_info
            elif model_id in _METADATA_ONLY_MODEL_IDS:
                _logger.debug("Skipping metadata-only Granta MI modelId='%s'.", model_id)
            else:
                _logger.warning("No mapping registered for Granta MI modelId='%s'. ", model_id)
