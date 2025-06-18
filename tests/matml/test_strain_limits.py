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
from ansys.materials.manager._models._material_models.strain_limits_isotropic import (
    StrainLimitsIsotropic,
)
from ansys.materials.manager._models._material_models.strain_limits_orthotropic import (
    StrainLimitsOrthotropic,
)
from ansys.materials.manager._models.material import Material
from ansys.materials.manager.util.matml.matml_from_material import MatmlWriter

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
XML_FILE_PATH = os.path.join(DIR_PATH, "..", "data", "MatML_unittest_strain_limit.xml")

STRAIN_LIMITS_ORTHOTROPIC = """<?xml version="1.0" ?>
<Material>
  <BulkDetails>
    <Name>orthotropic material with strain limit</Name>
    <PropertyData property="pr0">
      <Data format="string">-</Data>
      <Qualifier name="Definition">Orthotropic</Qualifier>
      <ParameterValue parameter="pa0" format="float">
        <Data>311.0</Data>
        <Qualifier name="Variable Type">Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa1" format="float">
        <Data>213.0</Data>
        <Qualifier name="Variable Type">Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa2" format="float">
        <Data>13.0</Data>
        <Qualifier name="Variable Type">Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa3" format="float">
        <Data>-132.0</Data>
        <Qualifier name="Variable Type">Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa4" format="float">
        <Data>-13.0</Data>
        <Qualifier name="Variable Type">Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa5" format="float">
        <Data>-13.0</Data>
        <Qualifier name="Variable Type">Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa6" format="float">
        <Data>24.0</Data>
        <Qualifier name="Variable Type">Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa7" format="float">
        <Data>12.0</Data>
        <Qualifier name="Variable Type">Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa8" format="float">
        <Data>232.0</Data>
        <Qualifier name="Variable Type">Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa9" format="float">
        <Data>7.88860905221012e-31</Data>
        <Qualifier name="Variable Type">Independent</Qualifier>
        <Qualifier name="Field Variable">Temperature</Qualifier>
        <Qualifier name="Default Data">22</Qualifier>
        <Qualifier name="Field Units">C</Qualifier>
        <Qualifier name="Upper Limit">Program Controlled</Qualifier>
        <Qualifier name="Lower Limit">Program Controlled</Qualifier>
      </ParameterValue>
    </PropertyData>
  </BulkDetails>
</Material>"""

STRAIN_LIMITS_ISOTROPIC = """<?xml version="1.0" ?>
<Material>
  <BulkDetails>
    <Name>isotropic material with strain limit</Name>
    <PropertyData property="pr0">
      <Data format="string">-</Data>
      <Qualifier name="Definition">Isotropic</Qualifier>
      <ParameterValue parameter="pa0" format="float">
        <Data>213.0</Data>
        <Qualifier name="Variable Type">Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa1" format="float">
        <Data>7.88860905221012e-31</Data>
        <Qualifier name="Variable Type">Independent</Qualifier>
      </ParameterValue>
    </PropertyData>
  </BulkDetails>
</Material>"""

STRAIN_LIMITS_VARIABLE_ISOTROPIC = """<?xml version="1.0" ?>
<Material>
  <BulkDetails>
    <Name>isotropic material with variable strain limit</Name>
    <PropertyData property="pr0">
      <Data format="string">-</Data>
      <Qualifier name="Definition">Isotropic</Qualifier>
      <ParameterValue parameter="pa0" format="float">
        <Data>2333.0, 2324.0, 2432.0</Data>
        <Qualifier name="Variable Type">Dependent,Dependent,Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa1" format="float">
        <Data>23.0, 25.0, 27.0</Data>
        <Qualifier name="Variable Type">Independent,Independent,Independent</Qualifier>
      </ParameterValue>
    </PropertyData>
  </BulkDetails>
</Material>"""

