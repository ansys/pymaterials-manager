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
XML_FILE_PATH = os.path.join(DIR_PATH, "..", "data", "MatML_unittest_tsai_wu.xml")


def test_read_constant_tsai_wu():
    material_dic = read_matml_file(XML_FILE_PATH)
    assert "material with tsai-wu" in material_dic.keys()
    assert len(material_dic["material with tsai-wu"].models) == 2
    tsai_wu = material_dic["material with tsai-wu"].models[1]
    assert tsai_wu.name == "Tsai-Wu Constants"
    assert tsai_wu.coupling_coefficient_xy == [-1.0]
    assert tsai_wu.coupling_coefficient_xz == [-1.0]
    assert tsai_wu.coupling_coefficient_yz == [-1.0]
    assert tsai_wu.independent_parameters[0].name == "Temperature"
    assert tsai_wu.independent_parameters[0].values == [7.88860905221012e-31]


def test_read_variable_tsai_wu():
    material_dic = read_matml_file(XML_FILE_PATH)
    assert "material with variable tsai-wu" in material_dic.keys()
    assert len(material_dic["material with variable tsai-wu"].models) == 2
    tsai_wu = material_dic["material with variable tsai-wu"].models[1]
    assert tsai_wu.name == "Tsai-Wu Constants"
    assert tsai_wu.coupling_coefficient_xy == [-1.0, -1.0, -1.0]
    assert tsai_wu.coupling_coefficient_xz == [-1.0, -1.0, -1.0]
    assert tsai_wu.coupling_coefficient_yz == [-1.0, -1.0, -1.0]
    assert tsai_wu.independent_parameters[0].name == "Temperature"
    assert tsai_wu.independent_parameters[0].values == [22.0, 50.0, 70.0]
