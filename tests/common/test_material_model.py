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

from ansys.units import Quantity
import pytest

from ansys.materials.manager._models._common import IndependentParameter
from ansys.materials.manager._models._common.tabular_quantity import TabularQuantity
from ansys.materials.manager._models._material_models.density import Density
from ansys.materials.manager._models._material_models.elasticity_isotropic import (
    ElasticityIsotropic,
)
from ansys.materials.manager._models.material import Material


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


def test_validate_model_tabular_quantity():
    density = Density(
        density=TabularQuantity(
            values=Quantity(value=[1.0, 2.0], units="kg m^-3"),
            independent_parameters=[
                IndependentParameter(
                    name="Temperature", values=Quantity(value=[20.0, 30.0], units="C")
                )
            ],
        )
    )

    density.validate_model()
    assert density


def test_delete_material_model():
    material = Material(
        name="Test Material",
        models=[
            Density(
                density=Quantity(value=[1.0], units="kg m^-3"),
                independent_parameters=[
                    IndependentParameter(
                        name="Temperature", values=Quantity(value=[1.0], units="C")
                    )
                ],
            )
        ],
    )
    material.remove_model_by_name("Density")
    density = material.get_model_by_name("Density")
    assert density is None


def test_append_single_model():
    material = Material(
        name="Test Material",
        models=[
            Density(
                density=Quantity(value=[1.0], units="kg m^-3"),
                independent_parameters=[
                    IndependentParameter(
                        name="Temperature", values=Quantity(value=[1.0], units="C")
                    )
                ],
            )
        ],
    )
    elasticity = ElasticityIsotropic(
        youngs_modulus=Quantity(value=[2.0], units="Pa"),
        poissons_ratio=Quantity(value=[0.3], units=""),
        independent_parameters=[
            IndependentParameter(name="Temperature", values=Quantity(value=[2.0], units="C"))
        ],
    )
    material.append_models(elasticity)
    elasticity_model = material.get_model_by_name("Elasticity")
    assert elasticity_model is not None


def test_get_independent_parameter_by_name():
    density = Density(
        density=Quantity(value=[1.0], units="kg m^-3"),
        independent_parameters=[
            IndependentParameter(name="Temperature", values=Quantity(value=[1.0], units="C"))
        ],
    )
    temp_param = density.get_independent_parameter_by_name("Temperature")
    assert temp_param is not None
    assert temp_param.name == "Temperature"
    assert temp_param.values.value == [1.0]
    assert temp_param.values.unit == "C"
