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
XML_FILE_PATH = os.path.join(DIR_PATH, "..", "data", "MatML_unittest_usermat.xml")


def test_read_usermat():
    material_dic = read_matml_file(XML_FILE_PATH)
    material_name = "usermat"
    assert material_name in material_dic.keys()
    assert len(material_dic[material_name].models) == 4
    usermat = material_dic[material_name].models[3]
    assert usermat.name == "Model Coefficients"
    assert usermat.model_qualifiers[0].name == "UserMat"
    assert usermat.model_qualifiers[0].value == "USER"
    assert usermat.model_qualifiers[1].name == "Custom Qualifier"
    assert usermat.model_qualifiers[1].value == "Custom Qualifier Value"
    assert usermat.material_property == "UserDefinedPropertySet"
    assert usermat.independent_parameters[0].name == "Temperature"
    assert usermat.independent_parameters[0].values == [7.88860905221012e-31]
    assert usermat.user_parameters[0].name == "y"
    assert usermat.user_parameters[0].values == [0.0]
    assert usermat.user_parameters[0].user_mat_constant == 1
    assert usermat.user_parameters[0].display == True


def test_variable_user_mat():
    material_dic = read_matml_file(XML_FILE_PATH)
    material_name = "variable usermat"
    assert material_name in material_dic.keys()
    assert len(material_dic[material_name].models) == 4
    usermat = material_dic[material_name].models[3]
    assert usermat.name == "Model Coefficients"
    assert usermat.model_qualifiers[0].name == "UserMat"
    assert usermat.model_qualifiers[0].value == "USER"
    assert usermat.material_property == "CustomPset"
    assert usermat.independent_parameters[0].name == "Temperature"
    assert usermat.independent_parameters[0].values == [10.0, 20.0]
    assert usermat.user_parameters[0].name == "alpha"
    assert usermat.user_parameters[0].values == [0.1, 0.4]
    assert usermat.user_parameters[0].user_mat_constant == 1
    assert usermat.user_parameters[0].display == True
    assert usermat.user_parameters[1].name == "beta"
    assert usermat.user_parameters[1].values == [0.2, 0.8]
    assert usermat.user_parameters[1].user_mat_constant == 2
    assert usermat.user_parameters[1].display == True
