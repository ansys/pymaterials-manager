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


class ThermalConductivityOrthotropic(MaterialModel):
    """Represents an orthotropic thermal conductivity material model."""

    name: Literal["Thermal Conductivity"] = Field(
        default="Thermal Conductivity", repr=False, frozen=True
    )
    supported_packages: SupportedPackage = Field(
        default=[SupportedPackage.MAPDL], repr=False, frozen=True
    )
    thermal_conductivity_x: list[float] = Field(
        default=[],
        title="TThermal Conductivity X direction",
        description="The thermal conductivity in the X direction of the material.",
    )
    thermal_conductivity_y: list[float] = Field(
        default=[],
        title="Thermal Conductivity Y direction",
        description="The thermal conductivity in the Y direction of the material.",
    )
    thermal_conductivity_z: list[float] = Field(
        default=[],
        title="Thermal Conductivity Z direction",
        description="The thermal conductivity in the Z direction of the material.",
    )
    model_qualifiers: list[ModelQualifier] = Field(
        default=[ModelQualifier(name="Behavior", value="Orthotropic")],
        title="Model Qualifiers",
        description="Model qualifiers for the orthotropic thermal conductivity model.",
    )

    @model_validator(mode="before")
    def _initialize_qualifiers(cls, values) -> Dict:
        if "model_qualifiers" in values:
            found_behavior = False
            for model_qualifier in values["model_qualifiers"]:
                if model_qualifier.name == "Behavior" and model_qualifier.value != "Orthotropic":
                    raise ValueError(
                        "Behavior must be 'Orthotropic' for ThermalConductivityOrthotropic model."
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
