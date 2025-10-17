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


from typing import Literal

from ansys.units import Quantity
from pydantic import Field, model_validator
from pyparsing import Dict

from ansys.materials.manager._models._common import (
    MaterialModel,
    ParameterField,
    QualifierType,
    validate_and_initialize_model_qualifiers,
)


class ElasticityIsotropic(MaterialModel):
    """Represents an isotropic elasticity material model."""

    name: Literal["Elasticity"] = Field(default="Elasticity", repr=False, frozen=True)
    youngs_modulus: Quantity | None = ParameterField(
        default=None,
        description="The Young's modulus of the material.",
        matml_name="Young's Modulus",
        mapdl_name="EX",
        lsdyna_name="e",
    )
    poissons_ratio: Quantity | None = ParameterField(
        default=None,
        description="The Poisson's ratio of the material.",
        matml_name="Poisson's Ratio",
        mapdl_name="PRXY",
        lsdyna_name="pr",
    )

    @model_validator(mode="before")
    def _initialize_qualifiers(cls, values) -> Dict:
        expected_qualifiers = {"Behavior": ["Isotropic", QualifierType.STRICT]}
        values["model_qualifiers"] = validate_and_initialize_model_qualifiers(
            values, expected_qualifiers
        )
        return values
