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

from pydantic import Field, model_validator
from pyparsing import Any

from ansys.materials.manager._models._common._packages import SupportedPackage  # noqa: F401
from ansys.materials.manager._models._common.common import (
    ParameterField,
    QualifierType,
    validate_and_initialize_model_qualifiers,
)
from ansys.materials.manager._models._common.material_model import MaterialModel
from ansys.materials.manager._models._common.model_qualifier import ModelQualifier
from ansys.materials.manager.material import Material


class ElasticityOrthotropic(MaterialModel):
    """Represents an isotropic elasticity material model."""

    name: Literal["Elasticity"] = Field(default="Elasticity", repr=False, frozen=True)

    supported_packages: SupportedPackage = Field(
        default=[SupportedPackage.MAPDL], repr=False, frozen=True
    )
    youngs_modulus_x: list[float] = ParameterField(
        default=[],
        description="The Young's modulus of the material in the x direction.",
        matml_name="Young's Modulus X direction",
    )

    youngs_modulus_y: list[float] = ParameterField(
        default=[],
        description="The Young's modulus of the material in the y direction.",
        matml_name="Young's Modulus Y direction",
    )

    youngs_modulus_z: list[float] = ParameterField(
        default=[],
        description="The Young's modulus of the material in the z direction.",
        matml_name="Young's Modulus Z direction",
    )

    poissons_ratio_yz: list[float] = ParameterField(
        default=[],
        description="The Poisson's ratio yz of the material.",
        matml_name="Poisson's Ratio YZ",
    )

    poissons_ratio_xz: list[float] = ParameterField(
        default=[],
        description="The Poisson's ratio xz of the material.",
        matml_name="Poisson's Ratio XZ",
    )

    poissons_ratio_xy: list[float] = ParameterField(
        default=[],
        description="The Poisson's ratio xy of the material.",
        matml_name="Poisson's Ratio XY",
    )

    shear_modulus_yz: list[float] = ParameterField(
        default=[],
        description="The shear modulus yz of the material.",
        matml_name="Shear Modulus YZ",
    )

    shear_modulus_xz: list[float] = ParameterField(
        default=[],
        description="The shear modulus xz of the material.",
        matml_name="Shear Modulus XZ",
    )

    shear_modulus_xy: list[float] = ParameterField(
        default=[],
        description="The shear modulus xy of the material.",
        matml_name="Shear Modulus XY",
    )
    model_qualifiers: list[ModelQualifier] = Field(
        default=[ModelQualifier(name="Behavior", value="Orthotropic")],
        title="Model Qualifiers",
        description="Model qualifiers for the orthotropic elasticity model.",
    )

    @model_validator(mode="before")
    def _initialize_qualifiers(cls, values) -> Dict:
        expected_qualifiers = {"Behavior": ["Orhtotropic", QualifierType.STRICT]}
        values["model_qualifiers"] = validate_and_initialize_model_qualifiers(
            values, expected_qualifiers
        )
        return values

    def write_model(self, material: Material, pyansys_session: Any) -> None:
        """Write this model to the specified session."""
        pass

    def validate_model(self) -> tuple[bool, list[str]]:
        """Validate the orthotropic elasticity model."""
        pass
