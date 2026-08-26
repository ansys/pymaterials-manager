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

import math

from ansys.units import Quantity, UnitSystem
import pytest

from ansys.materials.manager.models import (
    Density,
    ElasticityIsotropic,
    IndependentParameter,
    Material,
    TabularQuantity,
)


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


SI = UnitSystem(system="SI")


def test_convert_density_to_si():
    density = Density(density=Quantity(value=[1.0], units="g cm^-3"))
    density.convert_to_unit_system(SI)
    assert math.isclose(density.density.value[0], 1000.0, rel_tol=1e-6)


def test_convert_density_multiple_values_to_si():
    density = Density(density=Quantity(value=[1.0, 2.0, 3.0], units="g cm^-3"))
    density.convert_to_unit_system(SI)
    assert math.isclose(density.density.value[0], 1000.0, rel_tol=1e-6)
    assert math.isclose(density.density.value[1], 2000.0, rel_tol=1e-6)
    assert math.isclose(density.density.value[2], 3000.0, rel_tol=1e-6)


def test_convert_density_independent_parameter_to_si():
    density = Density(
        density=Quantity(value=[1.0, 2.0], units="g cm^-3"),
        independent_parameters=[
            IndependentParameter(name="Temperature", values=Quantity(value=[0.0, 100.0], units="C"))
        ],
    )
    density.convert_to_unit_system(SI)
    assert math.isclose(density.density.value[0], 1000.0, rel_tol=1e-6)
    assert math.isclose(density.density.value[1], 2000.0, rel_tol=1e-6)
    assert math.isclose(density.independent_parameters[0].values.value[0], 273.15, rel_tol=1e-6)
    assert math.isclose(density.independent_parameters[0].values.value[1], 373.15, rel_tol=1e-6)


def test_convert_elasticity_youngs_modulus_to_si():
    elasticity = ElasticityIsotropic(
        youngs_modulus=Quantity(value=[1.0], units="MPa"),
        poissons_ratio=Quantity(value=[0.3], units=""),
    )
    elasticity.convert_to_unit_system(SI)
    assert math.isclose(elasticity.youngs_modulus.value[0], 1e6, rel_tol=1e-6)


def test_convert_material_delegates_to_models():
    material = Material(
        name="Test",
        models=[Density(density=Quantity(value=[1.0], units="g cm^-3"))],
    )
    material.convert_to_unit_system(SI)
    density_model = material.get_model_by_name("Density")
    assert math.isclose(density_model.density.value[0], 1000.0, rel_tol=1e-6)


def test_convert_preserves_unit_system_in_unit_string():
    density = Density(density=Quantity(value=[1.0], units="g cm^-3"))
    original_unit = density.density.unit
    density.convert_to_unit_system(SI)
    assert density.density.unit != original_unit
