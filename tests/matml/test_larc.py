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
from ansys.materials.manager._models._material_models.larc03_04_constants import LaRc0304Constants
from ansys.materials.manager._models.material import Material
from ansys.materials.manager.util.matml.matml_from_material import MatmlWriter

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
XML_FILE_PATH = os.path.join(DIR_PATH, "..", "data", "MatML_unittest_larc.xml")

LARC = """<?xml version="1.0" ?>
<Material>
  <BulkDetails>
    <Name>material with larc</Name>
    <PropertyData property="pr0">
      <Data format="string">-</Data>
      <ParameterValue parameter="pa0" format="float">
        <Data>1.0</Data>
        <Qualifier name="Variable Type">Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa1" format="float">
        <Data>2.0</Data>
        <Qualifier name="Variable Type">Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa2" format="float">
        <Data>3.0</Data>
        <Qualifier name="Variable Type">Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa3" format="float">
        <Data>4.0</Data>
        <Qualifier name="Variable Type">Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa4" format="float">
        <Data>7.88860905221012e-31</Data>
        <Qualifier name="Variable Type">Independent</Qualifier>
      </ParameterValue>
    </PropertyData>
  </BulkDetails>
</Material>"""

LARC_VARIABLE = """<?xml version="1.0" ?>
<Material>
  <BulkDetails>
    <Name>material with variable larc</Name>
    <PropertyData property="pr0">
      <Data format="string">-</Data>
      <ParameterValue parameter="pa0" format="float">
        <Data>5.0, 9.0, 13.0</Data>
        <Qualifier name="Variable Type">Dependent,Dependent,Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa1" format="float">
        <Data>6.0, 10.0, 14.0</Data>
        <Qualifier name="Variable Type">Dependent,Dependent,Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa2" format="float">
        <Data>7.0, 11.0, 15.0</Data>
        <Qualifier name="Variable Type">Dependent,Dependent,Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa3" format="float">
        <Data>8.0, 12.0, 16.0</Data>
        <Qualifier name="Variable Type">Dependent,Dependent,Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa4" format="float">
        <Data>22.0, 50.0, 70.0</Data>
        <Qualifier name="Variable Type">Independent,Independent,Independent</Qualifier>
      </ParameterValue>
    </PropertyData>
  </BulkDetails>
</Material>"""

LARC_METADATA = """<?xml version="1.0" ?>
<Metadata>
  <PropertyDetails id="pr0">
    <Unitless/>
    <Name>LaRc03/04 Constants</Name>
  </PropertyDetails>
  <ParameterDetails id="pa0">
    <Unitless/>
    <Name>Fracture Toughness Ratio</Name>
  </ParameterDetails>
  <ParameterDetails id="pa1">
    <Unitless/>
    <Name>Longitudinal Friction Coefficient</Name>
  </ParameterDetails>
  <ParameterDetails id="pa2">
    <Unitless/>
    <Name>Transverse Friction Coefficient</Name>
  </ParameterDetails>
  <ParameterDetails id="pa3">
    <Unitless/>
    <Name>Fracture Angle Under Compression</Name>
  </ParameterDetails>
  <ParameterDetails id="pa4">
    <Unitless/>
    <Name>Temperature</Name>
  </ParameterDetails>
</Metadata>"""


def test_read_constant_larc():
    material_dic = read_matml_file(XML_FILE_PATH)
    material_name = "material with larc"
    assert material_name in material_dic.keys()
    assert len(material_dic[material_name].models) == 2
    larc = material_dic[material_name].models[1]
    assert larc.name == "LaRc03/04 Constants"
    assert larc.fracture_toughness_ratio == [1.0]
    assert larc.longitudinal_friction_coefficient == [2.0]
    assert larc.transverse_friction_coefficient == [3.0]
    assert larc.fracture_angle_under_compression == [4.0]
    assert larc.independent_parameters[0].name == "Temperature"
    assert larc.independent_parameters[0].values == [7.88860905221012e-31]


def test_read_variable_larc():
    material_dic = read_matml_file(XML_FILE_PATH)
    material_name = "material with variable larc"
    assert material_name in material_dic.keys()
    assert len(material_dic[material_name].models) == 2
    larc = material_dic[material_name].models[1]
    assert larc.name == "LaRc03/04 Constants"
    assert larc.fracture_toughness_ratio == [5.0, 9.0, 13.0]
    assert larc.longitudinal_friction_coefficient == [6.0, 10.0, 14.0]
    assert larc.transverse_friction_coefficient == [7.0, 11.0, 15.0]
    assert larc.fracture_angle_under_compression == [8.0, 12.0, 16.0]
    assert larc.independent_parameters[0].name == "Temperature"
    assert larc.independent_parameters[0].values == [22.0, 50.0, 70.0]


def test_write_constant_larc():
    materials = [
        Material(
            name="material with larc",
            models=[
                LaRc0304Constants(
                    fracture_toughness_ratio=[1.0],
                    longitudinal_friction_coefficient=[2.0],
                    transverse_friction_coefficient=[3.0],
                    fracture_angle_under_compression=[4.0],
                    independent_parameters=[
                        IndependentParameter(name="Temperature", values=[7.88860905221012e-31])
                    ],
                ),
            ],
        )
    ]

    writer = MatmlWriter(materials)
    tree = writer._to_etree()
    material_string, metadata_string = get_material_and_metadata_from_xml(tree)
    print(material_string)
    print(metadata_string)
    assert material_string == LARC
    assert metadata_string == LARC_METADATA


def test_write_variable_larc():
    materials = [
        Material(
            name="material with variable larc",
            models=[
                LaRc0304Constants(
                    fracture_toughness_ratio=[5.0, 9.0, 13.0],
                    longitudinal_friction_coefficient=[6.0, 10.0, 14.0],
                    transverse_friction_coefficient=[7.0, 11.0, 15.0],
                    fracture_angle_under_compression=[8.0, 12.0, 16.0],
                    independent_parameters=[
                        IndependentParameter(name="Temperature", values=[22.0, 50.0, 70.0])
                    ],
                ),
            ],
        )
    ]

    writer = MatmlWriter(materials)
    tree = writer._to_etree()
    material_string, metadata_string = get_material_and_metadata_from_xml(tree)
    print(material_string)
    assert material_string == LARC_VARIABLE
    assert metadata_string == LARC_METADATA
