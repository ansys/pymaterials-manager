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

from ansys.materials.manager import MaterialManager
from ansys.materials.manager.models import (
    Density,
    ElasticityIsotropic,
    IndependentParameter,
    Material,
)

SI = UnitSystem(system="SI", preferred_units=["Pa", "N"])


@pytest.fixture
def manager_with_density():
    manager = MaterialManager()
    material = Material(
        name="Steel",
        models=[Density(density=Quantity(value=[7.85], units="g cm^-3"))],
    )
    manager.add_material(material)
    return manager


@pytest.fixture
def manager_with_density_and_temperature():
    manager = MaterialManager()
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
    manager.add_material(material)
    return manager


@pytest.fixture
def manager_with_elasticity():
    manager = MaterialManager()
    material = Material(
        name="Aluminum",
        models=[
            ElasticityIsotropic(
                youngs_modulus=Quantity(value=[70.0], units="GPa"),
                poissons_ratio=Quantity(value=[0.33], units=""),
            )
        ],
    )
    manager.add_material(material)
    return manager


def test_write_to_matml_density_converts_to_si(manager_with_density, tmp_path):
    out = tmp_path / "density.xml"
    manager_with_density.write_to_matml(out, unit_system=SI)

    reader = MaterialManager()
    reader.read_from_matml(out)
    density_model = reader.get_material("Steel").get_model_by_name("Density")
    assert math.isclose(density_model.density.value[0], 7850.0, rel_tol=1e-4)
    assert str(density_model.density.unit) == "kg m^-3"


def test_write_to_matml_density_preserves_values_without_unit_system(
    manager_with_density, tmp_path
):
    out = tmp_path / "density_no_us.xml"
    manager_with_density.write_to_matml(out)

    reader = MaterialManager()
    reader.read_from_matml(out)
    density_model = reader.get_material("Steel").get_model_by_name("Density")
    assert math.isclose(density_model.density.value[0], 7.85, rel_tol=1e-6)


def test_write_to_matml_converts_independent_parameter_to_si(
    manager_with_density_and_temperature, tmp_path
):
    out = tmp_path / "density_temp.xml"
    manager_with_density_and_temperature.write_to_matml(out, unit_system=SI)

    reader = MaterialManager()
    reader.read_from_matml(out)
    density_model = reader.get_material("Steel").get_model_by_name("Density")
    temp_param = density_model.independent_parameters[0]
    assert math.isclose(temp_param.values.value[0], 273.15, rel_tol=1e-4)
    assert math.isclose(temp_param.values.value[1], 373.15, rel_tol=1e-4)


def test_write_to_matml_elasticity_converts_to_si(manager_with_elasticity, tmp_path):
    out = tmp_path / "elasticity.xml"
    manager_with_elasticity.write_to_matml(out, unit_system=SI)

    reader = MaterialManager()
    reader.read_from_matml(out)
    elasticity_model = reader.get_material("Aluminum").get_model_by_name("Elasticity")
    assert math.isclose(elasticity_model.youngs_modulus.value[0], 70.0e9, rel_tol=1e-4)
    assert elasticity_model.youngs_modulus.unit == "Pa"


def test_write_to_matml_subset_of_materials(tmp_path):
    manager = MaterialManager()
    manager.add_material(
        Material(name="Mat1", models=[Density(density=Quantity(value=[1.0], units="g cm^-3"))])
    )
    manager.add_material(
        Material(name="Mat2", models=[Density(density=Quantity(value=[2.0], units="g cm^-3"))])
    )
    out = tmp_path / "subset.xml"
    manager.write_to_matml(out, material_names=["Mat1"], unit_system=SI)

    reader = MaterialManager()
    reader.read_from_matml(out)
    assert reader.get_material("Mat1") is not None
    density_model = reader.get_material("Mat1").get_model_by_name("Density")
    assert math.isclose(density_model.density.value[0], 1000.0, rel_tol=1e-4)


# --- set_unit_system tests ---


