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
from ansys.materials.manager._models._material_models.specific_heat import SpecificHeat
from ansys.materials.manager._models.material import Material
from ansys.materials.manager.util.matml.matml_from_material import MatmlWriter

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
XML_FILE_PATH = os.path.join(DIR_PATH, "..", "data", "MatML_unittest_specific_heat.xml")

SPECIFIC_HEAT_VOLUME = """<?xml version="1.0" ?>
<Material>
  <BulkDetails>
    <Name>material with specific heat volume</Name>
    <PropertyData property="pr0">
      <Data format="string">-</Data>
      <Qualifier name="Definition">Constant Volume</Qualifier>
      <Qualifier name="Field Variable Compatible">Temperature</Qualifier>
      <Qualifier name="Symbol">Cᵥ</Qualifier>
      <ParameterValue parameter="pa0" format="float">
        <Data>2.0</Data>
        <Qualifier name="Variable Type">Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa1" format="float">
        <Data>22.0</Data>
        <Qualifier name="Variable Type">Independent</Qualifier>
        <Qualifier name="Field Variable">Temperature</Qualifier>
        <Qualifier name="Default Data">22.0</Qualifier>
        <Qualifier name="Field Units">C</Qualifier>
        <Qualifier name="Upper Limit">Program Controlled</Qualifier>
        <Qualifier name="Lower Limit">Program Controlled</Qualifier>
      </ParameterValue>
    </PropertyData>
  </BulkDetails>
</Material>"""

SPECIFIC_HEAT_VOLUME_VARIABLE = """<?xml version="1.0" ?>
<Material>
  <BulkDetails>
    <Name>material with variable specific heat volume</Name>
    <PropertyData property="pr0">
      <Data format="string">-</Data>
      <Qualifier name="Definition">Constant Volume</Qualifier>
      <Qualifier name="Field Variable Compatible">Temperature</Qualifier>
      <Qualifier name="Symbol">Cᵥ</Qualifier>
      <ParameterValue parameter="pa0" format="float">
        <Data>10.0, 20.0, 30.0</Data>
        <Qualifier name="Variable Type">Dependent,Dependent,Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa1" format="float">
        <Data>22.0, 40.0, 60.0</Data>
        <Qualifier name="Variable Type">Independent,Independent,Independent</Qualifier>
        <Qualifier name="Field Variable">Temperature</Qualifier>
        <Qualifier name="Default Data">22.0</Qualifier>
        <Qualifier name="Field Units">C</Qualifier>
        <Qualifier name="Upper Limit">Program Controlled</Qualifier>
        <Qualifier name="Lower Limit">Program Controlled</Qualifier>
      </ParameterValue>
    </PropertyData>
  </BulkDetails>
</Material>"""

SPECIFIC_HEAT_PRESSURE = """<?xml version="1.0" ?>
<Material>
  <BulkDetails>
    <Name>material with specific heat pressure</Name>
    <PropertyData property="pr0">
      <Data format="string">-</Data>
      <Qualifier name="Definition">Constant Pressure</Qualifier>
      <Qualifier name="Field Variable Compatible">Temperature</Qualifier>
      <Qualifier name="Symbol">Cᵨ</Qualifier>
      <ParameterValue parameter="pa0" format="float">
        <Data>1.0</Data>
        <Qualifier name="Variable Type">Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa1" format="float">
        <Data>22.0</Data>
        <Qualifier name="Variable Type">Independent</Qualifier>
        <Qualifier name="Field Variable">Temperature</Qualifier>
        <Qualifier name="Default Data">22.0</Qualifier>
        <Qualifier name="Field Units">C</Qualifier>
        <Qualifier name="Upper Limit">Program Controlled</Qualifier>
        <Qualifier name="Lower Limit">Program Controlled</Qualifier>
      </ParameterValue>
    </PropertyData>
  </BulkDetails>
</Material>"""

SPECIFIC_HEAT_PRESSURE_VARIABLE = """<?xml version="1.0" ?>
<Material>
  <BulkDetails>
    <Name>material with variable specific heat pressure</Name>
    <PropertyData property="pr0">
      <Data format="string">-</Data>
      <Qualifier name="Definition">Constant Pressure</Qualifier>
      <Qualifier name="Field Variable Compatible">Temperature</Qualifier>
      <Qualifier name="Symbol">Cᵨ</Qualifier>
      <ParameterValue parameter="pa0" format="float">
        <Data>1.0, 2.0, 3.0</Data>
        <Qualifier name="Variable Type">Dependent,Dependent,Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa1" format="float">
        <Data>22.0, 40.0, 60.0</Data>
        <Qualifier name="Variable Type">Independent,Independent,Independent</Qualifier>
        <Qualifier name="Field Variable">Temperature</Qualifier>
        <Qualifier name="Default Data">22.0</Qualifier>
        <Qualifier name="Field Units">C</Qualifier>
        <Qualifier name="Upper Limit">Program Controlled</Qualifier>
        <Qualifier name="Lower Limit">Program Controlled</Qualifier>
      </ParameterValue>
    </PropertyData>
  </BulkDetails>
</Material>"""

