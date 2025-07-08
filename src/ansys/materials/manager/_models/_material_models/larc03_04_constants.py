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

from ansys.units import Quantity
from pydantic import Field

from ansys.materials.manager._models._common import MaterialModel, ParameterField


class LaRc0304Constants(MaterialModel):
    """Represents a LaRc03/04 constants material model."""

    name: Literal["LaRc03/04 Constants"] = Field(
        default="LaRc03/04 Constants", repr=False, frozen=True
    )
    fracture_toughness_ratio: Quantity | None = ParameterField(
        default=None,
        description="The ratio of fracture toughness.",
        matml_name="Fracture Toughness Ratio",
    )
    longitudinal_friction_coefficient: Quantity | None = ParameterField(
        default=None,
        description="The coefficient of friction in the longitudinal direction.",
        matml_name="Longitudinal Friction Coefficient",
    )
    transverse_friction_coefficient: Quantity | None = ParameterField(
        default=None,
        description="The coefficient of friction in the transverse direction.",
        matml_name="Transverse Friction Coefficient",
    )
    fracture_angle_under_compression: Quantity | None = ParameterField(
        default=None,
        description="The angle of fracture under compression.",
        matml_name="Fracture Angle Under Compression",
    )

    def write_model(self, material_id: int, pyansys_session: Any) -> None:
        """Write the anisotropic elasticity model to the pyansys session."""
        pass

    def validate_model(self) -> tuple[bool, list[str]]:
        """Validate the anisotropic elasticity model."""
        pass
