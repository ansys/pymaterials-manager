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
XML_FILE_PATH = os.path.join(DIR_PATH, "..", "data", "MatML_unittest_speed_of_sound.xml")


def test_read_constant_speed_of_sound():
    material_dic = read_matml_file(XML_FILE_PATH)
    material_name = "material with speed of sound"
    assert material_name in material_dic.keys()
    assert len(material_dic[material_name].models) == 2
    speed_of_sound = material_dic[material_name].models[1]
    assert speed_of_sound.name == "Speed of Sound"
    assert speed_of_sound.model_qualifiers[0].name == "BETA"
    assert speed_of_sound.model_qualifiers[0].value == "Mechanical.ModalAcoustics"
    assert speed_of_sound.model_qualifiers[1].name == "Field Variable Compatible"
    assert speed_of_sound.model_qualifiers[1].value == "Temperature"
    assert speed_of_sound.independent_parameters[0].name == "Temperature"
    assert speed_of_sound.independent_parameters[0].field_variable == "Temperature"
    assert speed_of_sound.independent_parameters[0].values == [7.88860905221012e-31]
    assert speed_of_sound.independent_parameters[0].units == "C"
    assert speed_of_sound.independent_parameters[0].upper_limit == "Program Controlled"
    assert speed_of_sound.independent_parameters[0].lower_limit == "Program Controlled"
    assert speed_of_sound.independent_parameters[0].default_value == "22"
    assert speed_of_sound.speed_of_sound == [100.0]


def test_read_variable_speed_of_sound():
    material_dic = read_matml_file(XML_FILE_PATH)
    material_name = "material with variable speed of sound"
    assert material_name in material_dic.keys()
    assert len(material_dic[material_name].models) == 2
    speed_of_sound = material_dic[material_name].models[1]
    assert speed_of_sound.name == "Speed of Sound"
    assert speed_of_sound.model_qualifiers[0].name == "BETA"
    assert speed_of_sound.model_qualifiers[0].value == "Mechanical.ModalAcoustics"
    assert speed_of_sound.model_qualifiers[1].name == "Field Variable Compatible"
    assert speed_of_sound.model_qualifiers[1].value == "Temperature"
    assert speed_of_sound.independent_parameters[0].name == "Temperature"
    assert speed_of_sound.independent_parameters[0].field_variable == "Temperature"
    assert speed_of_sound.independent_parameters[0].values == [22.0, 40.0, 60.0]
    assert speed_of_sound.independent_parameters[0].units == "C"
    assert speed_of_sound.independent_parameters[0].upper_limit == "Program Controlled"
    assert speed_of_sound.independent_parameters[0].lower_limit == "Program Controlled"
    assert speed_of_sound.independent_parameters[0].default_value == "22"
    assert speed_of_sound.speed_of_sound == [200.0, 300.0, 350.0]
