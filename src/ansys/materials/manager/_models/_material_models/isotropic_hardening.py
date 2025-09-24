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

from ast import Dict
from typing import Any, Literal

from ansys.units import Quantity
from pydantic import Field, model_validator

from ansys.materials.manager._models._common import (
    MaterialModel,
    ParameterField,
    QualifierType,
    _MapdlCore,
    validate_and_initialize_model_qualifiers,
)
from ansys.materials.manager.util.mapdl.mapdl_writer import write_tb_points_for_temperature


class IsotropicHardening(MaterialModel):
    """Represents an isotropic hardening material model."""

    name: Literal["Isotropic Hardening"] = Field(
        default="Isotropic Hardening", repr=False, frozen=True
    )

    stress: Quantity | None = ParameterField(
        default=None,
        description="Stress values for the material.",
        matml_name="Stress",
    )

    @model_validator(mode="before")
    def _initialize_qualifiers(cls, values) -> Dict:
        expected_qualifiers = {"Definition": ["Multilinear", QualifierType.STRICT]}
        values["model_qualifiers"] = validate_and_initialize_model_qualifiers(
            values, expected_qualifiers
        )
        return values

    def _write_mapdl(self, material_id: int) -> str:
        plastic_strain = [
            ind_param.values.value.tolist()
            for ind_param in self.independent_parameters
            if ind_param.name == "Plastic Strain"
        ][0]
        temperature = [
            ind_param.values.value.tolist()
            for ind_param in self.independent_parameters
            if ind_param.name == "Temperature"
        ]
        table_parameters = [
            plastic_strain,
            self.stress.value.tolist(),
        ]
        if len(self.independent_parameters) == 1:
            temperature_parameter = len(table_parameters[0]) * [0]
            material_string = write_tb_points_for_temperature(
                label="PLASTIC",
                table_parameters=table_parameters,
                material_id=material_id,
                temperature_parameter=temperature_parameter,
                tb_opt="MISO",
            )

        elif len(self.independent_parameters) == 2 and len(temperature) == 1:
            material_string = write_tb_points_for_temperature(
                label="PLASTIC",
                table_parameters=table_parameters,
                material_id=material_id,
                temperature_parameter=temperature[0],
                tb_opt="MISO",
            )
        else:
            raise Exception("Only variable supported at the moment is temperature")
        return material_string

    def validate_model(self):
        """Override the validate_model implementation from the baseclass."""
        is_plastic_strain = [
            True if ind_par.name == "Plastic Strain" else False
            for ind_par in self.independent_parameters
        ]
        if not any(is_plastic_strain):
            raise Exception(
                "Plastic Strain has not been provided for the isotropic hardening model."
            )
        super().validate_model()

    def write_model(self, material_id: int, pyansys_session: Any) -> str:
        """Write this model to the specified session."""
        self.validate_model()
        if isinstance(pyansys_session, _MapdlCore):
            material_string = self._write_mapdl(material_id)
        else:
            raise Exception("The session is not supported.")
        return material_string
