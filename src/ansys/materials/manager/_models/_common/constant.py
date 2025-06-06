# Copyright (C) 2022 - 2025 ANSYS, Inc. and/or its affiliates.
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

from typing import Any, List, Tuple

from ansys.materials.manager._models._common._base import _BaseModel, _FluentCore, _MapdlCore
from ansys.materials.manager._models._common._exceptions import ModelValidationException
from ansys.materials.manager._models._common._packages import SupportedPackage
from ansys.materials.manager._models._fluent.simple_properties import (
    property_codes as fluent_property_codes,
)
from ansys.materials.manager._models._mapdl.simple_properties import (
    property_codes as mapdl_property_codes,
)

TYPE_CHECKING = False
if TYPE_CHECKING:
    from ansys.materials.manager.material import Material  # noqa: F401


class Constant(_BaseModel):
    """Represents a constant property value in a solver."""

    applicable_packages: SupportedPackage.MAPDL | SupportedPackage.FLUENT
    _name: str
    _value: float

    def __init__(self, name: str, value: float) -> None:
        """
        Create a constant property value.

        This property is created in the default unit system of the solver. Ensure
        that you provide the value in the correct units.

        Parameters
        ----------
        name: str
            Name of the property to model as a constant.
        value: float
            Value of the constant property.
        """
        self._name = name
        self._value = value

    @property
    def name(self) -> str:
        """Name of the quantity modeled by the constant."""
        return self._name

    @property
    def value(self) -> float:
        """Constant value of the quantity."""
        return self._value

    @value.setter
    def value(self, value: float) -> None:
        self._value = value

    def write_model(self, material: "Material", pyansys_session: Any) -> None:
        """
        Write this model to MAPDL.

        This method should make some effort to validate the model state before writing.

        Parameters
        ----------
        material: Material
            Material object to associate with this model.
        pyansys_session: Any
            Configured instance of the PyAnsys session.
        """
        is_ok, issues = self.validate_model()
        if not is_ok:
            raise ModelValidationException("\n".join(issues))

        if isinstance(pyansys_session, _MapdlCore):
            self._write_mapdl(pyansys_session, material)
        elif isinstance(pyansys_session, _FluentCore):
            self._write_fluent(pyansys_session, material)
        else:
            raise TypeError(
                "This model is only supported by MAPDL and Fluent. Ensure that you have the correct"
                "type of the PyAnsys session."
            )

    def _write_mapdl(self, mapdl: "_MapdlCore", material: "Material") -> None:
        mapdl_property_code = mapdl_property_codes[self._name.lower()]
        mapdl.mp(mapdl_property_code, material.material_id, self._value)

    def _write_fluent(self, fluent: "_FluentCore", material: "Material") -> None:
        try:
            fluent_property_code = fluent_property_codes[self._name.lower()]
            property_state = {fluent_property_code: {"option": "constant", "value": self._value}}
            fluent.settings.setup.materials.fluid[material.name] = property_state
        except (RuntimeError, KeyError):
            pass

    def validate_model(self) -> "Tuple[bool, List[str]]":
        """
        Perform pre-flight validation of the model setup.

        Returns
        -------
        Tuple
            First element is Boolean. ``True`` if validation is successful. If ``False``,
            the second element contains a list of strings with more information.
        """
        failures = []
        is_ok = True

        if self._name is None or self._name == "":
            failures.append("Invalid property name")
            is_ok = False
        if self._value is None:
            failures.append("Value cannot be None")
            is_ok = False
        return is_ok, failures
