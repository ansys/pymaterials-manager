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

import os

from ansys.mapdl.core import Mapdl
import pytest

from ansys.materials.manager._models._material_models.elasticity_isotropic import (
    ElasticityIsotropic,
)
from ansys.materials.manager._models._material_models.elasticity_orthotropic import (
    ElasticityOrthotropic,
)
from ansys.materials.manager.util.mapdl.mapdl_reader import read_mapdl

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
ELASTICITY_ISOTROPIC_CONSTANT = os.path.join(
    DIR_PATH, "..", "data", "mapdl_elasticity_isotropic_constant.cdb"
)
ELASTICITY_ORTHOTROPIC_CONSTANT = os.path.join(
    DIR_PATH, "..", "data", "mapdl_elasticity_orthotropic_constant.cdb"
)
ELASTICITY_ISOTROPIC_VARIABLE = os.path.join(
    DIR_PATH, "..", "data", "mapdl_elasticity_isotropic_variable.cdb"
)
ELASTICITY_ORTHOTROPIC_VARIABLE = os.path.join(
    DIR_PATH, "..", "data", "mapdl_elasticity_orthotropic_variable.cdb"
)
ELASTICITY_ORTHOTROPIC_VARIABLE_A11_A22 = os.path.join(
    DIR_PATH, "..", "data", "mapdl_elasticity_orthotropic_variable_a11_a22.cdb"
)

pytestmark = pytest.mark.mapdl_integration


@pytest.fixture
def mapdl():
    mapdl = Mapdl(ip="127.0.0.1", port="50052", local=False)
    mapdl.prep7()
    yield mapdl
    mapdl.mpdele("all", "all")


def test_constant_isotropic_elasticity_mapdl_read(mapdl):
    with open(ELASTICITY_ISOTROPIC_CONSTANT, "r") as file:
        data = file.read()
    mapdl.prep7()
    mapdl.input_strings(data)
    materials = read_mapdl(mapdl)
    material_name = "MATERIAL NUMBER 2"
    assert material_name in materials.keys()
    material = materials[material_name]
    assert isinstance(material.models[0], ElasticityIsotropic)
    assert material.models[0].youngs_modulus.value.tolist() == [1000000.0]
    assert material.models[0].poissons_ratio.value.tolist() == [0.3]
    assert material.models[0].independent_parameters == None


def test_constant_orthotropic_elasticity_mapdl_read(mapdl):
    with open(ELASTICITY_ORTHOTROPIC_CONSTANT, "r") as file:
        data = file.read()
    mapdl.prep7()
    mapdl.input_strings(data)
    materials = read_mapdl(mapdl)
    material_name = "MATERIAL NUMBER 1"
    assert material_name in materials.keys()
    material = materials[material_name]
    assert isinstance(material.models[0], ElasticityOrthotropic)
    assert material.models[0].youngs_modulus_x.value.tolist() == [1000000]
    assert material.models[0].youngs_modulus_y.value.tolist() == [1500000]
    assert material.models[0].youngs_modulus_z.value.tolist() == [2000000]
    assert material.models[0].shear_modulus_xy.value.tolist() == [1000000]
    assert material.models[0].shear_modulus_yz.value.tolist() == [3000000]
    assert material.models[0].shear_modulus_xz.value.tolist() == [2000000]
    assert material.models[0].poissons_ratio_xy.value.tolist() == [0.2]
    assert material.models[0].poissons_ratio_yz.value.tolist() == [0.4]
    assert material.models[0].poissons_ratio_xz.value.tolist() == [0.3]
    assert material.models[0].independent_parameters == None


def test_variable_temp_isotropic_elasticity_mapdl_read(mapdl):
    with open(ELASTICITY_ISOTROPIC_VARIABLE, "r") as file:
        data = file.read()
    mapdl.prep7()
    mapdl.input_strings(data)
    materials = read_mapdl(mapdl)
    material_name = "MATERIAL NUMBER 3"
    assert material_name in materials.keys()
    material = materials[material_name]
    assert isinstance(material.models[0], ElasticityIsotropic)
    assert material.models[0].youngs_modulus.value.tolist() == [2000000, 1000000]
    assert material.models[0].poissons_ratio.value.tolist() == [0.35, 0.3]
    assert material.models[0].independent_parameters[0].name == "Temperature"
    assert material.models[0].independent_parameters[0].values.value.tolist() == [12, 21]