def test_set_unit_system_converts_existing_materials():
    manager = MaterialManager()
    manager.add_material(
        Material(name="Steel", models=[Density(density=Quantity(value=[7.85], units="g cm^-3"))])
    )
    manager.set_unit_system(SI)
    density_model = manager.get_material("Steel").get_model_by_name("Density")
    assert math.isclose(density_model.density.value[0], 7850.0, rel_tol=1e-4)
    assert str(density_model.density.unit) == "kg m^-3"


def test_set_unit_system_converts_all_materials():
    manager = MaterialManager()
    manager.add_material(
        Material(name="Mat1", models=[Density(density=Quantity(value=[1.0], units="g cm^-3"))])
    )
    manager.add_material(
        Material(name="Mat2", models=[Density(density=Quantity(value=[2.0], units="g cm^-3"))])
    )
    manager.set_unit_system(SI)
    for name, expected in [("Mat1", 1000.0), ("Mat2", 2000.0)]:
        density = manager.get_material(name).get_model_by_name("Density").density
        assert math.isclose(density.value[0], expected, rel_tol=1e-4)


def test_set_unit_system_converts_independent_parameters():
    manager = MaterialManager()
    manager.add_material(
        Material(
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
    )
    manager.set_unit_system(SI)
    density_model = manager.get_material("Steel").get_model_by_name("Density")
    temp_param = density_model.independent_parameters[0]
    assert math.isclose(temp_param.values.value[0], 273.15, rel_tol=1e-4)
    assert math.isclose(temp_param.values.value[1], 373.15, rel_tol=1e-4)


# --- add_material with unit_system tests ---


def test_add_material_auto_converts_when_unit_system_set():
    manager = MaterialManager(unit_system=SI)
    manager.add_material(
        Material(name="Steel", models=[Density(density=Quantity(value=[7.85], units="g cm^-3"))])
    )
    density_model = manager.get_material("Steel").get_model_by_name("Density")
    assert math.isclose(density_model.density.value[0], 7850.0, rel_tol=1e-4)
    assert str(density_model.density.unit) == "kg m^-3"


def test_add_material_no_conversion_without_unit_system():
    manager = MaterialManager()
    manager.add_material(
        Material(name="Steel", models=[Density(density=Quantity(value=[7.85], units="g cm^-3"))])
    )
    density_model = manager.get_material("Steel").get_model_by_name("Density")
    assert math.isclose(density_model.density.value[0], 7.85, rel_tol=1e-6)
    assert str(density_model.density.unit) == "g cm^-3"


def test_add_material_raises_if_already_present():
    manager = MaterialManager()
    manager.add_material(
        Material(name="Steel", models=[Density(density=Quantity(value=[7.85], units="g cm^-3"))])
    )
    with pytest.raises(Exception, match="already present"):
        manager.add_material(
            Material(
                name="Steel", models=[Density(density=Quantity(value=[7.85], units="g cm^-3"))]
            )
        )


# --- extend_material (add model) tests ---


def test_extend_material_auto_converts_when_unit_system_set():
    manager = MaterialManager(unit_system=SI)
    manager.add_material(Material(name="Aluminum"))
    manager.extend_material(
        "Aluminum",
        [ElasticityIsotropic(youngs_modulus=Quantity(value=[70.0], units="GPa"))],
    )
    elasticity = manager.get_material("Aluminum").get_model_by_name("Elasticity")
    assert math.isclose(elasticity.youngs_modulus.value[0], 70.0e9, rel_tol=1e-4)
    assert str(elasticity.youngs_modulus.unit) == "Pa"


def test_extend_material_no_conversion_without_unit_system():
    manager = MaterialManager()
    manager.add_material(Material(name="Aluminum"))
    manager.extend_material(
        "Aluminum",
        [ElasticityIsotropic(youngs_modulus=Quantity(value=[70.0], units="GPa"))],
    )
    elasticity = manager.get_material("Aluminum").get_model_by_name("Elasticity")
    assert math.isclose(elasticity.youngs_modulus.value[0], 70.0, rel_tol=1e-6)
    assert str(elasticity.youngs_modulus.unit) == "GPa"


def test_extend_material_does_nothing_for_unknown_material():
    manager = MaterialManager(unit_system=SI)
    # should not raise, just print a message
    manager.extend_material(
        "NonExistent", [Density(density=Quantity(value=[1.0], units="g cm^-3"))]
    )
