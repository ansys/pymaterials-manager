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
XML_FILE_PATH = DIR_PATH.joinpath("..", "data", "matml_unittest_larc.xml")


def test_read_constant_larc():
    matml_reader = MatmlReader(XML_FILE_PATH)
    materials = matml_reader.convert_matml_materials()
    material = materials["material with larc"]
    assert len(material.models) == 1
    larc = material.models[0]
    assert larc.name == "LaRc03/04 Constants"
    assert larc.fracture_toughness_ratio.value == [1.0]
    assert larc.fracture_toughness_ratio.unit == ""
    assert larc.longitudinal_friction_coefficient.value == [2.0]
    assert larc.longitudinal_friction_coefficient.unit == ""
    assert larc.transverse_friction_coefficient.value == [3.0]
    assert larc.transverse_friction_coefficient.unit == ""
    assert larc.fracture_angle_under_compression.value == [4.0]
    assert larc.fracture_angle_under_compression.unit == ""
    assert larc.independent_parameters[0].name == "Temperature"
    assert larc.independent_parameters[0].values.value == [7.88860905221012e-31]
    assert larc.independent_parameters[0].values.unit == "C"


def test_read_variable_larc():
    matml_reader = MatmlReader(XML_FILE_PATH)
    materials = matml_reader.convert_matml_materials()
    material = materials["material with variable larc"]
    assert len(material.models) == 1
    larc = material.models[0]
    assert larc.name == "LaRc03/04 Constants"
    assert larc.fracture_toughness_ratio.value.tolist() == [5.0, 9.0, 13.0]
    assert larc.fracture_toughness_ratio.unit == ""
    assert larc.longitudinal_friction_coefficient.value.tolist() == [6.0, 10.0, 14.0]
    assert larc.longitudinal_friction_coefficient.unit == ""
    assert larc.transverse_friction_coefficient.value.tolist() == [7.0, 11.0, 15.0]
    assert larc.transverse_friction_coefficient.unit == ""
    assert larc.fracture_angle_under_compression.value.tolist() == [8.0, 12.0, 16.0]
    assert larc.fracture_angle_under_compression.unit == ""
    assert larc.independent_parameters[0].name == "Temperature"
    assert larc.independent_parameters[0].values.value.tolist() == [22.0, 50.0, 70.0]
    assert larc.independent_parameters[0].values.unit == "C"
