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

from ansys.materials.manager._models._common.independent_parameter import IndependentParameter


def test_independent_parameter_creation():
    name = "Temperature"
    values = 300.0
    default_value = 293.15
    units = "K"
    upper_limit = 1000.0
    lower_limit = 0.0

    independent_param = IndependentParameter(
        name=name,
        values=values,
        default_value=default_value,
        units=units,
        upper_limit=upper_limit,
        lower_limit=lower_limit,
    )

    assert independent_param.name == name
    assert independent_param.values == values
    assert independent_param.default_value == default_value
    assert independent_param.units == units
    assert independent_param.upper_limit == upper_limit
    assert independent_param.lower_limit == lower_limit
    assert isinstance(independent_param, IndependentParameter)
