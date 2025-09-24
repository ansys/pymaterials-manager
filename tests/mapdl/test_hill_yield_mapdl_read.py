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

from ansys.materials.manager._models._material_models.hill_yield_criterion import HillYieldCriterion
from ansys.materials.manager.util.mapdl.mapdl_reader import read_mapdl

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
HILL_VARIABLE_A11_A22 = os.path.join(DIR_PATH, "..", "data", "mapdl_hill_variable_a11_a22.cdb")

pytestmark = pytest.mark.mapdl_integration


@pytest.fixture(scope="module")
def mapdl():
    mapdl = Mapdl(ip="127.0.0.1", port="50052", local=False)
    mapdl.prep7()
    yield mapdl
    mapdl.mpdele("all", "all")


def test_variable_a11_a22_hill_yield_mapdl_read(mapdl):
    with open(HILL_VARIABLE_A11_A22, "r") as file:
        data = file.read()
    mapdl.prep7()
    mapdl.input_strings(data)
    materials = read_mapdl(mapdl)
    print(materials)
    material_name = "MATERIAL NUMBER 2"
    assert material_name in materials.keys()
    material = materials[material_name]
    assert isinstance(material.models[0], HillYieldCriterion)
    assert material.models[0].yield_stress_ratio_x.value.tolist() == [
        1.0,
        1.3871793,
        3.0072199,
        1.2181891,
        1.0,
        1.3871793,
        1.0,
    ]
    assert material.models[0].yield_stress_ratio_y.value.tolist() == [
        1.0,
        1.0,
        1.0,
        1.2181891,
        1.3871793,
        1.3871793,
        3.0072199,
    ]
    assert material.models[0].yield_stress_ratio_z.value.tolist() == [
        3.0072199,
        1.3871793,
        1.0,
        1.2181891,
        1.3871793,
        1.0,
        1.0,
    ]
    assert material.models[0].yield_stress_ratio_xy.value.tolist() == [
        1.2758386,
        1.2758386,
        1.2758386,
        1.2758386,
        1.2758386,
        1.2758386,
        1.2758386,
    ]
    assert material.models[0].yield_stress_ratio_yz.value.tolist() == [
        1.2758386,
        1.2758386,
        1.2758386,
        1.2758386,
        1.2758386,
        1.2758386,
        1.2758386,
    ]
    assert material.models[0].yield_stress_ratio_xz.value.tolist() == [
        1.2758386,
        1.2758386,
        1.2758386,
        1.2758386,
        1.2758386,
        1.2758386,
        1.2758386,
    ]
    assert material.models[0].independent_parameters[0].name == "UF01"
    assert material.models[0].independent_parameters[0].values.value.tolist() == [
        0.0,
        0.5,
        1.0,
        0.33333333,
        0.0,
        0.5,
        0.0,
    ]
    assert material.models[0].independent_parameters[1].name == "UF02"
    assert material.models[0].independent_parameters[1].values.value.tolist() == [
        0.0,
        0.0,
        0.0,
        0.33333333,
        0.5,
        0.5,
        1.0,
    ]
