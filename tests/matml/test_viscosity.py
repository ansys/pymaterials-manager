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
from ansys.materials.manager._models._material_models.viscosity import Viscosity
from ansys.materials.manager._models.material import Material
from ansys.materials.manager.util.matml.matml_from_material import MatmlWriter

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
XML_FILE_PATH = os.path.join(DIR_PATH, "..", "data", "MatML_unittest_viscosity.xml")

VISCOSITY = """<?xml version="1.0" ?>
<Material>
  <BulkDetails>
    <Name>material with viscosity</Name>
    <PropertyData property="pr0">
      <Data format="string">-</Data>
      <Qualifier name="BETA">Mechanical.ModalAcoustics</Qualifier>
      <ParameterValue parameter="pa0" format="float">
        <Data>1.0</Data>
        <Qualifier name="Variable Type">Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa1" format="float">
        <Data>22.0, 50.0, 70.0</Data>
        <Qualifier name="Variable Type">Independent,Independent,Independent</Qualifier>
        <Qualifier name="Field Variable">Temperature</Qualifier>
      </ParameterValue>
    </PropertyData>
  </BulkDetails>
</Material>"""

VISCOSITY_VARIABLE = """<?xml version="1.0" ?>
<Material>
  <BulkDetails>
    <Name>material with variable viscosity</Name>
    <PropertyData property="pr0">
      <Data format="string">-</Data>
      <Qualifier name="BETA">Mechanical.ModalAcoustics</Qualifier>
      <ParameterValue parameter="pa0" format="float">
        <Data>2.0, 3.0, 4.0</Data>
        <Qualifier name="Variable Type">Dependent,Dependent,Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa1" format="float">
        <Data>22.0, 50.0, 70.0</Data>
        <Qualifier name="Variable Type">Independent,Independent,Independent</Qualifier>
        <Qualifier name="Field Variable">Temperature</Qualifier>
      </ParameterValue>
    </PropertyData>
  </BulkDetails>
</Material>"""

VISCOSITY_METADATA = """<?xml version="1.0" ?>
<Metadata>
  <PropertyDetails id="pr0">
    <Unitless/>
    <Name>Viscosity</Name>
  </PropertyDetails>
  <ParameterDetails id="pa0">
    <Unitless/>
    <Name>Viscosity</Name>
  </ParameterDetails>
  <ParameterDetails id="pa1">
    <Unitless/>
    <Name>Temperature</Name>
  </ParameterDetails>
</Metadata>"""


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


def test_write_constant_viscosity():
    materials = [
        Material(
            name="material with viscosity",
            models=[
                Viscosity(
                    viscosity=[1.0],
                    independent_parameters=[
                        IndependentParameter(
                            name="Temperature",
                            field_variable="Temperature",
                            values=[22.0, 50.0, 70.0],
                        ),
                    ],
                ),
            ],
        )
    ]

    writer = MatmlWriter(materials)
    tree = writer._to_etree()
    material_string, metadata_string = get_material_and_metadata_from_xml(tree)
    assert material_string == VISCOSITY
    assert metadata_string == VISCOSITY_METADATA


def test_write_variable_viscosity():
    materials = [
        Material(
            name="material with variable viscosity",
            models=[
                Viscosity(
                    viscosity=[2.0, 3.0, 4.0],
                    independent_parameters=[
                        IndependentParameter(
                            name="Temperature",
                            field_variable="Temperature",
                            values=[22.0, 50.0, 70.0],
                        ),
                    ],
                ),
            ],
        )
    ]

    writer = MatmlWriter(materials)
    tree = writer._to_etree()
    material_string, metadata_string = get_material_and_metadata_from_xml(tree)
    assert material_string == VISCOSITY_VARIABLE
    assert metadata_string == VISCOSITY_METADATA
