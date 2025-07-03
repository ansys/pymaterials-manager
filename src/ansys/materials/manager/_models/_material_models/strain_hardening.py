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
from ansys.materials.manager._models._common.common import ParameterField
from ansys.materials.manager._models._common.material_model import MaterialModel
from ansys.materials.manager.material import Material

from ansys.units import Quantity

class StrainHardening(MaterialModel):
    """Represents a strain hardening material model."""

    name: Literal["Strain Hardening"] = Field(default="Strain Hardening", repr=False, frozen=True)
    supported_packages: SupportedPackage = Field(
        default=[SupportedPackage.MAPDL], repr=False, frozen=True
    )
    creep_constant_1: Quantity | None = ParameterField(
        default=None,
        description="The first creep constant for the strain hardening model.",
        matml_name="Creep Constant 1",
    )
    creep_constant_2: Quantity | None = ParameterField(
        default=None,
        description="The second creep constant for the strain hardening model.",
        matml_name="Creep Constant 2",
    )
    creep_constant_3: Quantity | None = ParameterField(
        default=None,
        description="The third creep constant for the strain hardening model.",
        matml_name="Creep Constant 3",
    )
    creep_constant_4: Quantity | None = ParameterField(
        default=None,
        description="The fourth creep constant for the strain hardening model.",
        matml_name="Creep Constant 4",
    )

    def write_model(self, material: Material, pyansys_session: Any) -> None:
        """Write this model to the specified session."""
        pass

    def validate_model(self) -> tuple[bool, list[str]]:
        """Validate the model."""
        pass