def test_variable_temp_orthotropic_elasticity_mapdl_read(mapdl):
    with open(ELASTICITY_ORTHOTROPIC_VARIABLE, "r") as file:
        data = file.read()
    mapdl.prep7()
    mapdl.input_strings(data)
    materials = read_mapdl(mapdl)
    material_name = "MATERIAL NUMBER 1"
    assert material_name in materials.keys()
    material = materials[material_name]
    assert isinstance(material.models[0], ElasticityOrthotropic)
    assert material.models[0].youngs_modulus_x.value.tolist() == [1000000, 1100000, 1200000]
    assert material.models[0].youngs_modulus_y.value.tolist() == [1500000, 1600000, 1700000]
    assert material.models[0].youngs_modulus_z.value.tolist() == [2000000, 2200000, 2300000]
    assert material.models[0].shear_modulus_xy.value.tolist() == [1000000, 1100000, 1200000]
    assert material.models[0].shear_modulus_yz.value.tolist() == [3000000, 3100000, 3200000]
    assert material.models[0].shear_modulus_xz.value.tolist() == [2000000, 2100000, 2200000]
    assert material.models[0].poissons_ratio_xy.value.tolist() == [0.2, 0.21, 0.22]
    assert material.models[0].poissons_ratio_yz.value.tolist() == [0.4, 0.41, 0.42]
    assert material.models[0].poissons_ratio_xz.value.tolist() == [0.3, 0.31, 0.32]
    assert material.models[0].independent_parameters[0].name == "Temperature"
    assert material.models[0].independent_parameters[0].values.value.tolist() == [12, 21, 31]


def test_variable_a11_a22_orthotropic_elasticity_mapdl_read(mapdl):
    with open(ELASTICITY_ORTHOTROPIC_VARIABLE_A11_A22, "r") as file:
        data = file.read()
    mapdl.prep7()
    mapdl.input_strings(data)
    materials = read_mapdl(mapdl)
    material_name = "MATERIAL NUMBER 1"
    assert material_name in materials.keys()
    material = materials[material_name]
    assert isinstance(material.models[0], ElasticityOrthotropic)
    assert material.models[0].youngs_modulus_x.value.tolist() == [
        100.0,
        200.0,
        300.0,
        100.0,
        200.0,
        300.0,
        100.0,
        200.0,
        300.0,
    ]
    assert material.models[0].youngs_modulus_y.value.tolist() == [
        110.0,
        210.0,
        310.0,
        110.0,
        210.0,
        310.0,
        110.0,
        210.0,
        310.0,
    ]
    assert material.models[0].youngs_modulus_z.value.tolist() == [
        120.0,
        220.0,
        320.0,
        120.0,
        220.0,
        320.0,
        120.0,
        220.0,
        320.0,
    ]
    assert material.models[0].shear_modulus_xy.value.tolist() == [
        10.0,
        20.0,
        30.0,
        10.0,
        20.0,
        30.0,
        10.0,
        20.0,
        30.0,
    ]
    assert material.models[0].shear_modulus_yz.value.tolist() == [
        11.0,
        21.0,
        31.0,
        11.0,
        21.0,
        31.0,
        11.0,
        21.0,
        31.0,
    ]
    assert material.models[0].shear_modulus_xz.value.tolist() == [
        12.0,
        22.0,
        32.0,
        12.0,
        22.0,
        32.0,
        12.0,
        22.0,
        32.0,
    ]
    assert material.models[0].poissons_ratio_xy.value.tolist() == [
        0.1,
        0.2,
        0.3,
        0.1,
        0.2,
        0.3,
        0.1,
        0.2,
        0.3,
    ]
    assert material.models[0].poissons_ratio_yz.value.tolist() == [
        0.11,
        0.21,
        0.31,
        0.11,
        0.21,
        0.31,
        0.11,
        0.21,
        0.31,
    ]
    assert material.models[0].poissons_ratio_xz.value.tolist() == [
        0.12,
        0.22,
        0.32,
        0.12,
        0.22,
        0.32,
        0.12,
        0.22,
        0.32,
    ]
    assert material.models[0].independent_parameters[0].name == "UF01"
    assert material.models[0].independent_parameters[0].values.value.tolist() == [
        0.0,
        0.5,
        1.0,
        0.0,
        0.5,
        1.0,
        0.0,
        0.5,
        1.0,
    ]
    assert material.models[0].independent_parameters[1].name == "UF02"
    assert material.models[0].independent_parameters[1].values.value.tolist() == [
        0.0,
        0.0,
        0.0,
        0.5,
        0.5,
        0.5,
        1.0,
        1.0,
        1.0,
    ]
