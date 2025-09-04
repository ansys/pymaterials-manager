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


from pydantic import BaseModel, Field


class InterpolationOptions(BaseModel):
    """Class to hold interpolation options for material models."""

    algorithm_type: str = Field(
        default="", title="Algorithm Type", description="Type of interpolation algorithm to use."
    )
    normalized: bool = Field(
        default=True,
        title="Normalized",
        description="True if the independent parameters are normalized before doing the interpolation.",  # noqa: E501
    )
    cached: bool = Field(
        default=True, title="Cached", description="Whether to cache the interpolation results."
    )
    extrapolation_type: str | None = Field(
        default=None, title="Extrapolation Type", description="Type of extrapolation to use."
    )
