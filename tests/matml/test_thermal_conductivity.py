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
XML_FILE_PATH = os.path.join(DIR_PATH, "..", "data", "MatML_unittest_thermal_conductivity.xml")


def test_read_thermal_conductivity_isotropic_material():
    material_dic = read_matml_file(XML_FILE_PATH)
    assert "Isotropic Convection Test Material" in material_dic.keys()
    assert len(material_dic["Isotropic Convection Test Material"].models) == 2
    isotropic_conductivity = material_dic["Isotropic Convection Test Material"].models[1]
    assert isotropic_conductivity.name == "Thermal Conductivity"
    assert isotropic_conductivity.model_qualifiers[0].name == "Behavior"
    assert isotropic_conductivity.model_qualifiers[0].value == "Isotropic"
    assert isotropic_conductivity.model_qualifiers[1].name == "Field Variable Compatible"
    assert isotropic_conductivity.model_qualifiers[1].value == "Temperature"
    assert isotropic_conductivity.thermal_conductivity == [10.0]
    assert isotropic_conductivity.independent_parameters[0].name == "Temperature"
    assert isotropic_conductivity.independent_parameters[0].values == [7.88860905221012e-31]
    assert isotropic_conductivity.independent_parameters[0].units == "C"
    assert isotropic_conductivity.independent_parameters[0].upper_limit == "Program Controlled"
    assert isotropic_conductivity.independent_parameters[0].lower_limit == "Program Controlled"
    assert isotropic_conductivity.independent_parameters[0].default_value == "22"


def test_read_thermal_conductivity_orthotropic_material():
    material_dic = read_matml_file(XML_FILE_PATH)
    assert "Orthotropic Convection Test Material" in material_dic.keys()
    assert len(material_dic["Orthotropic Convection Test Material"].models) == 2
    orthotropic_conductivity = material_dic["Orthotropic Convection Test Material"].models[1]
    assert orthotropic_conductivity.name == "Thermal Conductivity"
    assert orthotropic_conductivity.model_qualifiers[0].name == "Behavior"
    assert orthotropic_conductivity.model_qualifiers[0].value == "Orthotropic"
    assert orthotropic_conductivity.thermal_conductivity_x == [10.0]
    assert orthotropic_conductivity.thermal_conductivity_y == [15.0]
    assert orthotropic_conductivity.thermal_conductivity_z == [20.0]
    assert orthotropic_conductivity.independent_parameters[0].name == "Temperature"
    assert orthotropic_conductivity.independent_parameters[0].values == [7.88860905221012e-31]
