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
XML_FILE_PATH = os.path.join(DIR_PATH, "..", "data", "MatML_unittest_viscosity.xml")


def test_read_constant_viscosity():
    material_dic = read_matml_file(XML_FILE_PATH)
    material_name = "material with viscosity"
    assert material_name in material_dic.keys()
    assert len(material_dic[material_name].models) == 2
    viscosity = material_dic[material_name].models[1]
    assert viscosity.name == "Viscosity"
    assert viscosity.model_qualifiers[0].name == "BETA"
    assert viscosity.model_qualifiers[0].value == "Mechanical.ModalAcoustics"
    assert viscosity.model_qualifiers[1].name == "Field Variable Compatible"
    assert viscosity.model_qualifiers[1].value == "Temperature"
    assert viscosity.viscosity == [1.0]
    assert viscosity.independent_parameters[0].name == "Temperature"
    assert viscosity.independent_parameters[0].field_variable == "Temperature"
    assert viscosity.independent_parameters[0].values == [7.88860905221012e-31]
    assert viscosity.independent_parameters[0].units == "C"
    assert viscosity.independent_parameters[0].upper_limit == "Program Controlled"
    assert viscosity.independent_parameters[0].lower_limit == "Program Controlled"
    assert viscosity.independent_parameters[0].default_value == "22"


def test_read_variable_viscosity():
    material_dic = read_matml_file(XML_FILE_PATH)
    material_name = "material with variable viscosity"
    assert material_name in material_dic.keys()
    assert len(material_dic[material_name].models) == 2
    viscosity = material_dic[material_name].models[1]
    assert viscosity.name == "Viscosity"
    assert viscosity.model_qualifiers[0].name == "BETA"
    assert viscosity.model_qualifiers[0].value == "Mechanical.ModalAcoustics"
    assert viscosity.model_qualifiers[1].name == "Field Variable Compatible"
    assert viscosity.model_qualifiers[1].value == "Temperature"
    assert viscosity.viscosity == [2.0, 3.0, 4.0]
    assert viscosity.independent_parameters[0].name == "Temperature"
    assert viscosity.independent_parameters[0].field_variable == "Temperature"
    assert viscosity.independent_parameters[0].values == [22.0, 50.0, 70.0]
    assert viscosity.independent_parameters[0].units == "C"
    assert viscosity.independent_parameters[0].upper_limit == "Program Controlled"
    assert viscosity.independent_parameters[0].lower_limit == "Program Controlled"
    assert viscosity.independent_parameters[0].default_value == "22"