SPECIFIC_HEAT_METADATA = """<?xml version="1.0" ?>
<Metadata>
  <PropertyDetails id="pr0">
    <Unitless/>
    <Name>Specific Heat</Name>
  </PropertyDetails>
  <ParameterDetails id="pa0">
    <Unitless/>
    <Name>Specific Heat</Name>
  </ParameterDetails>
  <ParameterDetails id="pa1">
    <Unitless/>
    <Name>Temperature</Name>
  </ParameterDetails>
</Metadata>"""


def test_read_constant_specific_heat_volume():
    material_dic = read_matml_file(XML_FILE_PATH)
    material_name = "material with specific heat volume"
    assert material_name in material_dic.keys()
    assert len(material_dic[material_name].models) == 2
    specific_heat = material_dic[material_name].models[1]
    assert specific_heat.name == "Specific Heat"
    assert specific_heat.model_qualifiers[0].name == "Definition"
    assert specific_heat.model_qualifiers[0].value == "Constant Volume"
    assert specific_heat.model_qualifiers[1].name == "Field Variable Compatible"
    assert specific_heat.model_qualifiers[1].value == "Temperature"
    assert specific_heat.model_qualifiers[2].name == "Symbol"
    assert specific_heat.model_qualifiers[2].value == "Cᵥ"
    assert specific_heat.independent_parameters[0].name == "Temperature"
    assert specific_heat.independent_parameters[0].values == [22.0]
    assert specific_heat.independent_parameters[0].unit == "C"
    assert specific_heat.independent_parameters[0].upper_limit == "Program Controlled"
    assert specific_heat.independent_parameters[0].lower_limit == "Program Controlled"
    assert specific_heat.independent_parameters[0].default_value == 22.0
    assert specific_heat.specific_heat == [2.0]


def test_read_variable_specific_heat_volume():
    material_dic = read_matml_file(XML_FILE_PATH)
    material_name = "material with variable specific heat volume"
    assert material_name in material_dic.keys()
    assert len(material_dic[material_name].models) == 2
    specific_heat = material_dic[material_name].models[1]
    assert specific_heat.name == "Specific Heat"
    assert specific_heat.model_qualifiers[0].name == "Definition"
    assert specific_heat.model_qualifiers[0].value == "Constant Volume"
    assert specific_heat.model_qualifiers[1].name == "Field Variable Compatible"
    assert specific_heat.model_qualifiers[1].value == "Temperature"
    assert specific_heat.model_qualifiers[2].name == "Symbol"
    assert specific_heat.model_qualifiers[2].value == "Cᵥ"
    assert specific_heat.independent_parameters[0].name == "Temperature"
    assert specific_heat.independent_parameters[0].values == [22.0, 40.0, 60.0]
    assert specific_heat.independent_parameters[0].unit == "C"
    assert specific_heat.independent_parameters[0].upper_limit == "Program Controlled"
    assert specific_heat.independent_parameters[0].lower_limit == "Program Controlled"
    assert specific_heat.independent_parameters[0].default_value == 22.0
    assert specific_heat.specific_heat == [10.0, 20.0, 30.0]


def test_read_constant_specific_heat_pressure():
    material_dic = read_matml_file(XML_FILE_PATH)
    material_name = "material with specific heat pressure"
    assert material_name in material_dic.keys()
    assert len(material_dic[material_name].models) == 2
    specific_heat = material_dic[material_name].models[1]
    assert specific_heat.name == "Specific Heat"
    assert specific_heat.model_qualifiers[0].name == "Definition"
    assert specific_heat.model_qualifiers[0].value == "Constant Pressure"
    assert specific_heat.model_qualifiers[1].name == "Field Variable Compatible"
    assert specific_heat.model_qualifiers[1].value == "Temperature"
    assert specific_heat.model_qualifiers[2].name == "Symbol"
    assert specific_heat.model_qualifiers[2].value == "Cᵨ"
    assert specific_heat.independent_parameters[0].name == "Temperature"
    assert specific_heat.independent_parameters[0].values == [22.0]
    assert specific_heat.independent_parameters[0].unit == "C"
    assert specific_heat.independent_parameters[0].upper_limit == "Program Controlled"
    assert specific_heat.independent_parameters[0].lower_limit == "Program Controlled"
    assert specific_heat.independent_parameters[0].default_value == 22.0
    assert specific_heat.specific_heat == [1.0]
    assert specific_heat.interpolation_options.algorithm_type == "Linear Multivariate"
    assert specific_heat.interpolation_options.cached is True
    assert specific_heat.interpolation_options.normalized is True
    assert (
        specific_heat.interpolation_options.extrapolation_type == "Projection to the Bounding Box"
    )


