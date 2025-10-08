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

from pathlib import Path

from ansys.mapdl.core import Mapdl
import pytest

from ansys.materials.manager._models._material_models.density import Density
from ansys.materials.manager.util.mapdl.mapdl_reader import read_mapdl

DIR_PATH = Path(__file__).resolve().parent
CONSTANT_DENSITY = DIR_PATH.joinpath("..", "data", "mapdl_density_constant.cdb")
VARIABLE_DENSITY_TEMP = DIR_PATH.joinpath("..", "data", "mapdl_density_variable_1.cdb")

pytestmark = pytest.mark.mapdl_integration


@pytest.fixture(scope="module")
def mapdl():
    mapdl = Mapdl(ip="127.0.0.1", port="50052", local=False)
    mapdl.prep7()
    yield mapdl
    mapdl.mpdele("all", "all")


def test_constant_density_mapdl_read(mapdl):
    with open(CONSTANT_DENSITY, "r") as file:
        data = file.read()
    mapdl.input_strings(data)
    materials = read_mapdl(mapdl)
    material_name = "MATERIAL NUMBER 1"
    assert material_name in materials.keys()
    material = materials[material_name]
    assert isinstance(material.models[0], Density)
    assert material.models[0].density.value.tolist() == [1.34]
    assert material.models[0].independent_parameters == None


def test_variable_density_mapdl_read(mapdl):
    with open(VARIABLE_DENSITY_TEMP, "r") as file:
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
