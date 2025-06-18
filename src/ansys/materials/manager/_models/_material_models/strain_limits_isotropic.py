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


class StrainLimitsIsotropic(MaterialModel):
    """Represents a strain limits isotropic material model."""

    name: Literal["Strain Limits"] = Field(default="Strain Limits", repr=False, frozen=True)
    supported_packages: SupportedPackage = Field(
        default=[SupportedPackage.MAPDL], repr=False, frozen=True
    )
    model_qualifiers: list[ModelQualifier] = Field(
        default=[ModelQualifier(name="Definition", value="Isotropic")],
        title="Model Qualifiers",
        description="Model qualifiers for the strain limits isotropic model.",
    )
    von_mises: list[float] = Field(
        default=[],
        title="Von Mises Stress",
        description="The von Mises stress values for the strain limits isotropic model.",
    )

    @model_validator(mode="before")
    def _initialize_qualifiers(cls, values) -> Dict:
        if "model_qualifiers" in values:
            found_behavior = False
            for model_qualifier in values["model_qualifiers"]:
                if model_qualifier.name == "Behavior" and model_qualifier.value != "Isotropic":
                    raise ValueError(
                        "Behavior must be 'Isotropic' for strainLimitsIsotropic model."
                    )
                if model_qualifier.name == "Behavior":
                    found_behavior = True
            if not found_behavior:
                model_qualifiers = values.get("model_qualifiers", [])
                isotropic_qualifier = [ModelQualifier(name="Behavior", value="Isotropic")]
                values["model_qualifiers"] = isotropic_qualifier + model_qualifiers
        return values

    def write_model(self, material: Material, pyansys_session: Any) -> None:
        """Write this model to the specified session."""
        pass

    def validate_model(self) -> tuple[bool, list[str]]:
        """Validate the model."""
        pass
