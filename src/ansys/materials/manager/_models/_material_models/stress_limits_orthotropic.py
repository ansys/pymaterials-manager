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

from pydantic import Field, model_validator

from ansys.materials.manager._models._common._packages import SupportedPackage
from ansys.materials.manager._models._common.material_model import MaterialModel
from ansys.materials.manager._models._common.model_qualifier import ModelQualifier
from ansys.materials.manager.material import Material


class StressLimitsOrthotropic(MaterialModel):
    """Represents a stress limits orthotropic material model."""

    name: Literal["Stress Limit"] = Field(default="Stress Limits", repr=False, frozen=True)
    supported_packages: SupportedPackage = Field(
        default=[SupportedPackage.MAPDL], repr=False, frozen=True
    )
    model_qualifiers: list[ModelQualifier] = Field(
        default=[ModelQualifier(name="Behavior", value="Orthotropic")],
        title="Model Qualifiers",
        description="Model qualifiers for the stress limits orthotropic model.",
    )
    tensile_x_direction: list[float] = Field(
        default=[],
        title="Tensile X direction",
        description="The tensile stress limits in the X direction for the stress limits orthotropic model.",  # noqa: E501
    )
    tensile_y_direction: list[float] = Field(
        default=[],
        title="Tensile Y direction",
        description="The tensile stress limits in the Y direction for the stress limits orthotropic model.",  # noqa: E501
    )
    tensile_z_direction: list[float] = Field(
        default=[],
        title="Tensile Z direction",
        description="The tensile stress limits in the Z direction for the stress limits orthotropic model.",  # noqa: E501
    )
    compressive_x_direction: list[float] = Field(
        default=[],
        title="Compressive X direction",
        description="The compressive stress limits in the X direction for the stress limits orthotropic model.",  # noqa: E501
    )
    compressive_y_direction: list[float] = Field(
        default=[],
        title="Compressive Y direction",
        description="The compressive stress limits in the Y direction for the stress limits orthotropic model.",  # noqa: E501
    )
    compressive_z_direction: list[float] = Field(
        default=[],
        title="Compressive Z direction",
        description="The compressive stress limits in the Z direction for the stress limits orthotropic model.",  # noqa: E501
    )
    shear_xy: list[float] = Field(
        default=[],
        title="Shear XY",
        description="The shear stress limits in the XY plane for the stress limits orthotropic model.",  # noqa: E501
    )
    shear_xz: list[float] = Field(
        default=[],
        title="Shear XZ",
        description="The shear stress limits in the XZ plane for the stress limits orthotropic model.",  # noqa: E501
    )
    shear_yz: list[float] = Field(
        default=[],
        title="Shear YZ",
        description="The shear stress limits in the YZ plane for the stress limits orthotropic model.",  # noqa: E501
    )

    @model_validator(mode="before")
    def _initialize_qualifiers(cls, values) -> Dict:
        if "model_qualifiers" in values:
            found_behavior = False
            for model_qualifier in values["model_qualifiers"]:
                if model_qualifier.name == "Behavior" and model_qualifier.value != "Orthotropic":
                    raise ValueError(
                        "Behavior must be 'Orthotropic' for stressLimitsOrthotropic model."
                    )
                if model_qualifier.name == "Behavior":
                    found_behavior = True
            if not found_behavior:
                model_qualifiers = values.get("model_qualifiers", [])
                isotropic_qualifier = [ModelQualifier(name="Behavior", value="Orthotropic")]
                values["model_qualifiers"] = isotropic_qualifier + model_qualifiers
        return values

    def write_model(self, material: Material, pyansys_session: Any) -> None:
        """Write this model to the specified session."""
        pass

    def validate_model(self) -> tuple[bool, list[str]]:
        """Validate the model."""
        pass
