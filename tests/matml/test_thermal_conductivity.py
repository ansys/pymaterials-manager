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
from ansys.materials.manager._models._material_models.thermal_conductivity_isotropic import (
    ThermalConductivityIsotropic,
)
from ansys.materials.manager._models._material_models.thermal_conductivity_orthotropic import (
    ThermalConductivityOrthotropic,
)
from ansys.materials.manager._models.material import Material
from ansys.materials.manager.util.matml.matml_from_material import MatmlWriter

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
XML_FILE_PATH = os.path.join(DIR_PATH, "..", "data", "MatML_unittest_thermal_conductivity.xml")

THERMAL_CONDUCTIVITY_ISOTROPIC = """<?xml version="1.0" ?>
<Material>
  <BulkDetails>
    <Name>Isotropic Convection Test Material</Name>
    <PropertyData property="pr0">
      <Data format="string">-</Data>
      <Qualifier name="Behavior">Isotropic</Qualifier>
      <ParameterValue parameter="pa0" format="float">
        <Data>10.0</Data>
        <Qualifier name="Variable Type">Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa1" format="float">
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

THERMAL_CONDUCTIVITY_ISOTROPIC_METADATA = """<?xml version="1.0" ?>
<Metadata>
  <PropertyDetails id="pr0">
    <Unitless/>
    <Name>Thermal Conductivity</Name>
  </PropertyDetails>
  <ParameterDetails id="pa0">
    <Unitless/>
    <Name>Thermal Conductivity</Name>
  </ParameterDetails>
  <ParameterDetails id="pa1">
    <Unitless/>
    <Name>Temperature</Name>
  </ParameterDetails>
</Metadata>"""

THERMAL_CONDUCTIVITY_ORTHOTROPIC = """<?xml version="1.0" ?>
<Material>
  <BulkDetails>
    <Name>Orthotropic Convection Test Material</Name>
    <PropertyData property="pr0">
      <Data format="string">-</Data>
      <Qualifier name="Behavior">Orthotropic</Qualifier>
      <ParameterValue parameter="pa0" format="float">
        <Data>10.0</Data>
        <Qualifier name="Variable Type">Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa1" format="float">
        <Data>15.0</Data>
        <Qualifier name="Variable Type">Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa2" format="float">
        <Data>20.0</Data>
        <Qualifier name="Variable Type">Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa3" format="float">
        <Data>7.88860905221012e-31</Data>
        <Qualifier name="Variable Type">Independent</Qualifier>
        <Qualifier name="Field Variable">Temperature</Qualifier>
      </ParameterValue>
    </PropertyData>
  </BulkDetails>
</Material>"""

THERMAL_CONDUCTIVITY_ORTHOTROPIC_METADATA = """<?xml version="1.0" ?>
<Metadata>
  <PropertyDetails id="pr0">
    <Unitless/>
    <Name>Thermal Conductivity</Name>
  </PropertyDetails>
  <ParameterDetails id="pa0">
    <Unitless/>
    <Name>Thermal Conductivity X direction</Name>
  </ParameterDetails>
  <ParameterDetails id="pa1">
    <Unitless/>
    <Name>Thermal Conductivity Y direction</Name>
  </ParameterDetails>
  <ParameterDetails id="pa2">
    <Unitless/>
    <Name>Thermal Conductivity Z direction</Name>
  </ParameterDetails>
  <ParameterDetails id="pa3">
    <Unitless/>
    <Name>Temperature</Name>
  </ParameterDetails>
</Metadata>"""


def test_read_thermal_conductivity_isotropic_material():
    material_dic = read_matml_file(XML_FILE_PATH)
    assert "Isotropic Convection Test Material" in material_dic.keys()
    assert len(material_dic["Isotropic Convection Test Material"].models) == 2
    isotropic_conductivity = material_dic["Isotropic Convection Test Material"].models[1]
    assert isotropic_conductivity.name == "Thermal Conductivity"
    assert isotropic_conductivity.model_qualifiers[0].name == "Behavior"
    assert isotropic_conductivity.model_qualifiers[0].value == "Isotropic"
    assert isotropic_conductivity.model_qualifiers[1].name == "Field Variable Compatible"
    assert isotropic_conductivity.model_qualifiers[1].value == "Temperature"
    assert isotropic_conductivity.thermal_conductivity == [10.0]
    assert isotropic_conductivity.independent_parameters[0].name == "Temperature"
    assert isotropic_conductivity.independent_parameters[0].values == [7.88860905221012e-31]
    assert isotropic_conductivity.independent_parameters[0].units == "C"
    assert isotropic_conductivity.independent_parameters[0].upper_limit == "Program Controlled"
    assert isotropic_conductivity.independent_parameters[0].lower_limit == "Program Controlled"
    assert isotropic_conductivity.independent_parameters[0].default_value == "22"


def test_read_thermal_conductivity_orthotropic_material():
    material_dic = read_matml_file(XML_FILE_PATH)
    assert "Orthotropic Convection Test Material" in material_dic.keys()
    assert len(material_dic["Orthotropic Convection Test Material"].models) == 2
    orthotropic_conductivity = material_dic["Orthotropic Convection Test Material"].models[1]
    assert orthotropic_conductivity.name == "Thermal Conductivity"
    assert orthotropic_conductivity.model_qualifiers[0].name == "Behavior"
    assert orthotropic_conductivity.model_qualifiers[0].value == "Orthotropic"
    assert orthotropic_conductivity.thermal_conductivity_x == [10.0]
    assert orthotropic_conductivity.thermal_conductivity_y == [15.0]
    assert orthotropic_conductivity.thermal_conductivity_z == [20.0]
    assert orthotropic_conductivity.independent_parameters[0].name == "Temperature"
    assert orthotropic_conductivity.independent_parameters[0].values == [7.88860905221012e-31]


def test_write_thermal_conductivity_isotropic():
    materials = [
        Material(
            name="Isotropic Convection Test Material",
            models=[
                ThermalConductivityIsotropic(
                    thermal_conductivity=[10.0],
                    independent_parameters=[
                        IndependentParameter(
                            name="Temperature",
                            field_variable="Temperature",
                            values=[7.88860905221012e-31],
                            units="C",
                            default_value="22",
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
    assert material_string == THERMAL_CONDUCTIVITY_ISOTROPIC
    assert metadata_string == THERMAL_CONDUCTIVITY_ISOTROPIC_METADATA


def test_write_thermal_conductivity_orthotropic():
    materials = [
        Material(
            name="Orthotropic Convection Test Material",
            models=[
                ThermalConductivityOrthotropic(
                    thermal_conductivity_x=[10.0],
                    thermal_conductivity_y=[15.0],
                    thermal_conductivity_z=[20.0],
                    independent_parameters=[
                        IndependentParameter(
                            name="Temperature",
                            field_variable="Temperature",
                            values=[7.88860905221012e-31],
                        ),
                    ],
                ),
            ],
        )
    ]

    writer = MatmlWriter(materials)
    tree = writer._to_etree()
    material_string, metadata_string = get_material_and_metadata_from_xml(tree)
    assert material_string == THERMAL_CONDUCTIVITY_ORTHOTROPIC
    assert metadata_string == THERMAL_CONDUCTIVITY_ORTHOTROPIC_METADATA