STRAIN_LIMITS_VARIABLE_ORTHOTROPIC = """<?xml version="1.0" ?>
<Material>
  <BulkDetails>
    <Name>orthotropic material with variable strain limit</Name>
    <PropertyData property="pr0">
      <Data format="string">-</Data>
      <Qualifier name="Definition">Orthotropic</Qualifier>
      <ParameterValue parameter="pa0" format="float">
        <Data>324.0, 311.0, 312.0</Data>
        <Qualifier name="Variable Type">Dependent,Dependent,Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa1" format="float">
        <Data>236.0, 213.0, 234.0</Data>
        <Qualifier name="Variable Type">Dependent,Dependent,Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa2" format="float">
        <Data>15.0, 13.0, 14.0</Data>
        <Qualifier name="Variable Type">Dependent,Dependent,Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa3" format="float">
        <Data>-110.0, -132.0, -120.0</Data>
        <Qualifier name="Variable Type">Dependent,Dependent,Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa4" format="float">
        <Data>-11.0, -13.0, -12.0</Data>
        <Qualifier name="Variable Type">Dependent,Dependent,Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa5" format="float">
        <Data>-9.0, -13.0, -11.0</Data>
        <Qualifier name="Variable Type">Dependent,Dependent,Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa6" format="float">
        <Data>26.0, 24.0, 25.0</Data>
        <Qualifier name="Variable Type">Dependent,Dependent,Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa7" format="float">
        <Data>16.0, 12.0, 14.0</Data>
        <Qualifier name="Variable Type">Dependent,Dependent,Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa8" format="float">
        <Data>255.0, 232.0, 244.0</Data>
        <Qualifier name="Variable Type">Dependent,Dependent,Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa9" format="float">
        <Data>13.0, 21.0, 23.0</Data>
        <Qualifier name="Variable Type">Independent,Independent,Independent</Qualifier>
        <Qualifier name="Default Data">22</Qualifier>
        <Qualifier name="Field Units">C</Qualifier>
        <Qualifier name="Upper Limit">Program Controlled</Qualifier>
        <Qualifier name="Lower Limit">Program Controlled</Qualifier>
      </ParameterValue>
    </PropertyData>
  </BulkDetails>
</Material>"""

STRAIN_LIMITS_ORTHOTROPIC_METADATA = """<?xml version="1.0" ?>
<Metadata>
  <PropertyDetails id="pr0">
    <Unitless/>
    <Name>Strain Limits</Name>
  </PropertyDetails>
  <ParameterDetails id="pa0">
    <Unitless/>
    <Name>Tensile X direction</Name>
  </ParameterDetails>
  <ParameterDetails id="pa1">
    <Unitless/>
    <Name>Tensile Y direction</Name>
  </ParameterDetails>
  <ParameterDetails id="pa2">
    <Unitless/>
    <Name>Tensile Z direction</Name>
  </ParameterDetails>
  <ParameterDetails id="pa3">
    <Unitless/>
    <Name>Compressive X direction</Name>
  </ParameterDetails>
  <ParameterDetails id="pa4">
    <Unitless/>
    <Name>Compressive Y direction</Name>
  </ParameterDetails>
  <ParameterDetails id="pa5">
    <Unitless/>
    <Name>Compressive Z direction</Name>
  </ParameterDetails>
  <ParameterDetails id="pa6">
    <Unitless/>
    <Name>Shear XY</Name>
  </ParameterDetails>
  <ParameterDetails id="pa7">
    <Unitless/>
    <Name>Shear XZ</Name>
  </ParameterDetails>
  <ParameterDetails id="pa8">
    <Unitless/>
    <Name>Shear YZ</Name>
  </ParameterDetails>
  <ParameterDetails id="pa9">
    <Unitless/>
    <Name>Temperature</Name>
  </ParameterDetails>
</Metadata>"""

STRAIN_LIMITS_ISOTROPIC_METADATA = """<?xml version="1.0" ?>
<Metadata>
  <PropertyDetails id="pr0">
    <Unitless/>
    <Name>Strain Limits</Name>
  </PropertyDetails>
  <ParameterDetails id="pa0">
    <Unitless/>
    <Name>Von Mises</Name>
  </ParameterDetails>
  <ParameterDetails id="pa1">
    <Unitless/>
    <Name>Temperature</Name>
  </ParameterDetails>
</Metadata>"""


def test_read_constant_strain_limit_isotropic():
    material_dic = read_matml_file(XML_FILE_PATH)
    assert "isotropic material with strain limit" in material_dic.keys()
    assert len(material_dic["isotropic material with strain limit"].models) == 2
    orthotropic_strain_limits = material_dic["isotropic material with strain limit"].models[1]
    assert orthotropic_strain_limits.name == "Strain Limits"
    assert orthotropic_strain_limits.model_qualifiers[0].name == "Behavior"
    assert orthotropic_strain_limits.model_qualifiers[0].value == "Isotropic"
    assert orthotropic_strain_limits.von_mises == [213]
    assert orthotropic_strain_limits.independent_parameters[0].name == "Temperature"
    assert orthotropic_strain_limits.independent_parameters[0].values == [7.88860905221012e-31]