def test_read_variable_specific_heat_pressure():
    material_dic = read_matml_file(XML_FILE_PATH)
    material_name = "material with variable specific heat pressure"
    assert material_name in material_dic.keys()
    assert len(material_dic[material_name].models) == 2
    specific_heat = material_dic[material_name].models[1]
    assert specific_heat.name == "Specific Heat"
    assert specific_heat.model_qualifiers[0].name == "Definition"
    assert specific_heat.model_qualifiers[0].value == "Constant Pressure"
    assert specific_heat.model_qualifiers[1].name == "Field Variable Compatible"
    assert specific_heat.model_qualifiers[1].value == "Temperature"
    assert specific_heat.model_qualifiers[2].name == "Symbol"
    assert specific_heat.model_qualifiers[2].value == "Cᵨ"
    assert specific_heat.independent_parameters[0].name == "Temperature"
    assert specific_heat.independent_parameters[0].values == [22.0, 50.0, 75.0]
    assert specific_heat.independent_parameters[0].unit == "C"
    assert specific_heat.independent_parameters[0].upper_limit == "Program Controlled"
    assert specific_heat.independent_parameters[0].lower_limit == "Program Controlled"
    assert specific_heat.independent_parameters[0].default_value == 22.0
    assert specific_heat.specific_heat == [1.0, 2.0, 3.0]
    assert specific_heat.interpolation_options.algorithm_type == "Linear Multivariate"
    assert specific_heat.interpolation_options.cached is True
    assert specific_heat.interpolation_options.normalized is True
    assert (
        specific_heat.interpolation_options.extrapolation_type == "Projection to the Bounding Box"
    )


def test_write_constant_specific_heat_volume():
    materials = [
        Material(
            name="material with specific heat volume",
            models=[
                SpecificHeat(
                    model_qualifiers=[
                        ModelQualifier(name="Definition", value="Constant Volume"),
                        ModelQualifier(name="Field Variable Compatible", value="Temperature"),
                        ModelQualifier(name="Symbol", value="Cᵥ"),
                    ],
                    specific_heat=[2.0],
                    independent_parameters=[
                        IndependentParameter(
                            name="Temperature",
                            field_variable="Temperature",
                            values=[22.0],
                            unit="C",
                            default_value=22.0,
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
    assert material_string == SPECIFIC_HEAT_VOLUME
    assert metadata_string == SPECIFIC_HEAT_METADATA


def test_write_variable_specific_heat_volume():
    materials = [
        Material(
            name="material with variable specific heat volume",
            models=[
                SpecificHeat(
                    model_qualifiers=[
                        ModelQualifier(name="Definition", value="Constant Volume"),
                        ModelQualifier(name="Field Variable Compatible", value="Temperature"),
                        ModelQualifier(name="Symbol", value="Cᵥ"),
                    ],
                    specific_heat=[10.0, 20.0, 30.0],
                    independent_parameters=[
                        IndependentParameter(
                            name="Temperature",
                            field_variable="Temperature",
                            values=[22.0, 40.0, 60.0],
                            unit="C",
                            default_value=22.0,
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
    assert material_string == SPECIFIC_HEAT_VOLUME_VARIABLE
    assert metadata_string == SPECIFIC_HEAT_METADATA


def test_write_constant_specific_heat_pressure():
    materials = [
        Material(
            name="material with specific heat pressure",
            models=[
                SpecificHeat(
                    model_qualifiers=[
                        ModelQualifier(name="Definition", value="Constant Pressure"),
                        ModelQualifier(name="Field Variable Compatible", value="Temperature"),
                        ModelQualifier(name="Symbol", value="Cᵨ"),
                    ],
                    specific_heat=[1.0],
                    independent_parameters=[
                        IndependentParameter(
                            name="Temperature",
                            field_variable="Temperature",
                            values=[22.0],
                            unit="C",
                            default_value=22.0,
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
    assert material_string == SPECIFIC_HEAT_PRESSURE
    assert metadata_string == SPECIFIC_HEAT_METADATA


def test_write_variable_specific_heat_pressure():
    materials = [
        Material(
            name="material with variable specific heat pressure",
            models=[
                SpecificHeat(
                    model_qualifiers=[
                        ModelQualifier(name="Definition", value="Constant Pressure"),
                        ModelQualifier(name="Field Variable Compatible", value="Temperature"),
                        ModelQualifier(name="Symbol", value="Cᵨ"),
                    ],
                    specific_heat=[1.0, 2.0, 3.0],
                    independent_parameters=[
                        IndependentParameter(
                            name="Temperature",
                            field_variable="Temperature",
                            values=[22.0, 40.0, 60.0],
                            unit="C",
                            default_value=22.0,
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
    assert material_string == SPECIFIC_HEAT_PRESSURE_VARIABLE
    assert metadata_string == SPECIFIC_HEAT_METADATA
