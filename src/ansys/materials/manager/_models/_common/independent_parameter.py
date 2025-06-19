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


from typing import Union

from pydantic import BaseModel, Field


class IndependentParameter(BaseModel):
    """Class representing an independent parameter in a material model."""

    name: str = Field(
        default="", title="Name", description="The name of the independent parameter."
    )
    values: list[float] = Field(
        default=[], title="Values", description="The values of the independent parameter."
    )
    field_variable: str | None = Field(
        default=None,
        title="Field Variable",
        description="The field variable associated with the independent parameter.",
    )
    default_value: Union[str | float | None] = Field(
        default=None,
        title="Default Value",
        description="The default value of the independent parameter.",
    )
    unit: str | None = Field(
        default="", title="Unit", description="The unit of the independent parameter."
    )
    upper_limit: Union[str | float | None] = Field(
        default=None, title="Upper Limit", description="Upper limit of the independent parameter."
    )
    lower_limit: Union[str | float | None] = Field(
        default=None, title="Lower Limit", description="Lower limit of the independent parameter."
    )
