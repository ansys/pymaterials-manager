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

from tests.matml.utilities import read_matml_file

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
XML_FILE_PATH = os.path.join(DIR_PATH, "..", "data", "MatML_unittest_density.xml")


def test_read_material_with_constant_density():
    material_dic = read_matml_file(XML_FILE_PATH)
    assert "material with density" in material_dic.keys()
    constant_density_material = material_dic["material with density"]
    assert len(constant_density_material.models) == 1
    assert constant_density_material.models[0].name == "Density"
    assert constant_density_material.models[0].density == [1.34]
    assert len(constant_density_material.models[0].independent_parameters) == 1
    assert constant_density_material.models[0].independent_parameters[0].name == "Temperature"
    assert constant_density_material.models[0].independent_parameters[0].values == [
        7.88860905221012e-31
    ]


def test_read_model_with_variable_density():
    material_dic = read_matml_file(XML_FILE_PATH)
    assert "material with variable density" in material_dic.keys()
    variable_density_material = material_dic["material with variable density"]
    assert len(variable_density_material.models) == 1
    assert variable_density_material.models[0].name == "Density"
    assert variable_density_material.models[0].density == [12.0, 32.0, 38.0]
    assert len(variable_density_material.models[0].independent_parameters) == 1
    assert variable_density_material.models[0].independent_parameters[0].name == "Temperature"
    assert variable_density_material.models[0].independent_parameters[0].values == [
        20.0,
        21.0,
        23.0,
    ]
