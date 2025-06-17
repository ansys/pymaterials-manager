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
XML_FILE_PATH = os.path.join(DIR_PATH, "..", "data", "MatML_unittest_strain_limit.xml")


def test_read_constant_strain_limit_isotropic():
    material_dic = read_matml_file(XML_FILE_PATH)
    assert "isotropic material with strain limit" in material_dic.keys()
    assert len(material_dic["isotropic material with strain limit"].models) == 2
    orthotropic_strain_limits = material_dic["isotropic material with strain limit"].models[1]
    assert orthotropic_strain_limits.name == "Strain Limits"
    assert orthotropic_strain_limits.model_qualifiers[0].name == "Behavior"
    assert orthotropic_strain_limits.model_qualifiers[0].value == "Isotropic"
    assert orthotropic_strain_limits.von_mises == [213]
    assert orthotropic_strain_limits.independent_parameters[0].name == "Temperature"
    assert orthotropic_strain_limits.independent_parameters[0].values == [7.88860905221012e-31]


def test_read_variable_strain_limit_isotropic():
    material_dic = read_matml_file(XML_FILE_PATH)
    assert "isotropic material with variable strain limit" in material_dic.keys()
    assert len(material_dic["isotropic material with variable strain limit"].models) == 2
    orthotropic_strain_limits = material_dic[
        "isotropic material with variable strain limit"
    ].models[1]
    assert orthotropic_strain_limits.name == "Strain Limits"
    assert orthotropic_strain_limits.model_qualifiers[0].name == "Behavior"
    assert orthotropic_strain_limits.model_qualifiers[0].value == "Isotropic"
    assert orthotropic_strain_limits.von_mises == [2333, 2324, 2432]
    assert orthotropic_strain_limits.independent_parameters[0].name == "Temperature"
    assert orthotropic_strain_limits.independent_parameters[0].values == [23, 25, 27]


def test_read_constant_strain_limit_orthotropic():
    material_dic = read_matml_file(XML_FILE_PATH)
    assert "orthotropic material with strain limit" in material_dic.keys()
    assert len(material_dic["orthotropic material with strain limit"].models) == 2
    orthotropic_strain_limits = material_dic["orthotropic material with strain limit"].models[1]
    assert orthotropic_strain_limits.name == "Strain Limits"
    assert orthotropic_strain_limits.model_qualifiers[0].name == "Behavior"
    assert orthotropic_strain_limits.model_qualifiers[0].value == "Orthotropic"
    assert orthotropic_strain_limits.model_qualifiers[1].name == "Field Variable Compatible"
    assert orthotropic_strain_limits.model_qualifiers[1].value == "Temperature"
    assert orthotropic_strain_limits.interpolation_options.algorithm_type == "Linear Multivariate"
    assert orthotropic_strain_limits.interpolation_options.cached == True
    assert orthotropic_strain_limits.interpolation_options.normalized == True
    assert orthotropic_strain_limits.tensile_x_direction == [311.0]
    assert orthotropic_strain_limits.tensile_y_direction == [213.0]
    assert orthotropic_strain_limits.tensile_z_direction == [13.0]
    assert orthotropic_strain_limits.compressive_x_direction == [-132.0]
    assert orthotropic_strain_limits.compressive_y_direction == [-13.0]
    assert orthotropic_strain_limits.compressive_z_direction == [-13.0]
    assert orthotropic_strain_limits.shear_xy == [24.0]
    assert orthotropic_strain_limits.shear_xz == [12.0]
    assert orthotropic_strain_limits.shear_yz == [232.0]
    assert orthotropic_strain_limits.independent_parameters[0].name == "Temperature"
    assert orthotropic_strain_limits.independent_parameters[0].values == [7.88860905221012e-31]
    assert orthotropic_strain_limits.independent_parameters[0].units == "C"
    assert orthotropic_strain_limits.independent_parameters[0].upper_limit == "Program Controlled"
    assert orthotropic_strain_limits.independent_parameters[0].lower_limit == "Program Controlled"
    assert orthotropic_strain_limits.independent_parameters[0].default_value == "22"


def test_read_variable_strain_limit_orthotropic():
    material_dic = read_matml_file(XML_FILE_PATH)
    assert "orthotropic material with variable strain limit" in material_dic.keys()
    assert len(material_dic["orthotropic material with variable strain limit"].models) == 2
    orthotropic_strain_limits = material_dic[
        "orthotropic material with variable strain limit"
    ].models[1]
    assert orthotropic_strain_limits.name == "Strain Limits"
    assert orthotropic_strain_limits.model_qualifiers[0].name == "Behavior"
    assert orthotropic_strain_limits.model_qualifiers[0].value == "Orthotropic"
    assert orthotropic_strain_limits.model_qualifiers[1].name == "Field Variable Compatible"
    assert orthotropic_strain_limits.model_qualifiers[1].value == "Temperature"
    assert orthotropic_strain_limits.interpolation_options.algorithm_type == "Linear Multivariate"
    assert orthotropic_strain_limits.interpolation_options.cached == True
    assert orthotropic_strain_limits.interpolation_options.normalized == True
    assert orthotropic_strain_limits.tensile_x_direction == [324.0, 311.0, 312.0]
    assert orthotropic_strain_limits.tensile_y_direction == [236.0, 213.0, 234.0]
    assert orthotropic_strain_limits.tensile_z_direction == [15.0, 13.0, 14.0]
    assert orthotropic_strain_limits.compressive_x_direction == [-110.0, -132.0, -120.0]
    assert orthotropic_strain_limits.compressive_y_direction == [-11.0, -13.0, -12.0]
    assert orthotropic_strain_limits.compressive_z_direction == [-9.0, -13.0, -11.0]
    assert orthotropic_strain_limits.shear_xy == [26.0, 24.0, 25.0]
    assert orthotropic_strain_limits.shear_xz == [16.0, 12.0, 14.0]
    assert orthotropic_strain_limits.shear_yz == [255.0, 232.0, 244.0]
    assert orthotropic_strain_limits.independent_parameters[0].name == "Temperature"
    assert orthotropic_strain_limits.independent_parameters[0].values == [13.0, 21.0, 23.0]
    assert orthotropic_strain_limits.independent_parameters[0].units == "C"
    assert orthotropic_strain_limits.independent_parameters[0].upper_limit == "Program Controlled"
    assert orthotropic_strain_limits.independent_parameters[0].lower_limit == "Program Controlled"
    assert orthotropic_strain_limits.independent_parameters[0].default_value == "22"