def test_read_variable_strain_limit_isotropic():
    material_dic = read_matml_file(XML_FILE_PATH)
    assert "isotropic material with variable strain limit" in material_dic.keys()
    assert len(material_dic["isotropic material with variable strain limit"].models) == 2
    orthotropic_strain_limits = material_dic[
        "isotropic material with variable strain limit"
    ].models[1]
    assert orthotropic_strain_limits.name == "Strain Limits"
    assert orthotropic_strain_limits.model_qualifiers[0].name == "Behavior"
    assert orthotropic_strain_limits.model_qualifiers[0].value == "Isotropic"
    assert orthotropic_strain_limits.von_mises == [2333, 2324, 2432]
    assert orthotropic_strain_limits.independent_parameters[0].name == "Temperature"
    assert orthotropic_strain_limits.independent_parameters[0].values == [23, 25, 27]


def test_read_constant_strain_limit_orthotropic():
    material_dic = read_matml_file(XML_FILE_PATH)
    assert "orthotropic material with strain limit" in material_dic.keys()
    assert len(material_dic["orthotropic material with strain limit"].models) == 2
    orthotropic_strain_limits = material_dic["orthotropic material with strain limit"].models[1]
    assert orthotropic_strain_limits.name == "Strain Limits"
    assert orthotropic_strain_limits.model_qualifiers[0].name == "Behavior"
    assert orthotropic_strain_limits.model_qualifiers[0].value == "Orthotropic"
    assert orthotropic_strain_limits.model_qualifiers[1].name == "Field Variable Compatible"
    assert orthotropic_strain_limits.model_qualifiers[1].value == "Temperature"
    assert orthotropic_strain_limits.interpolation_options.algorithm_type == "Linear Multivariate"
    assert orthotropic_strain_limits.interpolation_options.cached == True
    assert orthotropic_strain_limits.interpolation_options.normalized == True
    assert orthotropic_strain_limits.tensile_x_direction == [311.0]
    assert orthotropic_strain_limits.tensile_y_direction == [213.0]
    assert orthotropic_strain_limits.tensile_z_direction == [13.0]
    assert orthotropic_strain_limits.compressive_x_direction == [-132.0]
    assert orthotropic_strain_limits.compressive_y_direction == [-13.0]
    assert orthotropic_strain_limits.compressive_z_direction == [-13.0]
    assert orthotropic_strain_limits.shear_xy == [24.0]
    assert orthotropic_strain_limits.shear_xz == [12.0]
    assert orthotropic_strain_limits.shear_yz == [232.0]
    assert orthotropic_strain_limits.independent_parameters[0].name == "Temperature"
    assert orthotropic_strain_limits.independent_parameters[0].values == [7.88860905221012e-31]
    assert orthotropic_strain_limits.independent_parameters[0].units == "C"
    assert orthotropic_strain_limits.independent_parameters[0].upper_limit == "Program Controlled"
    assert orthotropic_strain_limits.independent_parameters[0].lower_limit == "Program Controlled"
    assert orthotropic_strain_limits.independent_parameters[0].default_value == "22"


def test_read_variable_strain_limit_orthotropic():
    material_dic = read_matml_file(XML_FILE_PATH)
    assert "orthotropic material with variable strain limit" in material_dic.keys()
    assert len(material_dic["orthotropic material with variable strain limit"].models) == 2
    orthotropic_strain_limits = material_dic[
        "orthotropic material with variable strain limit"
    ].models[1]
    assert orthotropic_strain_limits.name == "Strain Limits"
    assert orthotropic_strain_limits.model_qualifiers[0].name == "Behavior"
    assert orthotropic_strain_limits.model_qualifiers[0].value == "Orthotropic"
    assert orthotropic_strain_limits.model_qualifiers[1].name == "Field Variable Compatible"
    assert orthotropic_strain_limits.model_qualifiers[1].value == "Temperature"
    assert orthotropic_strain_limits.interpolation_options.algorithm_type == "Linear Multivariate"
    assert orthotropic_strain_limits.interpolation_options.cached == True
    assert orthotropic_strain_limits.interpolation_options.normalized == True
    assert orthotropic_strain_limits.tensile_x_direction == [324.0, 311.0, 312.0]
    assert orthotropic_strain_limits.tensile_y_direction == [236.0, 213.0, 234.0]
    assert orthotropic_strain_limits.tensile_z_direction == [15.0, 13.0, 14.0]
    assert orthotropic_strain_limits.compressive_x_direction == [-110.0, -132.0, -120.0]
    assert orthotropic_strain_limits.compressive_y_direction == [-11.0, -13.0, -12.0]
    assert orthotropic_strain_limits.compressive_z_direction == [-9.0, -13.0, -11.0]
    assert orthotropic_strain_limits.shear_xy == [26.0, 24.0, 25.0]
    assert orthotropic_strain_limits.shear_xz == [16.0, 12.0, 14.0]
    assert orthotropic_strain_limits.shear_yz == [255.0, 232.0, 244.0]
    assert orthotropic_strain_limits.independent_parameters[0].name == "Temperature"
    assert orthotropic_strain_limits.independent_parameters[0].values == [13.0, 21.0, 23.0]
    assert orthotropic_strain_limits.independent_parameters[0].units == "C"
    assert orthotropic_strain_limits.independent_parameters[0].upper_limit == "Program Controlled"
    assert orthotropic_strain_limits.independent_parameters[0].lower_limit == "Program Controlled"
    assert orthotropic_strain_limits.independent_parameters[0].default_value == "22"


