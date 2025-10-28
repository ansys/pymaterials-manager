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


class StrainLimitsOrthotropic(MaterialModel):
    """Represents a strain limits orthotropic material model."""

    name: Literal["Strain Limit"] = Field(default="Strain Limits", repr=False, frozen=True)
    tensile_x_direction: Quantity | None = ParameterField(
        default=None,
        description="The tensile strain limits in the X direction for the strain limits orthotropic model.",  # noqa: E501
        matml_name="Tensile X direction",
    )
    tensile_y_direction: Quantity | None = ParameterField(
        default=None,
        description="The tensile strain limits in the Y direction for the strain limits orthotropic model.",  # noqa: E501
        matml_name="Tensile Y direction",
    )
    tensile_z_direction: Quantity | None = ParameterField(
        default=None,
        description="The tensile strain limits in the Z direction for the strain limits orthotropic model.",  # noqa: E501
        matml_name="Tensile Z direction",
    )
    compressive_x_direction: Quantity | None = ParameterField(
        default=None,
        description="The compressive strain limits in the X direction for the strain limits orthotropic model.",  # noqa: E501
        matml_name="Compressive X direction",
    )
    compressive_y_direction: Quantity | None = ParameterField(
        default=None,
        description="The compressive strain limits in the Y direction for the strain limits orthotropic model.",  # noqa: E501
        matml_name="Compressive Y direction",
    )
    compressive_z_direction: Quantity | None = ParameterField(
        default=None,
        description="The compressive strain limits in the Z direction for the strain limits orthotropic model.",  # noqa: E501
        matml_name="Compressive Z direction",
    )
    shear_xy: Quantity | None = ParameterField(
        default=None,
        description="The shear strain limits in the XY plane for the strain limits orthotropic model.",  # noqa: E501
        matml_name="Shear XY",
    )
    shear_xz: Quantity | None = ParameterField(
        default=None,
        description="The shear strain limits in the XZ plane for the strain limits orthotropic model.",  # noqa: E501
        matml_name="Shear XZ",
    )
    shear_yz: Quantity | None = ParameterField(
        default=None,
        description="The shear strain limits in the YZ plane for the strain limits orthotropic model.",  # noqa: E501
        matml_name="Shear YZ",
    )

    @model_validator(mode="before")
    def _initialize_qualifiers(cls, values) -> Dict:
        expected_qualifiers = {"Behavior": ["Orthotropic", QualifierType.STRICT]}
        values["model_qualifiers"] = validate_and_initialize_model_qualifiers(
            values, expected_qualifiers
        )
        return values
