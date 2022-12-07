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

        This property will be created in the default unit system of the solver. Ensure
        you provide the value in the correct units.

        Parameters
        ----------
        name: str
            The name of the property to be modelled as a constant.
        value: float
            The value of the constant property.
        """
        self._name = name
        self._value = value

    @property
    def name(self) -> str:
        """Get the name of the quantity modelled by this constant."""
        return self._name

    @property
    def value(self) -> float:
        """Get the constant value of this quantity."""
        return self._value

    @value.setter
    def value(self, value: float) -> None:
        self._value = value

    def write_model(self, material: "Material", pyansys_session: Any) -> None:
        """
        Write this model to MAPDL.

        Should make some effort to validate the model state before writing.

        Parameters
        ----------
        pyansys_session: Any
            Configured instance of PyAnsys session.

        material: Material
            Material object with which this model will be associated.
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
                "This model is only supported by MAPDL and Fluent, ensure you have the correct"
                "type of `pyansys_session`."
            )

    def _write_mapdl(self, mapdl: "_MapdlCore", material: "Material") -> None:
        mapdl_property_code = mapdl_property_codes[self._name.lower()]
        mapdl.mp(mapdl_property_code, material.material_id, self._value)

    def _write_fluent(self, fluent: "_FluentCore", material: "Material") -> None:
        try:
            fluent_property_code = fluent_property_codes[self._name.lower()]
            if isinstance(self._value, str):
                propState = {fluent_property_code: {"option": self._value}}
            else:
                propState = {fluent_property_code: {"option": "constant", "value": self._value}}
            fluent.setup.materials.fluid[material.name] = propState
        except (RuntimeError, KeyError):
            pass

    def validate_model(self) -> "Tuple[bool, List[str]]":
        """
        Perform pre-flight validation of model setup.

        Returns
        -------
        Tuple
            First element is boolean, true if validation is successful. If false then the second
            element will contain a list of strings with more information.
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