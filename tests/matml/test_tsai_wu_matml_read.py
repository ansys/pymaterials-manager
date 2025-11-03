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

from ansys.materials.manager.util.visitors.matml_reader import MatmlReader

DIR_PATH = Path(__file__).resolve().parent
XML_FILE_PATH = DIR_PATH.joinpath("..", "data", "matml_unittest_tsai_wu.xml")


def test_read_constant_tsai_wu():
    matml_reader = MatmlReader(XML_FILE_PATH)
    materials = matml_reader.convert_matml_materials()
    material = materials["material with tsai-wu"]
    assert len(material.models) == 1
    tsai_wu = material.models[0]
    assert tsai_wu.name == "Tsai-Wu Constants"
    assert tsai_wu.coupling_coefficient_xy.value == [-1.0]
    assert tsai_wu.coupling_coefficient_xy.unit == ""
    assert tsai_wu.coupling_coefficient_xz.value == [-1.0]
    assert tsai_wu.coupling_coefficient_xz.unit == ""
    assert tsai_wu.coupling_coefficient_yz.value == [-1.0]
    assert tsai_wu.coupling_coefficient_yz.unit == ""
    assert tsai_wu.independent_parameters[0].name == "Temperature"
    assert tsai_wu.independent_parameters[0].values.value == [7.88860905221012e-31]
    assert tsai_wu.independent_parameters[0].values.unit == "C"


def test_read_variable_tsai_wu():
    matml_reader = MatmlReader(XML_FILE_PATH)
    materials = matml_reader.convert_matml_materials()
    material = materials["material with variable tsai-wu"]
    assert len(material.models) == 1
    tsai_wu = material.models[0]
    assert tsai_wu.name == "Tsai-Wu Constants"
    assert tsai_wu.coupling_coefficient_xy.value.tolist() == [-1.0, -1.0, -1.0]
    assert tsai_wu.coupling_coefficient_xy.unit == ""
    assert tsai_wu.coupling_coefficient_xz.value.tolist() == [-1.0, -1.0, -1.0]
    assert tsai_wu.coupling_coefficient_xz.unit == ""
    assert tsai_wu.coupling_coefficient_yz.value.tolist() == [-1.0, -1.0, -1.0]
    assert tsai_wu.coupling_coefficient_yz.unit == ""
    assert tsai_wu.independent_parameters[0].name == "Temperature"
    assert tsai_wu.independent_parameters[0].values.value.tolist() == [22.0, 50.0, 70.0]
    assert tsai_wu.independent_parameters[0].values.unit == "C"
