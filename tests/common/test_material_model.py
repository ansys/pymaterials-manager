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

from ansys.units import Quantity
import pytest

from ansys.materials.manager._models._common import IndependentParameter
from ansys.materials.manager._models._material_models.density import Density


def test_validate_model_1():
    density = Density(density=Quantity(value=[1.0], units="kg m^-3"))
    density.validate_model()
    assert density


def test_validate_model_2():
    density = Density(
        density=Quantity(value=1.0, units="kg m^-3"),
    )

    density.validate_model()
    assert density


def test_validate_model_3():
    density = Density(
        density=Quantity(value=1.0, units="kg m^-3"),
        independent_parameters=[
            IndependentParameter(name="Temperature", values=Quantity(value=1.0, units="C"))
        ],
    )
    density.validate_model()
    assert density


def test_validate_model_4():
    density = Density(
        density=Quantity(value=1.0, units="kg m^-3"),
        independent_parameters=[
            IndependentParameter(name="Temperature", values=Quantity(value=[1.0], units="C"))
        ],
    )
    density.validate_model()
    assert density


def test_validate_model_5():
    density = Density(
        density=Quantity(value=[1.0], units="kg m^-3"),
        independent_parameters=[
            IndependentParameter(name="Temperature", values=Quantity(value=1.0, units="C"))
        ],
    )
    density.validate_model()
    assert density


def test_validate_model_6():
    density = Density(
        density=Quantity(value=[1.0], units="kg m^-3"),
        independent_parameters=[
            IndependentParameter(name="Temperature", values=Quantity(value=[1.0], units="C"))
        ],
    )
    density.validate_model()
    assert density


def test_validate_model_7():
    density = Density(
        density=Quantity(value=[1.0], units="kg m^-3"),
        independent_parameters=[
            IndependentParameter(name="Temperature", values=Quantity(value=[1.0, 2.0], units="C"))
        ],
    )
    with pytest.raises(Exception) as error_info:
        density.validate_model()
    assert (
        error_info.value.args[0]
        == "The number independent parameters Temperature and dependent parameters density do not match."  # noqa: E501
    )


def test_validate_model_8():
    density = Density(
        density=Quantity(value=[1.0, 2.0], units="kg m^-3"),
        independent_parameters=[
            IndependentParameter(name="Temperature", values=Quantity(value=[1.0], units="C"))
        ],
    )
    with pytest.raises(Exception) as error_info:
        density.validate_model()
    assert (
        error_info.value.args[0]
        == "The number independent parameters Temperature and dependent parameters density do not match."  # noqa: E501
    )


def test_validate_model_9():
    density = Density(
        density=Quantity(value=1.0, units="kg m^-3"),
        independent_parameters=[
            IndependentParameter(name="Temperature", values=Quantity(value=[1.0, 2.0], units="C"))
        ],
    )
    with pytest.raises(Exception) as error_info:
        density.validate_model()
    assert (
        error_info.value.args[0]
        == "The number independent parameters Temperature and dependent parameters density do not match."  # noqa: E501
    )


def test_validate_model_10():
    density = Density(
        density=Quantity(value=[1.0, 2.0], units="kg m^-3"),
        independent_parameters=[
            IndependentParameter(name="Temperature", values=Quantity(value=1.0, units="C"))
        ],
    )
    with pytest.raises(Exception) as error_info:
        density.validate_model()
    assert (
        error_info.value.args[0]
        == "The number independent parameters Temperature and dependent parameters density do not match."  # noqa: E501
    )
