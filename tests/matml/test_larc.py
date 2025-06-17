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

from utilities import read_matml_file

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
XML_FILE_PATH = os.path.join(DIR_PATH, "..", "data", "MatML_unittest_larc.xml")


def test_read_constant_larc():
    material_dic = read_matml_file(XML_FILE_PATH)
    material_name = "material with larc"
    assert material_name in material_dic.keys()
    assert len(material_dic[material_name].models) == 2
    larc = material_dic[material_name].models[1]
    assert larc.name == "LaRc03/04 Constants"
    assert larc.fracture_toughness_ratio == [1.0]
    assert larc.longitudinal_friction_coefficient == [2.0]
    assert larc.transverse_friction_coefficient == [3.0]
    assert larc.fracture_angle_under_compression == [4.0]
    assert larc.independent_parameters[0].name == "Temperature"
    assert larc.independent_parameters[0].values == [7.88860905221012e-31]


def test_read_variable_larc():
    material_dic = read_matml_file(XML_FILE_PATH)
    material_name = "material with variable larc"
    assert material_name in material_dic.keys()
    assert len(material_dic[material_name].models) == 2
    larc = material_dic[material_name].models[1]
    assert larc.name == "LaRc03/04 Constants"
    assert larc.fracture_toughness_ratio == [5.0, 9.0, 13.0]
    assert larc.longitudinal_friction_coefficient == [6.0, 10.0, 14.0]
    assert larc.transverse_friction_coefficient == [7.0, 11.0, 15.0]
    assert larc.fracture_angle_under_compression == [8.0, 12.0, 16.0]
    assert larc.independent_parameters[0].name == "Temperature"
    assert larc.independent_parameters[0].values == [22.0, 50.0, 70.0]
