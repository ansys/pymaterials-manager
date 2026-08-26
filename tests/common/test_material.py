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
)

SI = UnitSystem(system="SI")


# --- convert_to_unit_system ---


def test_convert_to_unit_system_density():
    material = Material(
        name="Steel",
        models=[Density(density=Quantity(value=[7.85], units="g cm^-3"))],
    )
    material.convert_to_unit_system(SI)
    density = material.get_model_by_name("Density").density
    assert math.isclose(density.value[0], 7850.0, rel_tol=1e-4)
    assert str(density.unit) == "kg m^-3"


def test_convert_to_unit_system_elasticity():
    material = Material(
        name="Aluminum",
        models=[ElasticityIsotropic(youngs_modulus=Quantity(value=[70.0], units="GPa"))],
    )
    material.convert_to_unit_system(SI)
    youngs = material.get_model_by_name("Elasticity").youngs_modulus
    assert math.isclose(youngs.value[0], 70.0e9, rel_tol=1e-4)
    # SI expands Pa to its base units
    assert str(youngs.unit) == "kg m^-1 s^-2"


def test_convert_to_unit_system_with_independent_parameter():
    material = Material(
        name="Steel",
        models=[
            Density(
                density=Quantity(value=[7.85, 7.80], units="g cm^-3"),
                independent_parameters=[
                    IndependentParameter(
                        name="Temperature", values=Quantity(value=[0.0, 100.0], units="C")
                    )
                ],
            )
        ],
    )
    material.convert_to_unit_system(SI)
    density_model = material.get_model_by_name("Density")
    assert math.isclose(density_model.density.value[0], 7850.0, rel_tol=1e-4)
    temp = density_model.independent_parameters[0].values
    assert math.isclose(temp.value[0], 273.15, rel_tol=1e-4)
    assert math.isclose(temp.value[1], 373.15, rel_tol=1e-4)


def test_convert_to_unit_system_all_models_converted():
    material = Material(
        name="Steel",
        models=[
            Density(density=Quantity(value=[7.85], units="g cm^-3")),
            ElasticityIsotropic(youngs_modulus=Quantity(value=[200.0], units="GPa")),
        ],
    )
    material.convert_to_unit_system(SI)
    assert math.isclose(
        material.get_model_by_name("Density").density.value[0], 7850.0, rel_tol=1e-4
    )
    assert math.isclose(
        material.get_model_by_name("Elasticity").youngs_modulus.value[0], 200.0e9, rel_tol=1e-4
    )


# --- append_models ---


def test_append_models_single_model():
    material = Material(name="Steel")
    material.append_models(Density(density=Quantity(value=[7.85], units="g cm^-3")))
    assert material.get_model_by_name("Density") is not None


def test_append_models_list():
    material = Material(name="Steel")
    material.append_models(
        [
            Density(density=Quantity(value=[7.85], units="g cm^-3")),
            ElasticityIsotropic(youngs_modulus=Quantity(value=[200.0], units="GPa")),
        ]
    )
    assert material.get_model_by_name("Density") is not None
    assert material.get_model_by_name("Elasticity") is not None


def test_append_models_raises_on_duplicate():
    material = Material(
        name="Steel",
        models=[Density(density=Quantity(value=[7.85], units="g cm^-3"))],
    )
    with pytest.raises(ValueError, match="repeated"):
        material.append_models(Density(density=Quantity(value=[8.0], units="g cm^-3")))


# --- get_model_by_name / remove_model_by_name ---


def test_get_model_by_name_case_insensitive():
    material = Material(
        name="Steel",
        models=[Density(density=Quantity(value=[7.85], units="g cm^-3"))],
    )
    assert material.get_model_by_name("density") is not None
    assert material.get_model_by_name("DENSITY") is not None


def test_get_model_by_name_returns_none_for_missing():
    material = Material(name="Steel")
    assert material.get_model_by_name("Density") is None


def test_remove_model_by_name():
    material = Material(
        name="Steel",
        models=[Density(density=Quantity(value=[7.85], units="g cm^-3"))],
    )
    material.remove_model_by_name("Density")
    assert material.get_model_by_name("Density") is None


def test_remove_model_by_name_noop_for_missing():
    material = Material(name="Steel")
    material.remove_model_by_name("Density")  # should not raise
