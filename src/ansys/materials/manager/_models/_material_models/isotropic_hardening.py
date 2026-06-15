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
        description="Stress values for the material.",
    )

    yield_strength: Quantity | None = Field(
        default=None,
        description="Yield strength values for the material.",
    )

    tangent_modulus: Quantity | None = Field(
        default=None,
        description="Tangent modulus values for the material.",
    )

    @model_validator(mode="before")
    def _initialize_qualifiers(cls, values) -> Dict:
        expected_qualifiers = {
            "Definition": ["Multilinear", QualifierType.RANGE, ["Multilinear", "Bilinear"]]
        }
        if values:
            definition = values["model_qualifiers"].get("Definition", None)
            if definition is not None:
                if definition == "Bilinear":
                    expected_qualifiers["Table"] = [
                        "Plastic",
                        QualifierType.RANGE,
                        ["Plastic", "Total"],
                    ]
                    expected_qualifiers["Active Table"] = [
                        "Plastic",
                        QualifierType.RANGE,
                        ["Plastic", "Total"],
                    ]
        values["model_qualifiers"] = validate_and_initialize_model_qualifiers(
            values, expected_qualifiers
        )
        return values

    def validate_model(self):
        """Override the validate_model implementation from the baseclass."""
        for qualifier in self.model_qualifiers:
            if qualifier.name == "Definition":
                if qualifier.value == "Bilinear":
                    if self.stress is not None:
                        raise Exception(
                            "Stress values should not be provided for the Bilinear definition of the isotropic hardening model."
                        )
                    if self.yield_strength is None:
                        raise Exception(
                            "Yield Strength values must be provided for the Bilinear definition of the isotropic hardening model."
                        )
                    if self.tangent_modulus is None:
                        raise Exception(
                            "Tangent Modulus values must be provided for the Bilinear definition of the isotropic hardening model."
                        )
            elif qualifier.name == "Multiliear":
                is_plastic_strain = [
                    True if ind_par.name == "Plastic Strain" else False
                    for ind_par in self.independent_parameters
                ]
                if not any(is_plastic_strain):
                    raise Exception(
                        "Plastic Strain has not been provided for the isotropic hardening model."
                    )
                if self.stress is None:
                    raise Exception(
                        "Stress values must be provided for the Multilinear definition of the isotropic hardening model."
                    )
                if self.yield_strength is not None:
                    raise Exception(
                        "Yield Strength values should not be provided for the Multilinear definition of the isotropic hardening model."
                    )
                if self.tangent_modulus is not None:
                    raise Exception(
                        "Tangent Modulus values should not be provided for the Multilinear definition of the isotropic hardening model."
                    )
        super().validate_model()
