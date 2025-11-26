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

from ansys.materials.manager.parsers.matml.matml_reader import MatmlReader

DIR_PATH = Path(__file__).resolve().parent
XML_FILE_PATH = DIR_PATH.joinpath("..", "data", "matml_unittest_usermat.xml")


def test_read_usermat():
    matml_reader = MatmlReader(XML_FILE_PATH)
    materials = matml_reader.convert_matml_materials()
    material = materials["usermat"]
    assert len(material.models) == 3
    usermat = material.models[2]
    assert usermat.name == "Model Coefficients"
    assert usermat.model_qualifiers[0].name == "UserMat"
    assert usermat.model_qualifiers[0].value == "USER"
    assert usermat.model_qualifiers[1].name == "Custom Qualifier"
    assert usermat.model_qualifiers[1].value == "Custom Qualifier Value"
    assert usermat.independent_parameters[0].name == "Temperature"
    assert usermat.independent_parameters[0].values.value == [7.88860905221012e-31]
    assert usermat.independent_parameters[0].values.unit == "C"
    assert usermat.user_parameters[0].name == "y"
    assert usermat.user_parameters[0].values.value == [0.0]
    assert usermat.user_parameters[0].values.unit == ""
    assert usermat.user_parameters[0].user_mat_constant == 1


def test_variable_user_mat():
    matml_reader = MatmlReader(XML_FILE_PATH)
    materials = matml_reader.convert_matml_materials()
    material = materials["variable usermat"]
    assert len(material.models) == 3
    usermat = material.models[2]
    assert usermat.name == "Model Coefficients"
    assert usermat.model_qualifiers[0].name == "UserMat"
    assert usermat.model_qualifiers[0].value == "USER"
    assert usermat.independent_parameters[0].name == "Temperature"
    assert usermat.independent_parameters[0].values.value.tolist() == [10.0, 20.0]
    assert usermat.independent_parameters[0].values.unit == "C"
    assert usermat.user_parameters[0].name == "alpha"
    assert usermat.user_parameters[0].values.value.tolist() == [0.1, 0.4]
    assert usermat.user_parameters[0].values.unit == ""
    assert usermat.user_parameters[0].user_mat_constant == 1
    assert usermat.user_parameters[1].name == "beta"
    assert usermat.user_parameters[1].values.value.tolist() == [0.2, 0.8]
    assert usermat.user_parameters[0].values.unit == ""
    assert usermat.user_parameters[1].user_mat_constant == 2
