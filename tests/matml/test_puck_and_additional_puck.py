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
from ansys.materials.manager._models._common.model_qualifier import ModelQualifier
from ansys.materials.manager._models._material_models.fiber_angle import FiberAngle
from ansys.materials.manager._models._material_models.puck_constants import PuckConstants
from ansys.materials.manager._models._material_models.puck_constants_additional import (
    AdditionalPuckConstants,
)
from ansys.materials.manager._models._material_models.stress_limits_orthotropic import (
    StressLimitsOrthotropic,
)
from ansys.materials.manager._models.material import Material
from ansys.materials.manager.util.matml.matml_from_material import MatmlWriter

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
XML_FILE_PATH = os.path.join(DIR_PATH, "..", "data", "MatML_unittest_puck_for_woven.xml")

FIBER_ANGLE = """<?xml version="1.0" ?>
<Material>
  <BulkDetails>
    <Name>material with puck for woven</Name>
    <PropertyData property="pr0">
      <Data format="string">-</Data>
      <Qualifier name="Data Set"/>
      <Qualifier name="Data Set Information"/>
      <ParameterValue parameter="pa0" format="float">
        <Data>Woven Specification for Puck</Data>
        <Qualifier name="Variable Type">Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa1" format="float">
        <Data>45.0</Data>
        <Qualifier name="Variable Type">Independent</Qualifier>
      </ParameterValue>
    </PropertyData>
  </BulkDetails>
</Material>"""

PUCK_CONSTANTS = """<?xml version="1.0" ?>
<Material>
  <BulkDetails>
    <Name>material with puck for woven</Name>
    <PropertyData property="pr0">
      <Data format="string">-</Data>
      <Qualifier name="Data Set"/>
      <Qualifier name="Data Set Information"/>
      <ParameterValue parameter="pa0" format="float">
        <Data>Woven Specification for Puck</Data>
        <Qualifier name="Variable Type">Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa1" format="float">
        <Data>0.0</Data>
        <Qualifier name="Variable Type">Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa2" format="float">
        <Data>0.0</Data>
        <Qualifier name="Variable Type">Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa3" format="float">
        <Data>0.0</Data>
        <Qualifier name="Variable Type">Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa4" format="float">
        <Data>0.0</Data>
        <Qualifier name="Variable Type">Dependent</Qualifier>
      </ParameterValue>
    </PropertyData>
  </BulkDetails>
</Material>"""

ADDITIONAL_PUCK_CONSTANTS = """<?xml version="1.0" ?>
<Material>
  <BulkDetails>
    <Name>material with puck for woven</Name>
    <PropertyData property="pr0">
      <Data format="string">-</Data>
      <Qualifier name="Data Set"/>
      <Qualifier name="Data Set Information"/>
      <ParameterValue parameter="pa0" format="float">
        <Data>Woven Specification for Puck</Data>
        <Qualifier name="Variable Type">Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa1" format="float">
        <Data>0.8</Data>
        <Qualifier name="Variable Type">Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa2" format="float">
        <Data>0.5</Data>
        <Qualifier name="Variable Type">Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa3" format="float">
        <Data>0.5</Data>
        <Qualifier name="Variable Type">Dependent</Qualifier>
      </ParameterValue>
    </PropertyData>
  </BulkDetails>
</Material>"""

STRESS_LIMITS = """<?xml version="1.0" ?>
<Material>
  <BulkDetails>
    <Name>material with puck for woven</Name>
    <PropertyData property="pr0">
      <Data format="string">-</Data>
      <Qualifier name="Behavior">Orthotropic</Qualifier>
      <ParameterValue parameter="pa0" format="float">
        <Data>Woven Specification for Puck</Data>
        <Qualifier name="Variable Type">Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa1" format="float">
        <Data>100.0</Data>
        <Qualifier name="Variable Type">Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa2" format="float">
        <Data>101.0</Data>
        <Qualifier name="Variable Type">Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa3" format="float">
        <Data>102.0</Data>
        <Qualifier name="Variable Type">Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa4" format="float">
        <Data>-100.0</Data>
        <Qualifier name="Variable Type">Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa5" format="float">
        <Data>-101.0</Data>
        <Qualifier name="Variable Type">Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa6" format="float">
        <Data>-102.0</Data>
        <Qualifier name="Variable Type">Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa7" format="float">
        <Data>10.0</Data>
        <Qualifier name="Variable Type">Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa8" format="float">
        <Data>14.0</Data>
        <Qualifier name="Variable Type">Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa9" format="float">
        <Data>12.0</Data>
        <Qualifier name="Variable Type">Dependent</Qualifier>
      </ParameterValue>
    </PropertyData>
  </BulkDetails>
</Material>"""

