# Copyright (C) 2022 - 2026 ANSYS, Inc. and/or its affiliates.
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

from typing import Literal

from ansys.units import Quantity
from pydantic import Field

from ansys.materials.manager._models._common import MaterialModel
from ansys.materials.manager._models._common.tabular_quantity import TabularQuantity


class TensileStrengthUltimate(MaterialModel):
    """Represents an ultimate tensile strength material model."""

    name: Literal["Tensile Strength, Ultimate"] = Field(
        default="Tensile Strength, Ultimate", repr=False, frozen=True
    )
    tensile_strength_ultimate: TabularQuantity | Quantity | None = Field(
        default=None,
        description="The ultimate tensile strength of the material.",
    )


class TensileStrengthYield(MaterialModel):
    """Represents a yield (proof) tensile strength material model."""

    name: Literal["Tensile Strength, Yield"] = Field(
        default="Tensile Strength, Yield", repr=False, frozen=True
    )
    tensile_strength_yield: TabularQuantity | Quantity | None = Field(
        default=None,
        description="The yield tensile strength of the material.",
    )
