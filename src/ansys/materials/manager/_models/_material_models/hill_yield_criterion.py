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
from ansys.materials.manager._models.material import Material


class HillYieldCriterion(MaterialModel):
    """Represents a Hill yield criterion material model."""

    name: Literal["Hill Yield Criterion"] = Field(
        default="Hill Yield Criterion", repr=False, frozen=True
    )
    supported_packages: SupportedPackage = Field(
        default=[SupportedPackage.MAPDL], repr=False, frozen=True
    )
    model_qualifiers: list[ModelQualifier] = Field(
        default=[
            ModelQualifier(name="Separated Hill Potentials for Plasticity and Creep", value="No")
        ],
        title="Model Qualifiers",
        description="Model qualifiers for the Hill yield criterion model.",
    )
    yield_stress_ratio_x: list[float] | None = Field(
        default=None,
        title="Yield stress ratio in X direction",
        description="The yield stress ratio in the x direction.",
    )
    yield_stress_ratio_y: list[float] | None = Field(
        default=None,
        title="Yield stress ratio in Y direction",
        description="The yield stress ratio in the y direction.",
    )
    yield_stress_ratio_z: list[float] | None = Field(
        default=None,
        title="Yield stress ratio in Z direction",
        description="The yield stress ratio in the z direction.",
    )
    yield_stress_ratio_xy: list[float] | None = Field(
        default=None,
        title="Yield stress ratio in XY direction",
        description="The yield stress ratio in the xy direction.",
    )
    yield_stress_ratio_xz: list[float] | None = Field(
        default=None,
        title="Yield stress ratio in XZ direction",
        description="The yield stress ratio in the xz direction.",
    )
    yield_stress_ratio_yz: list[float] | None = Field(
        default=None,
        title="Yield stress ratio in YZ direction",
        description="The yield stress ratio in the yz direction.",
    )
    yield_stress_ratio_x_for_plasticity: list[float] | None = Field(
        default=None,
        title="Yield stress ratio in X direction for plasticity",
        description="The yield stress ratio in the x direction for plasticity.",
    )
    yield_stress_ratio_y_for_plasticity: list[float] | None = Field(
        default=None,
        title="Yield stress ratio in Y direction for plasticity",
        description="The yield stress ratio in the y direction for plasticity.",
    )
    yield_stress_ratio_z_for_plasticity: list[float] | None = Field(
        default=None,
        title="Yield stress ratio in Z direction for plasticity",
        description="The yield stress ratio in the z direction for plasticity.",
    )
    yield_stress_ratio_xy_for_plasticity: list[float] | None = Field(
        default=None,
        title="Yield stress ratio in XY direction for plasticity",
        description="The yield stress ratio in the xy direction for plasticity.",
    )
    yield_stress_ratio_xz_for_plasticity: list[float] | None = Field(
        default=None,
        title="Yield stress ratio in XZ direction for plasticity",
        description="The yield stress ratio in the xz direction for plasticity.",
    )
    yield_stress_ratio_yz_for_plasticity: list[float] | None = Field(
        default=None,
        title="Yield stress ratio in YZ direction for plasticity",
        description="The yield stress ratio in the yz direction for plasticity.",
    )
    yield_stress_ratio_x_for_creep: list[float] | None = Field(
        default=None,
        title="Yield stress ratio in X direction for creep",
        description="The yield stress ratio in the x direction for creep.",
    )
    yield_stress_ratio_y_for_creep: list[float] | None = Field(
        default=None,
        title="Yield stress ratio in Y direction for creep",
        description="The yield stress ratio in the y direction for creep.",
    )
    yield_stress_ratio_z_for_creep: list[float] | None = Field(
        default=None,
        title="Yield stress ratio in Z direction for creep",
        description="The yield stress ratio in the z direction for creep.",
    )
    yield_stress_ratio_xy_for_creep: list[float] | None = Field(
        default=None,
        title="Yield stress ratio in XY direction for creep",
        description="The yield stress ratio in the xy direction for creep.",
    )
    yield_stress_ratio_xz_for_creep: list[float] | None = Field(
        default=None,
        title="Yield stress ratio in XZ direction for creep",
        description="The yield stress ratio in the xz direction for creep.",
    )
    yield_stress_ratio_yz_for_creep: list[float] | None = Field(
        default=None,
        title="Yield stress ratio in YZ direction for creep",
        description="The yield stress ratio in the yz direction for creep.",
    )

    def write_model(self, material: Material, pyansys_session: Any) -> None:
        """Write this model to the specified session."""
        pass

    def validate_model(self) -> tuple[bool, list[str]]:
        """Validate the model."""
        pass
