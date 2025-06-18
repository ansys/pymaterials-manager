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


class CoefficientofThermalExpansionOrthotropic(MaterialModel):
    """Represents an orthotropic coefficient of thermal expansion material model."""

    name: Literal["Coefficient of Thermal Expansion"] = Field(
        default="Coefficient of Thermal Expansion", repr=False, frozen=True
    )
    supported_packages: SupportedPackage = Field(
        default=[SupportedPackage.MAPDL], repr=False, frozen=True
    )
    coefficient_of_thermal_expansion_x: list[float] = Field(
        default=[],
        title="Coefficient of Thermal Expansion X direction",
        description="The coefficient of thermal expansion in X direction  for the material.",
    )
    coefficient_of_thermal_expansion_y: list[float] = Field(
        default=[],
        title="Coefficient of Thermal Expansion Y direction",
        description="The coefficient of thermal expansion in Y direction for the material.",
    )
    coefficient_of_thermal_expansion_z: list[float] = Field(
        default=[],
        title="Coefficient of Thermal Expansion Z direction",
        description="The coefficient of thermal expansion in Z direction for the material.",
    )

    model_qualifiers: list[ModelQualifier] = Field(
        default=[ModelQualifier(name="Behavior", value="Orthotropic")],
        title="Model Qualifiers",
        description="Model qualifiers for the orthotropic coefficient of thermal expansion model.",
    )

    @model_validator(mode="before")
    def _initialize_qualifiers(cls, values) -> Dict:
        if "model_qualifiers" in values:
            found_behavior = False
            found_definition = False
            for model_qualifier in values["model_qualifiers"]:
                if model_qualifier.name == "Behavior" and model_qualifier.value != "Orthotropic":
                    raise ValueError(
                        "Behavior must be 'Orthotropic' for CoefficientofThermalExpansionOrthotropic model."  # noqa: E501
                    )
                if model_qualifier.name == "Behavior":
                    found_behavior = True
                if model_qualifier.name == "Definition":
                    found_definition = True
            if not found_definition:
                model_qualifiers = values.get("model_qualifiers", [])
                definition_qualifier = [ModelQualifier(name="Definition", value="Instantaneous")]
                values["model_qualifiers"] = definition_qualifier + model_qualifiers
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
        # as we have distinction between the secant and instantaneous coefficient
        # of thermal expansion
        # we need to validate that the model qualifiers are set correctly
        # i.e. [ModelQualifier(name="Definition", value="Secant")] or
        # [ModelQualifier(name="Definition", value="Instantaneous")] is present
        pass
