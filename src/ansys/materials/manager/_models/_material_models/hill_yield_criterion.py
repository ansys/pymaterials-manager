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
from ansys.materials.manager._models.material import Material


class HillYieldCriterion(MaterialModel):
    """Represents a Hill yield criterion material model."""

    name: Literal["hill_yield_criterion"] = Field(
        default="hill_yield_criterion", repr=False, frozen=True
    )
    supported_packages: SupportedPackage = Field(
        default=[SupportedPackage.MAPDL], repr=False, frozen=True
    )
    separated_hill_potentials_for_plasticity_and_creep: str = Field(
        default="No",
        title="Separated Hill Potentials for Plasticity and Creep",
        description="Indicates whether the Hill potentials for plasticity and creep are separated. If set to 'yes', the model uses separate Hill potentials for plasticity and creep; if 'no', it uses a single Hill potential for both.",  # noqa: E501
    )
    yield_stress_ratio_x: list[float] = Field(
        default=[],
        title="Yield stress ratio in X direction",
        description="The yield stress ratio in the x direction.",
    )
    yield_stress_ratio_y: list[float] = Field(
        default=[],
        title="Yield stress ratio in Y direction",
        description="The yield stress ratio in the y direction.",
    )
    yield_stress_ratio_z: list[float] = Field(
        default=[],
        title="Yield stress ratio in Z direction",
        description="The yield stress ratio in the z direction.",
    )
    yield_stress_ratio_xy: list[float] = Field(
        default=[],
        title="Yield stress ratio in XY direction",
        description="The yield stress ratio in the xy direction.",
    )
    yield_stress_ratio_xz: list[float] = Field(
        default=[],
        title="Yield stress ratio in XZ direction",
        description="The yield stress ratio in the xz direction.",
    )
    yield_stress_ratio_yz: list[float] = Field(
        default=[],
        title="Yield stress ratio in YZ direction",
        description="The yield stress ratio in the yz direction.",
    )

    def write_model(self, material: Material, pyansys_session: Any) -> None:
        """Write this model to the specified session."""
        pass

    def validate_model(self) -> tuple[bool, list[str]]:
        """Validate the model."""
        pass
