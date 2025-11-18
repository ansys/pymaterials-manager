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
    QualifierType,
    validate_and_initialize_model_qualifiers,
)


class IsotropicHardening(MaterialModel):
    """Represents an isotropic hardening material model."""

    name: Literal["Isotropic Hardening"] = Field(
        default="Isotropic Hardening", repr=False, frozen=True
    )

    stress: Quantity | None = Field(
        default=None,
        description="Stress values for the material. Needed for multilinear definition.",
    )

    yield_strength: Quantity | None = Field(
        default=None,
        description="Yield strength of the material. Needed for bilinear definition.",
    )

    tangent_modulus: Quantity | None = Field(
        default=None,
        description="Tangent modulus of the material. Needed for bilinear definition.",
    )

    @model_validator(mode="before")
    def _initialize_qualifiers(cls, values) -> Dict:
        expected_qualifiers = {
            "Definition": ["Multilinear", QualifierType.RANGE, ["Multilinear", "Bilinear"]]
        }
        values["model_qualifiers"] = validate_and_initialize_model_qualifiers(
            values, expected_qualifiers
        )
        return values

    def validate_model(self):
        """Override the validate_model implementation from the baseclass."""
        is_multilinear = False
        is_bilinear = False
        for qualifier in self.model_qualifiers:
            if qualifier.name == "Definition" and qualifier.value == "Multilinear":
                is_multilinear = True
            if qualifier.name == "Definition" and qualifier.value == "Bilinear":
                is_bilinear = True

        if is_multilinear:
            is_plastic_strain = [
                True if ind_par.name == "Plastic Strain" else False
                for ind_par in self.independent_parameters
            ]
            if not any(is_plastic_strain):
                raise Exception(
                    "Plastic Strain has not been provided for the multilinear isotropic hardening model."  # noqa: E501
                )

        if is_bilinear:
            if self.yield_strength is None:
                raise Exception(
                    "Yield Strength has not been provided for the bilinear isotropic hardening model."  # noqa: E501
                )
            if self.tangent_modulus is None:
                raise Exception(
                    "Tangent Modulus has not been provided for the bilinear isotropic hardening model."  # noqa: E501
                )

        super().validate_model()
