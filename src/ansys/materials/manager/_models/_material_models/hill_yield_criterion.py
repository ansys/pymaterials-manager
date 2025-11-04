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

from typing import Dict, Literal

from ansys.units import Quantity
from pydantic import Field, model_validator

from ansys.materials.manager._models._common import (
    MaterialModel,
    ParameterField,
    QualifierType,
    validate_and_initialize_model_qualifiers,
)


class HillYieldCriterion(MaterialModel):
    """Represents a Hill yield criterion material model."""

    name: Literal["Hill Yield Criterion"] = Field(
        default="Hill Yield Criterion", repr=False, frozen=True
    )
    yield_stress_ratio_x: Quantity | None = ParameterField(
        default=None,
        description="The yield stress ratio in the x direction.",
        matml_name="Yield stress ratio in X direction",
    )
    yield_stress_ratio_y: Quantity | None = ParameterField(
        default=None,
        description="The yield stress ratio in the y direction.",
        matml_name="Yield stress ratio in Y direction",
    )
    yield_stress_ratio_z: Quantity | None = ParameterField(
        default=None,
        description="The yield stress ratio in the z direction.",
        matml_name="Yield stress ratio in Z direction",
    )
    yield_stress_ratio_xy: Quantity | None = ParameterField(
        default=None,
        description="The yield stress ratio in the xy direction.",
        matml_name="Yield stress ratio in XY direction",
    )
    yield_stress_ratio_xz: Quantity | None = ParameterField(
        default=None,
        description="The yield stress ratio in the xz direction.",
        matml_name="Yield stress ratio in XZ direction",
    )
    yield_stress_ratio_yz: Quantity | None = ParameterField(
        default=None,
        description="The yield stress ratio in the yz direction.",
        matml_name="Yield stress ratio in YZ direction",
    )
    yield_stress_ratio_x_for_plasticity: Quantity | None = ParameterField(
        default=None,
        description="The yield stress ratio in the x direction for plasticity.",
        matml_name="Yield stress ratio in X direction for plasticity",
    )
    yield_stress_ratio_y_for_plasticity: Quantity | None = ParameterField(
        default=None,
        description="The yield stress ratio in the y direction for plasticity.",
        matml_name="Yield stress ratio in Y direction for plasticity",
    )
    yield_stress_ratio_z_for_plasticity: Quantity | None = ParameterField(
        default=None,
        description="The yield stress ratio in the z direction for plasticity.",
        matml_name="Yield stress ratio in Z direction for plasticity",
    )
    yield_stress_ratio_xy_for_plasticity: Quantity | None = ParameterField(
        default=None,
        description="The yield stress ratio in the xy direction for plasticity.",
        matml_name="Yield stress ratio in XY direction for plasticity",
    )
    yield_stress_ratio_xz_for_plasticity: Quantity | None = ParameterField(
        default=None,
        description="The yield stress ratio in the xz direction for plasticity.",
        matml_name="Yield stress ratio in XZ direction for plasticity",
    )
    yield_stress_ratio_yz_for_plasticity: Quantity | None = ParameterField(
        default=None,
        description="The yield stress ratio in the yz direction for plasticity.",
        matml_name="Yield stress ratio in YZ direction for plasticity",
    )
    yield_stress_ratio_x_for_creep: Quantity | None = ParameterField(
        default=None,
        description="The yield stress ratio in the x direction for creep.",
        matml_name="Yield stress ratio in X direction for creep",
    )
    yield_stress_ratio_y_for_creep: Quantity | None = ParameterField(
        default=None,
        description="The yield stress ratio in the y direction for creep.",
        matml_name="Yield stress ratio in Y direction for creep",
    )
    yield_stress_ratio_z_for_creep: Quantity | None = ParameterField(
        default=None,
        description="The yield stress ratio in the z direction for creep.",
        matml_name="Yield stress ratio in Z direction for creep",
    )
    yield_stress_ratio_xy_for_creep: Quantity | None = ParameterField(
        default=None,
        description="The yield stress ratio in the xy direction for creep.",
        matml_name="Yield stress ratio in XY direction for creep",
    )
    yield_stress_ratio_xz_for_creep: Quantity | None = ParameterField(
        default=None,
        description="The yield stress ratio in the xz direction for creep.",
        matml_name="Yield stress ratio in XZ direction for creep",
    )
    yield_stress_ratio_yz_for_creep: Quantity | None = ParameterField(
        default=None,
        description="The yield stress ratio in the yz direction for creep.",
        matml_name="Yield stress ratio in YZ direction for creep",
    )

    @model_validator(mode="before")
    def _initialize_qualifiers(cls, values) -> Dict:
        expected_qualifiers = {
            "Separated Hill Potentials for Plasticity and Creep": [
                "No",
                QualifierType.RANGE,
                ["Yes", "No"],
            ]
        }
        values["model_qualifiers"] = validate_and_initialize_model_qualifiers(
            values, expected_qualifiers
        )
        return values
