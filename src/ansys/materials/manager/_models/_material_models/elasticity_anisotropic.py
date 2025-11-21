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
    QualifierType,
    validate_and_initialize_model_qualifiers,
)


class ElasticityAnisotropic(MaterialModel):
    """Represents an isotropic elasticity material model."""

    name: Literal["Elasticity"] = Field(default="Elasticity", repr=False, frozen=True)

    c_11: Quantity | None = Field(
        default=None,
        description="The C11 component of the elasticity matrix.",
    )
    c_12: Quantity | None = Field(
        default=None,
        description="The C12 component of the elasticity matrix.",
    )
    c_13: Quantity | None = Field(
        default=None,
        description="The C13 component of the elasticity matrix.",
    )
    c_14: Quantity | None = Field(
        default=None,
        description="The C14 component of the elasticity matrix.",
    )
    c_15: Quantity | None = Field(
        default=None,
        description="The C15 component of the elasticity matrix.",
    )
    c_16: Quantity | None = Field(
        default=None,
        description="The C16 component of the elasticity matrix.",
    )
    c_22: Quantity | None = Field(
        default=None,
        description="The C22 component of the elasticity matrix.",
    )
    c_23: Quantity | None = Field(
        default=None,
        description="The C23 component of the elasticity matrix.",
    )
    c_24: Quantity | None = Field(
        default=None,
        description="The C24 component of the elasticity matrix.",
    )
    c_25: Quantity | None = Field(
        default=None,
        description="The C25 component of the elasticity matrix.",
    )
    c_26: Quantity | None = Field(
        default=None,
        description="The C26 component of the elasticity matrix.",
    )
    c_33: Quantity | None = Field(
        default=None,
        description="The C33 component of the elasticity matrix.",
    )
    c_34: Quantity | None = Field(
        default=None,
        description="The C34 component of the elasticity matrix.",
    )
    c_35: Quantity | None = Field(
        default=None,
        description="The C35 component of the elasticity matrix.",
    )
    c_36: Quantity | None = Field(
        default=None,
        description="The C36 component of the elasticity matrix.",
    )
    c_44: Quantity | None = Field(
        default=None,
        description="The C44 component of the elasticity matrix.",
    )
    c_45: Quantity | None = Field(
        default=None,
        description="The C45 component of the elasticity matrix.",
    )
    c_46: Quantity | None = Field(
        default=None,
        description="The C46 component of the elasticity matrix.",
    )
    c_55: Quantity | None = Field(
        default=None,
        description="The C55 component of the elasticity matrix.",
    )
    c_56: Quantity | None = Field(
        default=None,
        description="The C56 component of the elasticity matrix.",
    )
    c_66: Quantity | None = Field(
        default=None,
        description="The C66 component of the elasticity matrix.",
    )

    @model_validator(mode="before")
    def _initialize_qualifiers(cls, values) -> Dict:
        expected_qualifiers = {"Behavior": ["Anisotropic", QualifierType.STRICT]}
        values["model_qualifiers"] = validate_and_initialize_model_qualifiers(
            values, expected_qualifiers
        )
        return values
