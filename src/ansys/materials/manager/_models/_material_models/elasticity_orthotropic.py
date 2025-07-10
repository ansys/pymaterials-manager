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

from typing import Dict, Literal

from ansys.units import Quantity
from pydantic import Field, model_validator
from pyparsing import Any

from ansys.materials.manager._models._common import (
    MaterialModel,
    ParameterField,
    QualifierType,
    validate_and_initialize_model_qualifiers,
)
from ansys.materials.manager._models._common._base import _MapdlCore
from ansys.materials.manager.util.mapdl.mapdl_writer import (
    write_constant_properties,
    write_interpolation_options,
    write_table_values,
    write_temperature_table_values,
)


class ElasticityOrthotropic(MaterialModel):
    """Represents an isotropic elasticity material model."""

    name: Literal["Elasticity"] = Field(default="Elasticity", repr=False, frozen=True)

    youngs_modulus_x: Quantity | None = ParameterField(
        default=None,
        description="The Young's modulus of the material in the x direction.",
        matml_name="Young's Modulus X direction",
    )

    youngs_modulus_y: Quantity | None = ParameterField(
        default=None,
        description="The Young's modulus of the material in the y direction.",
        matml_name="Young's Modulus Y direction",
    )

    youngs_modulus_z: Quantity | None = ParameterField(
        default=None,
        description="The Young's modulus of the material in the z direction.",
        matml_name="Young's Modulus Z direction",
    )

    poissons_ratio_yz: Quantity | None = ParameterField(
        default=None,
        description="The Poisson's ratio yz of the material.",
        matml_name="Poisson's Ratio YZ",
    )

    poissons_ratio_xz: Quantity | None = ParameterField(
        default=None,
        description="The Poisson's ratio xz of the material.",
        matml_name="Poisson's Ratio XZ",
    )

    poissons_ratio_xy: Quantity | None = ParameterField(
        default=None,
        description="The Poisson's ratio xy of the material.",
        matml_name="Poisson's Ratio XY",
    )

    shear_modulus_yz: Quantity | None = ParameterField(
        default=None,
        description="The shear modulus yz of the material.",
        matml_name="Shear Modulus YZ",
    )

    shear_modulus_xz: Quantity | None = ParameterField(
        default=None,
        description="The shear modulus xz of the material.",
        matml_name="Shear Modulus XZ",
    )

    shear_modulus_xy: Quantity | None = ParameterField(
        default=None,
        description="The shear modulus xy of the material.",
        matml_name="Shear Modulus XY",
    )

    @model_validator(mode="before")
    def _initialize_qualifiers(cls, values) -> Dict:
        expected_qualifiers = {"Behavior": ["Orthotropic", QualifierType.STRICT]}
        values["model_qualifiers"] = validate_and_initialize_model_qualifiers(
            values, expected_qualifiers
        )
        return values

    def _write_mapdl(self, material_id: int) -> str:
        dependent_parameters = [
            self.youngs_modulus_x,
            self.youngs_modulus_y,
            self.youngs_modulus_z,
            self.shear_modulus_xy,
            self.shear_modulus_yz,
            self.shear_modulus_xz,
            self.poissons_ratio_xy,
            self.poissons_ratio_yz,
            self.poissons_ratio_xz,
        ]
        if self.independent_parameters is None:
            material_string = write_constant_properties(
                labels=["EX", "EY", "EZ", "GXY", "GXZ", "GZY", "PRXY", "PRXZ", "PRYZ"],
                properties=dependent_parameters,
                material_id=material_id,
            )
            return material_string
        elif (
            len(self.independent_parameters) == 1
            and self.independent_parameters[0].name == "Temperature"
        ):
            if len(self.independent_parameters[0].values.value) == 1:
                material_string = write_constant_properties(
                    labels=["EX", "EY", "EZ", "GXY", "GXZ", "GZY", "PRXY", "PRXZ", "PRYZ"],
                    properties=dependent_parameters,
                    material_id=material_id,
                )
                return material_string
            else:
                material_string = write_temperature_table_values(
                    labels=["EX", "EY", "EZ", "GXY", "GXZ", "GZY", "PRXY", "PRXZ", "PRYZ"],
                    dependent_parameters=dependent_parameters,
                    material_id=material_id,
                    temperature_parameter=self.independent_parameters[0],
                )

        else:
            parameters_str, table_str = write_table_values(
                label="ELASTIC",
                dependent_parameters=dependent_parameters,
                material_id=material_id,
                independent_parameters=self.independent_parameters,
                tb_opt="OELM",
            )
            interpolation_string = ""
            if self.interpolation_options:
                interpolation_string += write_interpolation_options(
                    interpolation_options=self.interpolation_options,
                    independent_parameters=self.independent_parameters,
                )
            material_string = parameters_str + "\n" + table_str + "\n" + interpolation_string
        return material_string

    def write_model(self, material_id: int, pyansys_session: Any) -> str:
        """Write this model to the specified session."""
        self.validate_model()
        if isinstance(pyansys_session, _MapdlCore):
            material_string = self._write_mapdl(material_id)
        else:
            raise Exception("The session is not supported.")
        return material_string