FIBER_ANGLE_METADATA = """<?xml version="1.0" ?>
<Metadata>
  <PropertyDetails id="pr0">
    <Unitless/>
    <Name>Fiber Angle</Name>
  </PropertyDetails>
  <ParameterDetails id="pa0">
    <Unitless/>
    <Name>Material Property</Name>
  </ParameterDetails>
  <ParameterDetails id="pa1">
    <Unitless/>
    <Name>Fiber Angle</Name>
  </ParameterDetails>
</Metadata>"""

STRESS_LIMITS_METADATA = """<?xml version="1.0" ?>
<Metadata>
  <PropertyDetails id="pr0">
    <Unitless/>
    <Name>Stress Limits</Name>
  </PropertyDetails>
  <ParameterDetails id="pa0">
    <Unitless/>
    <Name>Material Property</Name>
  </ParameterDetails>
  <ParameterDetails id="pa1">
    <Unitless/>
    <Name>Tensile X direction</Name>
  </ParameterDetails>
  <ParameterDetails id="pa2">
    <Unitless/>
    <Name>Tensile Y direction</Name>
  </ParameterDetails>
  <ParameterDetails id="pa3">
    <Unitless/>
    <Name>Tensile Z direction</Name>
  </ParameterDetails>
  <ParameterDetails id="pa4">
    <Unitless/>
    <Name>Compressive X direction</Name>
  </ParameterDetails>
  <ParameterDetails id="pa5">
    <Unitless/>
    <Name>Compressive Y direction</Name>
  </ParameterDetails>
  <ParameterDetails id="pa6">
    <Unitless/>
    <Name>Compressive Z direction</Name>
  </ParameterDetails>
  <ParameterDetails id="pa7">
    <Unitless/>
    <Name>Shear XY</Name>
  </ParameterDetails>
  <ParameterDetails id="pa8">
    <Unitless/>
    <Name>Shear XZ</Name>
  </ParameterDetails>
  <ParameterDetails id="pa9">
    <Unitless/>
    <Name>Shear YZ</Name>
  </ParameterDetails>
</Metadata>"""

PUCK_CONSTANTS_METADATA = """<?xml version="1.0" ?>
<Metadata>
  <PropertyDetails id="pr0">
    <Unitless/>
    <Name>Puck Constants</Name>
  </PropertyDetails>
  <ParameterDetails id="pa0">
    <Unitless/>
    <Name>Material Property</Name>
  </ParameterDetails>
  <ParameterDetails id="pa1">
    <Unitless/>
    <Name>Compressive Inclination XZ</Name>
  </ParameterDetails>
  <ParameterDetails id="pa2">
    <Unitless/>
    <Name>Compressive Inclination YZ</Name>
  </ParameterDetails>
  <ParameterDetails id="pa3">
    <Unitless/>
    <Name>Tensile Inclination XZ</Name>
  </ParameterDetails>
  <ParameterDetails id="pa4">
    <Unitless/>
    <Name>Tensile Inclination YZ</Name>
  </ParameterDetails>
</Metadata>"""

ADDITIONAL_PUCK_CONSTANTS_METADATA = """<?xml version="1.0" ?>
<Metadata>
  <PropertyDetails id="pr0">
    <Unitless/>
    <Name>Additional Puck Constants</Name>
  </PropertyDetails>
  <ParameterDetails id="pa0">
    <Unitless/>
    <Name>Material Property</Name>
  </ParameterDetails>
  <ParameterDetails id="pa1">
    <Unitless/>
    <Name>Interface Weakening Factor</Name>
  </ParameterDetails>
  <ParameterDetails id="pa2">
    <Unitless/>
    <Name>Degradation Parameter s</Name>
  </ParameterDetails>
  <ParameterDetails id="pa3">
    <Unitless/>
    <Name>Degradation Parameter M</Name>
  </ParameterDetails>
</Metadata>"""


