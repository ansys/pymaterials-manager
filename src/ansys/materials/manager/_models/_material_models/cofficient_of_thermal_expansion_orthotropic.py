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

from typing import Any, Dict, Literal

from ansys.units import Quantity
from pydantic import Field, model_validator

from ansys.materials.manager._models._common import (
    MaterialModel,
    ParameterField,
    QualifierType,
    _MapdlCore,
    validate_and_initialize_model_qualifiers,
)
from ansys.materials.manager.util.mapdl.mapdl_writer import (
    write_constant_properties,
    write_interpolation_options,
    write_table_values,
    write_temperature_reference_value,
    write_temperature_table_values,
)


class CoefficientofThermalExpansionOrthotropic(MaterialModel):
    """Represents an orthotropic coefficient of thermal expansion material model."""

    name: Literal["Coefficient of Thermal Expansion"] = Field(
        default="Coefficient of Thermal Expansion", repr=False, frozen=True
    )
    coefficient_of_thermal_expansion_x: Quantity | None = ParameterField(
        default=None,
        description="The coefficient of thermal expansion in X direction  for the material.",
        matml_name="Coefficient of Thermal Expansion X direction",
    )
    coefficient_of_thermal_expansion_y: Quantity | None = ParameterField(
        default=None,
        description="The coefficient of thermal expansion in Y direction for the material.",
        matml_name="Coefficient of Thermal Expansion Y direction",
    )
    coefficient_of_thermal_expansion_z: Quantity | None = ParameterField(
        default=None,
        description="The coefficient of thermal expansion in Z direction for the material.",
        matml_name="Coefficient of Thermal Expansion Z direction",
    )

    @model_validator(mode="before")
    def _initialize_qualifiers(cls, values) -> Dict:
        expected_qualifiers = {
            "Behavior": ["Orthotropic", QualifierType.STRICT],
            "Definition": ["Instantaneous", QualifierType.FREE, ["Instantaneous", "Secant"]],
        }
        values["model_qualifiers"] = validate_and_initialize_model_qualifiers(
            values, expected_qualifiers
        )
        return values

    def _write_mapdl(self, material_id: int) -> str:
        dependent_parameters = [
            self.coefficient_of_thermal_expansion_x.value,
            self.coefficient_of_thermal_expansion_y.value,
            self.coefficient_of_thermal_expansion_z.value,
        ]
        dependent_parameters_units = [
            self.coefficient_of_thermal_expansion_x.unit,
            self.coefficient_of_thermal_expansion_y.unit,
            self.coefficient_of_thermal_expansion_z.unit,
        ]
        for qualfier in self.model_qualifiers:
            if qualfier.name == "Definition":
                if qualfier.value == "Instantaneous":
                    labels = ["CTEX", "CTEY", "CTEZ"]
                else:
                    labels = ["ALPX", "ALPY", "ALPZ"]

        if not self.independent_parameters:
            material_string = write_constant_properties(
                labels=labels,
                properties=dependent_parameters,
                property_units=dependent_parameters_units,
                material_id=material_id,
            )
            return material_string
        else:
            material_string = ""
            for param in self.independent_parameters:
                if param.name == "Temperature":
                    if param.default_value:
                        temperature = param.default_value
                        if temperature == "Program Controlled":
                            temperature = 22.0
                        material_string += write_temperature_reference_value(
                            material_id, temperature
                        )
            if (
                len(self.independent_parameters) == 1
                and self.independent_parameters[0].name == "Temperature"
            ):
                if len(self.independent_parameters[0].values.value) == 1:
                    material_string += write_constant_properties(
                        labels=labels,
                        properties=dependent_parameters,
                        property_units=dependent_parameters_units,
                        material_id=material_id,
                    )
                    return material_string
                else:
                    material_string += write_temperature_table_values(
                        labels=labels,
                        dependent_parameters=dependent_parameters,
                        dependent_parameters_unit=dependent_parameters_units,
                        material_id=material_id,
                        temperature_parameter=self.independent_parameters[0],
                    )
                    return material_string
            else:
                if labels[0] == "CTEX":
                    raise Exception(
                        "Instantaneus coefficient of expansion is not supported for tb input."
                    )

                parameters_str, table_str = write_table_values(
                    label="CTE",
                    dependent_parameters=dependent_parameters,
                    material_id=material_id,
                    independent_parameters=self.independent_parameters,
                )
                material_string += parameters_str + "\n" + table_str

                if self.interpolation_options:
                    interpolation_string = write_interpolation_options(
                        interpolation_options=self.interpolation_options,
                        independent_parameters=self.independent_parameters,
                    )
                    material_string += "\n" + interpolation_string
        return material_string

    def write_model(self, material_id: int, pyansys_session: Any) -> None:
        """Write this model to the specified session."""
        self.validate_model()
        if isinstance(pyansys_session, _MapdlCore):
            material_string = self._write_mapdl(material_id)
        else:
            raise Exception("The session is not supported.")
        return material_string
