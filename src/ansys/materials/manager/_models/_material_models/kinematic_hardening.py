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

from typing import Any, Literal

from pydantic import Field

from ansys.materials.manager._models._common._packages import SupportedPackage
from ansys.materials.manager._models._common.material_model import MaterialModel
from ansys.materials.manager._models._common.model_qualifier import ModelQualifier
from ansys.materials.manager.material import Material


class KinematicHardening(MaterialModel):
    """Represents a kinematic hardening material model."""

    name: Literal["Kinematic Hardening"] = Field(
        default="Kinematic Hardening", repr=False, frozen=True
    )
    supported_packages: SupportedPackage = Field(
        default=[SupportedPackage.MAPDL], repr=False, frozen=True
    )
    model_qualifiers: list[ModelQualifier] = Field(
        default=[
            ModelQualifier(name="Definition", value="Chaboche"),
            ModelQualifier(name="Number of Kinematic Models", value="1"),
            ModelQualifier(name="source", value="ANSYS"),
        ],
        title="Model Qualifiers",
        description="Model qualifiers for the kinematic hardening model.",
    )
    yield_stress: list[float] = Field(
        default=[],
        title="Yield Stress",
        description="The yield stress values for the kinematic hardening model.",
    )
    material_constant_gamma_1: list[float] = Field(
        default=[],
        title="Material Constant γ1",
        description="The first material constant γ1 for the kinematic hardening model.",
    )
    material_constant_c_1: list[float] = Field(
        default=[],
        title="Material Constant C1",
        description="The first material constant C1 for the kinematic hardening model.",
    )
    material_constant_gamma_2: list[float] | None = Field(
        default=None,
        title="Material Constant γ2",
        description="The second material constant γ2 for the kinematic hardening model.",
    )
    material_constant_c_2: list[float] | None = Field(
        default=None,
        title="Material Constant C2",
        description="The second material constant C2 for the kinematic hardening model.",
    )
    material_constant_gamma_3: list[float] | None = Field(
        default=None,
        title="Material Constant γ3",
        description="The third material constant γ3 for the kinematic hardening model.",
    )
    material_constant_c_3: list[float] | None = Field(
        default=None,
        title="Material Constant C3",
        description="The third material constant C3 for the kinematic hardening model.",
    )
    material_constant_gamma_4: list[float] | None = Field(
        default=None,
        title="Material Constant γ4",
        description="The fourth material constant γ4 for the kinematic hardening model.",
    )
    material_constant_c_4: list[float] | None = Field(
        default=None,
        title="Material Constant C4",
        description="The fourth material constant C4 for the kinematic hardening model.",
    )
    material_constant_gamma_5: list[float] | None = Field(
        default=None,
        title="Material Constant γ5",
        description="The fifth material constant γ5 for the kinematic hardening model.",
    )
    material_constant_c_5: list[float] | None = Field(
        default=None,
        title="Material Constant C5",
        description="The fifth material constant C5 for the kinematic hardening model.",
    )

    def write_model(self, material: Material, pyansys_session: Any) -> None:
        """Write this model to the specified session."""
        pass

    def validate_model(self) -> tuple[bool, list[str]]:
        """Validate the model."""
        pass