def test_read_fiber_angle():
    material_dic = read_matml_file(XML_FILE_PATH)
    assert "material with puck for woven" in material_dic.keys()
    assert len(material_dic["material with puck for woven"].models) == 5
    fiber_angle = material_dic["material with puck for woven"].models[1]
    assert fiber_angle.name == "Fiber Angle"
    assert fiber_angle.independent_parameters[0].name == "Fiber Angle"
    assert fiber_angle.independent_parameters[0].values == [90.0]
    assert fiber_angle.model_qualifiers[0].name == "Data Set"
    assert fiber_angle.model_qualifiers[0].value == "2"
    assert fiber_angle.model_qualifiers[1].name == "Data Set Information"
    assert (
        fiber_angle.model_qualifiers[1].value
        == "minOccurrences::2$$maxOccurrences::2$$Name::Unidirectional"
    )


def test_read_puck_constants():
    material_dic = read_matml_file(XML_FILE_PATH)
    assert "material with puck for woven" in material_dic.keys()
    assert len(material_dic["material with puck for woven"].models) == 5
    puck_constants = material_dic["material with puck for woven"].models[3]
    assert puck_constants.name == "Puck Constants"
    assert puck_constants.independent_parameters == []
    assert puck_constants.model_qualifiers[0].name == "Data Set"
    assert puck_constants.model_qualifiers[0].value == "2"
    assert puck_constants.model_qualifiers[1].name == "Data Set Information"
    assert (
        puck_constants.model_qualifiers[1].value
        == "minOccurrences::2$$maxOccurrences::2$$Name::Unidirectional"
    )
    assert puck_constants.model_qualifiers[2].name == "Material Classification"
    assert puck_constants.model_qualifiers[2].value == "Material Specific"
    assert puck_constants.compressive_inclination_xz == [0.0]
    assert puck_constants.compressive_inclination_yz == [0.0]
    assert puck_constants.tensile_inclination_xz == [0.0]
    assert puck_constants.tensile_inclination_yz == [0.0]
    assert puck_constants.material_property == "Woven Specification for Puck"


def test_read_puck_additional_constants():
    material_dic = read_matml_file(XML_FILE_PATH)
    assert "material with puck for woven" in material_dic.keys()
    assert len(material_dic["material with puck for woven"].models) == 5
    puck_additional_constants = material_dic["material with puck for woven"].models[4]
    assert puck_additional_constants.name == "Additional Puck Constants"
    assert puck_additional_constants.independent_parameters == []
    assert puck_additional_constants.model_qualifiers[0].name == "Data Set"
    assert puck_additional_constants.model_qualifiers[0].value == "2"
    assert puck_additional_constants.model_qualifiers[1].name == "Data Set Information"
    assert (
        puck_additional_constants.model_qualifiers[1].value
        == "minOccurrences::2$$maxOccurrences::2$$Name::Unidirectional"
    )
    assert puck_additional_constants.degradation_parameter_s == [0.5]
    assert puck_additional_constants.degradation_parameter_m == [0.5]
    assert puck_additional_constants.interface_weakening_factor == [0.8]
    assert puck_additional_constants.material_property == "Woven Specification for Puck"


def test_read_stress_limits_orthotropic():
    material_dic = read_matml_file(XML_FILE_PATH)
    assert "material with puck for woven" in material_dic.keys()
    assert "material with puck for woven" in material_dic.keys()
    assert len(material_dic["material with puck for woven"].models) == 5
    stress_limits_orthotropic = material_dic["material with puck for woven"].models[2]
    assert stress_limits_orthotropic.name == "Stress Limits"
    assert stress_limits_orthotropic.independent_parameters == []
    assert stress_limits_orthotropic.model_qualifiers[0].name == "Behavior"
    assert stress_limits_orthotropic.model_qualifiers[0].value == "Orthotropic"
    assert stress_limits_orthotropic.model_qualifiers[1].name == "Data Set"
    assert stress_limits_orthotropic.model_qualifiers[1].value == "2"
    assert stress_limits_orthotropic.model_qualifiers[2].name == "Data Set Information"
    assert (
        stress_limits_orthotropic.model_qualifiers[2].value
        == "minOccurrences::2$$maxOccurrences::2$$Name::Unidirectional"
    )
    assert stress_limits_orthotropic.compressive_x_direction == [-100.0]
    assert stress_limits_orthotropic.compressive_y_direction == [-101.0]
    assert stress_limits_orthotropic.compressive_z_direction == [-102.0]
    assert stress_limits_orthotropic.tensile_x_direction == [100.0]
    assert stress_limits_orthotropic.tensile_y_direction == [101.0]
    assert stress_limits_orthotropic.tensile_z_direction == [102.0]
    assert stress_limits_orthotropic.shear_xy == [10.0]
    assert stress_limits_orthotropic.shear_xz == [14.0]
    assert stress_limits_orthotropic.shear_yz == [12.0]