def test_write_constant_strain_limits_orthotropic():
    materials = [
        Material(
            name="orthotropic material with strain limit",
            models=[
                StrainLimitsOrthotropic(
                    compressive_x_direction=[-132.0],
                    compressive_y_direction=[-13.0],
                    compressive_z_direction=[-13.0],
                    tensile_x_direction=[311.0],
                    tensile_y_direction=[213.0],
                    tensile_z_direction=[13.0],
                    shear_xy=[24.0],
                    shear_xz=[12.0],
                    shear_yz=[232.0],
                    independent_parameters=[
                        IndependentParameter(
                            name="Temperature",
                            field_variable="Temperature",
                            values=[7.88860905221012e-31],
                            units="C",
                            upper_limit="Program Controlled",
                            lower_limit="Program Controlled",
                            default_value="22",
                        )
                    ],
                ),
            ],
        )
    ]

    writer = MatmlWriter(materials)
    tree = writer._to_etree()
    material_string, metadata_string = get_material_and_metadata_from_xml(tree)
    assert material_string == STRAIN_LIMITS_ORTHOTROPIC
    assert metadata_string == STRAIN_LIMITS_ORTHOTROPIC_METADATA


def test_write_constant_strain_limits_isotropic():
    materials = [
        Material(
            name="isotropic material with strain limit",
            models=[
                StrainLimitsIsotropic(
                    von_mises=[213],
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
    assert material_string == STRAIN_LIMITS_ISOTROPIC
    assert metadata_string == STRAIN_LIMITS_ISOTROPIC_METADATA


def test_write_variable_strain_limits_isotropic():
    materials = [
        Material(
            name="isotropic material with variable strain limit",
            models=[
                StrainLimitsIsotropic(
                    von_mises=[2333, 2324, 2432],
                    independent_parameters=[
                        IndependentParameter(name="Temperature", values=[23, 25, 27])
                    ],
                ),
            ],
        )
    ]
    writer = MatmlWriter(materials)
    tree = writer._to_etree()
    material_string, metadata_string = get_material_and_metadata_from_xml(tree)
    assert material_string == STRAIN_LIMITS_VARIABLE_ISOTROPIC
    assert metadata_string == STRAIN_LIMITS_ISOTROPIC_METADATA


def test_write_variable_strain_limits_orthotropic():
    materials = [
        Material(
            name="orthotropic material with variable strain limit",
            models=[
                StrainLimitsOrthotropic(
                    tensile_x_direction=[324.0, 311.0, 312.0],
                    tensile_y_direction=[236.0, 213.0, 234.0],
                    tensile_z_direction=[15.0, 13.0, 14.0],
                    compressive_x_direction=[-110.0, -132.0, -120.0],
                    compressive_y_direction=[-11.0, -13.0, -12.0],
                    compressive_z_direction=[-9.0, -13.0, -11.0],
                    shear_xy=[26.0, 24.0, 25.0],
                    shear_xz=[16.0, 12.0, 14.0],
                    shear_yz=[255.0, 232.0, 244.0],
                    independent_parameters=[
                        IndependentParameter(
                            name="Temperature",
                            values=[13.0, 21.0, 23.0],
                            units="C",
                            upper_limit="Program Controlled",
                            lower_limit="Program Controlled",
                            default_value="22",
                        )
                    ],
                ),
            ],
        )
    ]

    writer = MatmlWriter(materials)
    tree = writer._to_etree()
    material_string, metadata_string = get_material_and_metadata_from_xml(tree)
    assert material_string == STRAIN_LIMITS_VARIABLE_ORTHOTROPIC
    assert metadata_string == STRAIN_LIMITS_ORTHOTROPIC_METADATA
