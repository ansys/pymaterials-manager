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
from ansys.materials.manager.material import Material


class AdditionalPuckConstants(MaterialModel):
    """Represents additional Puck constants for material modeling."""

    name: Literal["Additional Puck Constants"] = Field(
        default="Additional Puck Constants", repr=False, frozen=True
    )
    interface_weakening_factor: Quantity | None = ParameterField(
        default=None,
        description="The interface weakening factor for the additional Puck constants model.",
        matml_name="Interface Weakening Factor",
    )
    degradation_parameter_s: Quantity | None = ParameterField(
        default=None,
        description="The degradation parameter s for the additional Puck constants model.",
        matml_name="Degradation Parameter s",
    )
    degradation_parameter_m: Quantity | None = ParameterField(
        default=None,
        description="The degradation parameter M for the additional Puck constants model.",
        matml_name="Degradation Parameter M",
    )

    def write_model(self, material: Material, pyansys_session: Any) -> None:
        """Write this model to the specified session."""
        pass

    def validate_model(self) -> tuple[bool, list[str]]:
        """Validate the model."""
        pass
