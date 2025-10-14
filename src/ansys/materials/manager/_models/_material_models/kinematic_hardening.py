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

from ast import Dict
from typing import Literal

from ansys.units import Quantity
from pydantic import Field, model_validator

from ansys.materials.manager._models._common import (
    MaterialModel,
    ParameterField,
    QualifierType,
    validate_and_initialize_model_qualifiers,
)


class KinematicHardening(MaterialModel):
    """Represents a kinematic hardening material model."""

    name: Literal["Kinematic Hardening"] = Field(
        default="Kinematic Hardening", repr=False, frozen=True
    )
    yield_stress: Quantity | None = ParameterField(
        default=None,
        description="The yield stress values for the kinematic hardening model.",
        matml_name="Yield Stress",
    )
    material_constant_gamma_1: Quantity | None = ParameterField(
        default=None,
        description="The first material constant γ1 for the kinematic hardening model.",
        matml_name="Material Constant γ1",
    )
    material_constant_c_1: Quantity | None = ParameterField(
        default=None,
        description="The first material constant C1 for the kinematic hardening model.",
        matml_name="Material Constant C1",
    )
    material_constant_gamma_2: Quantity | None = ParameterField(
        default=None,
        description="The second material constant γ2 for the kinematic hardening model.",
        matml_name="Material Constant γ2",
    )
    material_constant_c_2: Quantity | None = ParameterField(
        default=None,
        description="The second material constant C2 for the kinematic hardening model.",
        matml_name="Material Constant C2",
    )
    material_constant_gamma_3: Quantity | None = ParameterField(
        default=None,
        description="The third material constant γ3 for the kinematic hardening model.",
        matml_name="Material Constant γ3",
    )
    material_constant_c_3: Quantity | None = ParameterField(
        default=None,
        description="The third material constant C3 for the kinematic hardening model.",
        matml_name="Material Constant C3",
    )
    material_constant_gamma_4: Quantity | None = ParameterField(
        default=None,
        description="The fourth material constant γ4 for the kinematic hardening model.",
        matml_name="Material Constant γ4",
    )
    material_constant_c_4: Quantity | None = ParameterField(
        default=None,
        description="The fourth material constant C4 for the kinematic hardening model.",
        matml_name="Material Constant C4",
    )
    material_constant_gamma_5: Quantity | None = ParameterField(
        default=None,
        description="The fifth material constant γ5 for the kinematic hardening model.",
        matml_name="Material Constant γ5",
    )
    material_constant_c_5: Quantity | None = ParameterField(
        default=None,
        description="The fifth material constant C5 for the kinematic hardening model.",
        matml_name="Material Constant C5",
    )

    @model_validator(mode="before")
    def _initialize_qualifiers(cls, values) -> Dict:
        expected_qualifiers = {
            "Definition": ["Chaboche", QualifierType.STRICT],
            "Number of Kinematic Models": ["1", QualifierType.RANGE, ["1", "2", "3", "4", "5"]],
            "source": ["ANSYS", QualifierType.STRICT],
        }
        values["model_qualifiers"] = validate_and_initialize_model_qualifiers(
            values, expected_qualifiers
        )
        return values
