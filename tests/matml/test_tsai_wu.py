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
from ansys.materials.manager._models._material_models.tsai_wu_constants import TsaiWuConstants
from ansys.materials.manager._models.material import Material
from ansys.materials.manager.util.matml.matml_from_material import MatmlWriter

from ansys.units import Quantity

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
XML_FILE_PATH = os.path.join(DIR_PATH, "..", "data", "MatML_unittest_tsai_wu.xml")
TSAI_WU = os.path.join(DIR_PATH, "..", "data", "tsai_wu.txt")
TSAI_WU_METADATA = os.path.join(DIR_PATH, "..", "data", "tsai_wu_metadata.txt")
TSAI_WU_VARIABLE = os.path.join(DIR_PATH, "..", "data", "tsai_wu_variable.txt")


def test_read_constant_tsai_wu():
    material_dic = read_matml_file(XML_FILE_PATH)
    assert "material with tsai-wu" in material_dic.keys()
    assert len(material_dic["material with tsai-wu"].models) == 2
    tsai_wu = material_dic["material with tsai-wu"].models[1]
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
    material_dic = read_matml_file(XML_FILE_PATH)
    assert "material with variable tsai-wu" in material_dic.keys()
    assert len(material_dic["material with variable tsai-wu"].models) == 2
    tsai_wu = material_dic["material with variable tsai-wu"].models[1]
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

def test_write_constant_tsai_wu():
    materials = [
        Material(
            name="material with tsai-wu",
            models=[
                TsaiWuConstants(
                    coupling_coefficient_xy=Quantity(value=[-1.0], unit=""),
                    coupling_coefficient_xz=Quantity(value=[-1.0], unit=""),
                    coupling_coefficient_yz=Quantity(value=[-1.0], unit=""),
                    independent_parameters=[
                        IndependentParameter(
                            name="Temperature",
                            field_variable="Temperature",
                            values=Quantity(value=[7.88860905221012e-31], unit="C"),
                        ),
                    ],
                ),
            ],
        )
    ]

    writer = MatmlWriter(materials)
    tree = writer._to_etree()
    material_string, metadata_string = get_material_and_metadata_from_xml(tree)
    with open(TSAI_WU, 'r') as file:
        data = file.read()
        assert data == material_string
    with open(TSAI_WU_METADATA, 'r') as file:
      data = file.read()
      assert data == metadata_string


def test_write_variable_tsai_wu():
    materials = [
        Material(
            name="material with variable tsai-wu",
            models=[
                TsaiWuConstants(
                    coupling_coefficient_xy=Quantity(value=[-1.0, -1.0, -1.0], unit=""),
                    coupling_coefficient_xz=Quantity(value=[-1.0, -1.0, -1.0], unit=""),
                    coupling_coefficient_yz=Quantity(value=[-1.0, -1.0, -1.0], unit=""),
                    independent_parameters=[
                        IndependentParameter(
                            name="Temperature",
                            field_variable="Temperature",
                            values=Quantity(value=[22.0, 50.0, 70.0], unit="C"),
                        ),
                    ],
                ),
            ],
        )
    ]

    writer = MatmlWriter(materials)
    tree = writer._to_etree()
    material_string, metadata_string = get_material_and_metadata_from_xml(tree)
    with open(TSAI_WU_VARIABLE, 'r') as file:
        data = file.read()
        assert data == material_string
    with open(TSAI_WU_METADATA, 'r') as file:
      data = file.read()
      assert data == metadata_string
