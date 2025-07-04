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

from utilities import get_material_and_metadata_from_xml, read_matml_file

from ansys.materials.manager._models._common.independent_parameter import IndependentParameter
from ansys.materials.manager._models._material_models.speed_of_sound import SpeedofSound
from ansys.materials.manager._models.material import Material
from ansys.materials.manager.util.matml.matml_from_material import MatmlWriter
from ansys.units import Quantity

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
XML_FILE_PATH = os.path.join(DIR_PATH, "..", "data", "MatML_unittest_speed_of_sound.xml")
SPEED_OF_SOUND = os.path.join(DIR_PATH, "..", "data", "speed_of_sound.txt")
SPEED_OF_SOUND_METADATA = os.path.join(DIR_PATH, "..", "data", "speed_of_sound_metadata.txt")
SPEED_OF_SOUND_VARIABLE = os.path.join(DIR_PATH, "..", "data", "speed_of_sound_variable.txt")

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
    assert speed_of_sound.independent_parameters[0].values.value == [7.88860905221012e-31]
    assert speed_of_sound.independent_parameters[0].values.unit == "C"
    assert speed_of_sound.independent_parameters[0].field_units == "C"
    assert speed_of_sound.independent_parameters[0].upper_limit == "Program Controlled"
    assert speed_of_sound.independent_parameters[0].lower_limit == "Program Controlled"
    assert speed_of_sound.independent_parameters[0].default_value == 22.0
    assert speed_of_sound.speed_of_sound.value == [100.0]
    assert speed_of_sound.speed_of_sound.unit == "m s^-1"


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
    assert speed_of_sound.independent_parameters[0].values.value.tolist() == [22.0, 40.0, 60.0]
    assert speed_of_sound.independent_parameters[0].values.unit == "C"
    assert speed_of_sound.independent_parameters[0].field_units == "C"
    assert speed_of_sound.independent_parameters[0].upper_limit == "Program Controlled"
    assert speed_of_sound.independent_parameters[0].lower_limit == "Program Controlled"
    assert speed_of_sound.independent_parameters[0].default_value == 22.0
    assert speed_of_sound.speed_of_sound.value.tolist() == [200.0, 300.0, 350.0]
    assert speed_of_sound.speed_of_sound.unit == "m s^-1"

def test_write_constant_speed_of_sound():
    materials = [
        Material(
            name="material with speed of sound",
            models=[
                SpeedofSound(
                    speed_of_sound=Quantity(value=[100.0], units="m s^-1"),
                    independent_parameters=[
                        IndependentParameter(
                            name="Temperature",
                            field_variable="Temperature",
                            values=Quantity(value=[7.88860905221012e-31], units="C"),
                            field_units="C",
                            default_value=22.0,
                            upper_limit="Program Controlled",
                            lower_limit="Program Controlled",
                        ),
                    ],
                ),
            ],
        )
    ]

    writer = MatmlWriter(materials)
    tree = writer._to_etree()
    material_string, metadata_string = get_material_and_metadata_from_xml(tree)
    with open(SPEED_OF_SOUND, 'r', encoding="utf8") as file:
        data = file.read()
        assert data == material_string
    with open(SPEED_OF_SOUND_METADATA, 'r') as file:
      data = file.read()
      assert data == metadata_string


def test_write_variable_speed_of_sound():
    materials = [
        Material(
            name="material with variable speed of sound",
            models=[
                SpeedofSound(
                    speed_of_sound=Quantity(value=[200.0, 300.0, 350.0], units="m s^-1"),
                    independent_parameters=[
                        IndependentParameter(
                            name="Temperature",
                            field_variable="Temperature",
                            values=Quantity(value=[22.0, 40.0, 60.0], units="C"),
                            field_units="C",
                            default_value=22.0,
                            upper_limit="Program Controlled",
                            lower_limit="Program Controlled",
                        ),
                    ],
                ),
            ],
        )
    ]

    writer = MatmlWriter(materials)
    tree = writer._to_etree()
    material_string, metadata_string = get_material_and_metadata_from_xml(tree)
    with open(SPEED_OF_SOUND_VARIABLE, 'r', encoding="utf8") as file:
        data = file.read()
        assert data == material_string
    with open(SPEED_OF_SOUND_METADATA, 'r') as file:
      data = file.read()
      assert data == metadata_string


