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


class IndependentParameter:
    """Class representing an independent parameter in a material model."""

    def __init__(
        self,
        name: str,
        values: float,
        default_value: float,
        units: str,
        resolution: str | None = None,
        upper_limit: str | float | None = None,
        lower_limit: str | float | None = None,
    ) -> None:
        """
        Create an instance of the ``IndependentParameter`` class.

        Parameters
        ----------
        name: str
            The name of the independent parameter.
        values: list[float]
            The value of the independent parameter.
        default_value: float
            The default value of the independent parameter.
        units: str
            The units of the independent parameter.
        resolution: str | None

        upper_limit: str | float | None
            upper limit of the independent parameter.
        lower_limit: str | float | None
            lower limit of the independent parameter.
        """
        self.name = name
        self.values = values
        self.default_value = default_value
        self.units = units
        self.resolution = resolution
        self.upper_limit = upper_limit
        self.lower_limit = lower_limit