def test_write_fiber_angle():
    materials = [
        Material(
            name="material with puck for woven",
            models=[
                FiberAngle(
                    model_qualifiers=[
                        ModelQualifier(name="Data Set", values=["1"]),
                        ModelQualifier(
                            name="Data Set Information",
                            values=["minOccurrences::2$$maxOccurrences::2$$Name::Unidirectional"],
                        ),
                    ],
                    material_property="Woven Specification for Puck",
                    independent_parameters=[
                        IndependentParameter(name="Fiber Angle", values=[45.0])
                    ],
                ),
            ],
        )
    ]

    writer = MatmlWriter(materials)
    tree = writer._to_etree()
    material_string, metadata_string = get_material_and_metadata_from_xml(tree)
    assert material_string == FIBER_ANGLE
    assert metadata_string == FIBER_ANGLE_METADATA


def test_write_puck_constants():
    materials = [
        Material(
            name="material with puck for woven",
            models=[
                PuckConstants(
                    compressive_inclination_xz=[0.0],
                    compressive_inclination_yz=[0.0],
                    tensile_inclination_xz=[0.0],
                    tensile_inclination_yz=[0.0],
                    model_qualifiers=[
                        ModelQualifier(name="Data Set", values=["2"]),
                        ModelQualifier(
                            name="Data Set Information",
                            values=["minOccurrences::2$$maxOccurrences::2$$Name::Unidirectional"],
                        ),
                    ],
                    material_property="Woven Specification for Puck",
                ),
            ],
        )
    ]

    writer = MatmlWriter(materials)
    tree = writer._to_etree()
    material_string, metadata_string = get_material_and_metadata_from_xml(tree)
    assert material_string == PUCK_CONSTANTS
    assert metadata_string == PUCK_CONSTANTS_METADATA


def test_write_puck_additional_constants():
    materials = [
        Material(
            name="material with puck for woven",
            models=[
                AdditionalPuckConstants(
                    degradation_parameter_s=[0.5],
                    degradation_parameter_m=[0.5],
                    interface_weakening_factor=[0.8],
                    model_qualifiers=[
                        ModelQualifier(name="Data Set", values=["2"]),
                        ModelQualifier(
                            name="Data Set Information",
                            values=["minOccurrences::2$$maxOccurrences::2$$Name::Unidirectional"],
                        ),
                    ],
                    material_property="Woven Specification for Puck",
                ),
            ],
        )
    ]

    writer = MatmlWriter(materials)
    tree = writer._to_etree()
    material_string, metadata_string = get_material_and_metadata_from_xml(tree)
    assert material_string == ADDITIONAL_PUCK_CONSTANTS
    assert metadata_string == ADDITIONAL_PUCK_CONSTANTS_METADATA


def test_write_stress_limits():
    materials = [
        Material(
            name="material with puck for woven",
            models=[
                StressLimitsOrthotropic(
                    compressive_x_direction=[-100.0],
                    compressive_y_direction=[-101.0],
                    compressive_z_direction=[-102.0],
                    tensile_x_direction=[100.0],
                    tensile_y_direction=[101.0],
                    tensile_z_direction=[102.0],
                    shear_xy=[10.0],
                    shear_xz=[14.0],
                    shear_yz=[12.0],
                    material_property="Woven Specification for Puck",
                ),
            ],
        )
    ]

    writer = MatmlWriter(materials)
    tree = writer._to_etree()
    material_string, metadata_string = get_material_and_metadata_from_xml(tree)
    assert material_string == STRESS_LIMITS
    assert metadata_string == STRESS_LIMITS_METADATA
