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
from ansys.materials.manager._models._common.user_parameter import UserParameter
from ansys.materials.manager._models._material_models.usermat import ModelCoefficients
from ansys.materials.manager._models.material import Material
from ansys.materials.manager.util.matml.matml_from_material import MatmlWriter

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
XML_FILE_PATH = os.path.join(DIR_PATH, "..", "data", "MatML_unittest_usermat.xml")

USERMAT = """<?xml version="1.0" ?>
<Material>
  <BulkDetails>
    <Name>isotropic material with strain limit</Name>
    <PropertyData property="pr0">
      <Data format="string">-</Data>
      <Qualifier name="UserMat">USER</Qualifier>
      <ParameterValue parameter="pa0" format="float">
        <Data>0.0</Data>
        <Qualifier name="Variable Type">Dependent</Qualifier>
        <Qualifier name="Display">True</Qualifier>
        <Qualifier name="UserMat Constant">1</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa1" format="float">
        <Data>UserDefinedPropertySet</Data>
        <Qualifier name="Variable Type">Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa2" format="float">
        <Data>7.88860905221012e-31</Data>
        <Qualifier name="Variable Type">Independent</Qualifier>
      </ParameterValue>
    </PropertyData>
  </BulkDetails>
</Material>"""

USERMAT_VARIABLE = """<?xml version="1.0" ?>
<Material>
  <BulkDetails>
    <Name>variable usermat</Name>
    <PropertyData property="pr0">
      <Data format="string">-</Data>
      <Qualifier name="UserMat">USER</Qualifier>
      <ParameterValue parameter="pa0" format="float">
        <Data>0.1, 0.4</Data>
        <Qualifier name="Variable Type">Dependent,Dependent</Qualifier>
        <Qualifier name="Display">True</Qualifier>
        <Qualifier name="UserMat Constant">1</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa1" format="float">
        <Data>0.2, 0.8</Data>
        <Qualifier name="Variable Type">Dependent,Dependent</Qualifier>
        <Qualifier name="Display">True</Qualifier>
        <Qualifier name="UserMat Constant">2</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa2" format="float">
        <Data>CustomPset</Data>
        <Qualifier name="Variable Type">Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa3" format="float">
        <Data>10.0, 20.0</Data>
        <Qualifier name="Variable Type">Independent,Independent</Qualifier>
      </ParameterValue>
    </PropertyData>
  </BulkDetails>
</Material>"""

USERMAT_METADATA = """<?xml version="1.0" ?>
<Metadata>
  <PropertyDetails id="pr0">
    <Unitless/>
    <Name>Model Coefficients</Name>
  </PropertyDetails>
  <ParameterDetails id="pa0">
    <Unitless/>
    <Name>y</Name>
  </ParameterDetails>
  <ParameterDetails id="pa1">
    <Unitless/>
    <Name>Material Property</Name>
  </ParameterDetails>
  <ParameterDetails id="pa2">
    <Unitless/>
    <Name>Temperature</Name>
  </ParameterDetails>
</Metadata>"""

USERMAT_VARIABLE_METADATA = """<?xml version="1.0" ?>
<Metadata>
  <PropertyDetails id="pr0">
    <Unitless/>
    <Name>Model Coefficients</Name>
  </PropertyDetails>
  <ParameterDetails id="pa0">
    <Unitless/>
    <Name>alpha</Name>
  </ParameterDetails>
  <ParameterDetails id="pa1">
    <Unitless/>
    <Name>beta</Name>
  </ParameterDetails>
  <ParameterDetails id="pa2">
    <Unitless/>
    <Name>Material Property</Name>
  </ParameterDetails>
  <ParameterDetails id="pa3">
    <Unitless/>
    <Name>Temperature</Name>
  </ParameterDetails>
</Metadata>"""


def test_read_usermat():
    material_dic = read_matml_file(XML_FILE_PATH)
    material_name = "usermat"
    assert material_name in material_dic.keys()
    assert len(material_dic[material_name].models) == 4
    usermat = material_dic[material_name].models[3]
    assert usermat.name == "Model Coefficients"
    assert usermat.model_qualifiers[0].name == "UserMat"
    assert usermat.model_qualifiers[0].value == "USER"
    assert usermat.model_qualifiers[1].name == "Custom Qualifier"
    assert usermat.model_qualifiers[1].value == "Custom Qualifier Value"
    assert usermat.material_property == "UserDefinedPropertySet"
    assert usermat.independent_parameters[0].name == "Temperature"
    assert usermat.independent_parameters[0].values == [7.88860905221012e-31]
    assert usermat.user_parameters[0].name == "y"
    assert usermat.user_parameters[0].values == [0.0]
    assert usermat.user_parameters[0].user_mat_constant == 1
    assert usermat.user_parameters[0].display == True


def test_variable_user_mat():
    material_dic = read_matml_file(XML_FILE_PATH)
    material_name = "variable usermat"
    assert material_name in material_dic.keys()
    assert len(material_dic[material_name].models) == 4
    usermat = material_dic[material_name].models[3]
    assert usermat.name == "Model Coefficients"
    assert usermat.model_qualifiers[0].name == "UserMat"
    assert usermat.model_qualifiers[0].value == "USER"
    assert usermat.material_property == "CustomPset"
    assert usermat.independent_parameters[0].name == "Temperature"
    assert usermat.independent_parameters[0].values == [10.0, 20.0]
    assert usermat.user_parameters[0].name == "alpha"
    assert usermat.user_parameters[0].values == [0.1, 0.4]
    assert usermat.user_parameters[0].user_mat_constant == 1
    assert usermat.user_parameters[0].display == True
    assert usermat.user_parameters[1].name == "beta"
    assert usermat.user_parameters[1].values == [0.2, 0.8]
    assert usermat.user_parameters[1].user_mat_constant == 2
    assert usermat.user_parameters[1].display == True


def test_write_constant_usermat():
    materials = [
        Material(
            name="isotropic material with strain limit",
            models=[
                ModelCoefficients(
                    user_parameters=[
                        UserParameter(
                            name="y",
                            values=[0.0],
                            user_mat_constant=1,
                            display=True,
                        )
                    ],
                    independent_parameters=[
                        IndependentParameter(name="Temperature", values=[7.88860905221012e-31])
                    ],
                    material_property="UserDefinedPropertySet",
                ),
            ],
        )
    ]

    writer = MatmlWriter(materials)
    tree = writer._to_etree()
    material_string, metadata_string = get_material_and_metadata_from_xml(tree)
    assert material_string == USERMAT
    assert metadata_string == USERMAT_METADATA


def test_write_variable_usermat():
    materials = [
        Material(
            name="variable usermat",
            models=[
                ModelCoefficients(
                    user_parameters=[
                        UserParameter(
                            name="alpha",
                            values=[0.1, 0.4],
                            user_mat_constant=1,
                            display=True,
                        ),
                        UserParameter(
                            name="beta",
                            values=[0.2, 0.8],
                            user_mat_constant=2,
                            display=True,
                        ),
                    ],
                    independent_parameters=[
                        IndependentParameter(name="Temperature", values=[10.0, 20.0])
                    ],
                    material_property="CustomPset",
                ),
            ],
        )
    ]

    writer = MatmlWriter(materials)
    tree = writer._to_etree()
    material_string, metadata_string = get_material_and_metadata_from_xml(tree)
    assert material_string == USERMAT_VARIABLE
    assert metadata_string == USERMAT_VARIABLE_METADATA
