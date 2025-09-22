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

from ansys.materials.manager._models._material_models.density import Density
from ansys.materials.manager._models._material_models.elasticity_orthotropic import (
    ElasticityOrthotropic,
)
from ansys.materials.manager.util.mapdl.mapdl_reader import read_mapdl

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
ELASTICITY_ORTHOTROPIC_VARIABLE = os.path.join(
    DIR_PATH, "..", "data", "mapdl_elasticity_orthotropic_variable.cdb"
)
VARIABLE_DENSITY_TEMP = os.path.join(DIR_PATH, "..", "data", "mapdl_density_variable_1.cdb")

pytestmark = pytest.mark.mapdl_integration


@pytest.fixture(scope="module")
def mapdl():
    mapdl = Mapdl(ip="127.0.0.1", port="50052", local=False)
    mapdl.prep7()
    yield mapdl
    mapdl.mpdele("all", "all")


def test_density_orthotropic_elasticity_variable_mapdl_read(mapdl):
    mapdl.mpdele("all", "all")
    with open(VARIABLE_DENSITY_TEMP, "r") as file:
        data = file.read()
    mapdl.input_strings(data)
    with open(ELASTICITY_ORTHOTROPIC_VARIABLE, "r") as file:
        data = file.read()
    mapdl.input_strings(data)
    materials = read_mapdl(mapdl)
    material_name = "MATERIAL NUMBER 1"
    assert material_name in materials.keys()
    material = materials[material_name]
    assert isinstance(material.models[0], Density)
    assert material.models[0].density.value.tolist() == [1.34, 2.25]
    assert material.models[0].independent_parameters[0].name == "Temperature"
    assert material.models[0].independent_parameters[0].values.value.tolist() == [22.0, 40.0]
    assert isinstance(material.models[1], ElasticityOrthotropic)
    assert material.models[1].youngs_modulus_x.value.tolist() == [1000000, 1100000, 1200000]
    assert material.models[1].youngs_modulus_y.value.tolist() == [1500000, 1600000, 1700000]
    assert material.models[1].youngs_modulus_z.value.tolist() == [2000000, 2200000, 2300000]
    assert material.models[1].shear_modulus_xy.value.tolist() == [1000000, 1100000, 1200000]
    assert material.models[1].shear_modulus_yz.value.tolist() == [3000000, 3100000, 3200000]
    assert material.models[1].shear_modulus_xz.value.tolist() == [2000000, 2100000, 2200000]
    assert material.models[1].poissons_ratio_xy.value.tolist() == [0.2, 0.21, 0.22]
    assert material.models[1].poissons_ratio_yz.value.tolist() == [0.4, 0.41, 0.42]
    assert material.models[1].poissons_ratio_xz.value.tolist() == [0.3, 0.31, 0.32]
    assert material.models[1].independent_parameters[0].name == "Temperature"
    assert material.models[1].independent_parameters[0].values.value.tolist() == [12, 21, 31]
