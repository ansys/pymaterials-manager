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
from ansys.materials.manager._models._common.interpolation_options import InterpolationOptions
from ansys.materials.manager._models._common.model_qualifier import ModelQualifier
from ansys.materials.manager._models._material_models.fabric_fiber_angle import FabricFiberAngle
from ansys.materials.manager._models._material_models.ply_type import PlyType
from ansys.materials.manager._models.material import Material
from ansys.materials.manager.util.matml.matml_from_material import MatmlWriter

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
XML_FILE_PATH = os.path.join(DIR_PATH, "..", "data", "MatML_unittest_fabric_fiber_angle.xml")

FABRIC_FIBER_ANGLE = """<?xml version="1.0" ?>
<Material>
  <BulkDetails>
    <Name>Plain woven Resin Epoxy/UD Resin Epoxy/T300 Typical 65%; angle=0</Name>
    <PropertyData property="pr0">
      <Data format="string">-</Data>
      <ParameterValue parameter="pa0" format="float">
        <Data>0.0</Data>
        <Qualifier name="Variable Type">Dependent</Qualifier>
      </ParameterValue>
    </PropertyData>
  </BulkDetails>
</Material>"""

FABRIC_FIBER_ANGLE_VARIABLE = """<?xml version="1.0" ?>
<Material>
  <BulkDetails>
    <Name>Variable Plain woven Resin Epoxy/UD Resin Epoxy/T300 Typical 65%</Name>
    <PropertyData property="pr0">
      <Data format="string">-</Data>
      <ParameterValue parameter="pa0" format="string">
        <Data>Interpolation Options</Data>
        <Qualifier name="AlgorithmType">Linear Multivariate</Qualifier>
        <Qualifier name="Cached">True</Qualifier>
        <Qualifier name="Normalized">True</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa1" format="float">
        <Data>55.0, 52.5, 50.0, 47.5, 45.0, 42.5, 40.0, 37.5, 35.0</Data>
        <Qualifier name="Variable Type">Dependent,Dependent,Dependent,Dependent,Dependent,Dependent,Dependent,Dependent,Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa2" format="float">
        <Data>-0.349065850398866, -0.261799387799149, -0.174532925199433, -0.0872664625997165, 0.0, 0.0872664625997165, 0.174532925199433, 0.261799387799149, 0.349065850398866</Data>
        <Qualifier name="Variable Type">Independent,Independent,Independent,Independent,Independent,Independent,Independent,Independent,Independent</Qualifier>
        <Qualifier name="Field Variable">Shear Angle</Qualifier>
        <Qualifier name="Default Data">0.0</Qualifier>
        <Qualifier name="Field Units">radian</Qualifier>
        <Qualifier name="Upper Limit">0.349065850398866</Qualifier>
        <Qualifier name="Lower Limit">-0.3490658503988659</Qualifier>
      </ParameterValue>
    </PropertyData>
  </BulkDetails>
</Material>"""  # noqa: E501

PLY_TYPE = """<?xml version="1.0" ?>
<Material>
  <BulkDetails>
    <Name>Plain woven Resin Epoxy/UD Resin Epoxy/T300 Typical 65%; angle=0</Name>
    <PropertyData property="pr0">
      <Data format="string">-</Data>
      <Qualifier name="source">ACP</Qualifier>
      <Qualifier name="Type">Woven</Qualifier>
    </PropertyData>
  </BulkDetails>
</Material>"""

FABRIC_FIBER_ANGLE_METADATA = """<?xml version="1.0" ?>
<Metadata>
  <PropertyDetails id="pr0">
    <Unitless/>
    <Name>Fabric Fiber Angle</Name>
  </PropertyDetails>
  <ParameterDetails id="pa0">
    <Unitless/>
    <Name>Options Variable</Name>
  </ParameterDetails>
  <ParameterDetails id="pa1">
    <Unitless/>
    <Name>Fabric Fiber Angle</Name>
  </ParameterDetails>
  <ParameterDetails id="pa2">
    <Unitless/>
    <Name>Shear Angle</Name>
  </ParameterDetails>
</Metadata>"""

PLY_TYPE_METADATA = """<?xml version="1.0" ?>
<Metadata>
  <PropertyDetails id="pr0">
    <Unitless/>
    <Name>Ply Type</Name>
  </PropertyDetails>
</Metadata>"""


def test_read_constant_fabric_fiber_angle_0_deg():
    material_dic = read_matml_file(XML_FILE_PATH)
    assert "Plain woven Resin Epoxy/UD Resin Epoxy/T300 Typical 65%; angle=0" in material_dic.keys()
    assert (
        len(material_dic["Plain woven Resin Epoxy/UD Resin Epoxy/T300 Typical 65%; angle=0"].models)
        == 5
    )
    fabric_fiber_angle = material_dic[
        "Plain woven Resin Epoxy/UD Resin Epoxy/T300 Typical 65%; angle=0"
    ].models[3]
    assert fabric_fiber_angle.name == "Fabric Fiber Angle"
    assert fabric_fiber_angle.model_qualifiers[0].name == "Field Variable Compatible"
    assert fabric_fiber_angle.model_qualifiers[0].value == "Temperature"
    assert fabric_fiber_angle.interpolation_options.algorithm_type == "Linear Multivariate"
    assert fabric_fiber_angle.interpolation_options.cached == True
    assert fabric_fiber_angle.interpolation_options.normalized == True
    assert fabric_fiber_angle.fabric_fiber_angle == [0.0]
    assert fabric_fiber_angle.independent_parameters == []


def test_read_constant_fabric_fiber_angle_35_deg():
    material_dic = read_matml_file(XML_FILE_PATH)
    assert (
        "Plain woven Resin Epoxy/UD Resin Epoxy/T300 Typical 65%; angle=35" in material_dic.keys()
    )
    assert (
        len(
            material_dic["Plain woven Resin Epoxy/UD Resin Epoxy/T300 Typical 65%; angle=35"].models
        )
        == 5
    )
    fabric_fiber_angle = material_dic[
        "Plain woven Resin Epoxy/UD Resin Epoxy/T300 Typical 65%; angle=35"
    ].models[3]
    assert fabric_fiber_angle.name == "Fabric Fiber Angle"
    assert fabric_fiber_angle.model_qualifiers[0].name == "Field Variable Compatible"
    assert fabric_fiber_angle.model_qualifiers[0].value == "Temperature"
    assert fabric_fiber_angle.interpolation_options.algorithm_type == "Linear Multivariate"
    assert fabric_fiber_angle.interpolation_options.cached == True
    assert fabric_fiber_angle.interpolation_options.normalized == True
    assert fabric_fiber_angle.fabric_fiber_angle == [35.0]
    assert fabric_fiber_angle.independent_parameters == []


def test_read_constant_fabric_fiber_angle_45_deg():
    material_dic = read_matml_file(XML_FILE_PATH)
    assert (
        "Plain woven Resin Epoxy/UD Resin Epoxy/T300 Typical 65%; angle=45" in material_dic.keys()
    )
    assert (
        len(
            material_dic["Plain woven Resin Epoxy/UD Resin Epoxy/T300 Typical 65%; angle=45"].models
        )
        == 5
    )
    fabric_fiber_angle = material_dic[
        "Plain woven Resin Epoxy/UD Resin Epoxy/T300 Typical 65%; angle=45"
    ].models[3]
    assert fabric_fiber_angle.name == "Fabric Fiber Angle"
    assert fabric_fiber_angle.model_qualifiers[0].name == "Field Variable Compatible"
    assert fabric_fiber_angle.model_qualifiers[0].value == "Temperature"
    assert fabric_fiber_angle.interpolation_options.algorithm_type == "Linear Multivariate"
    assert fabric_fiber_angle.interpolation_options.cached == True
    assert fabric_fiber_angle.interpolation_options.normalized == True
    assert fabric_fiber_angle.fabric_fiber_angle == [45.0]
    assert fabric_fiber_angle.independent_parameters == []


def test_read_variable_fabric_fiber_angle():
    material_dic = read_matml_file(XML_FILE_PATH)
    assert "Variable Plain woven Resin Epoxy/UD Resin Epoxy/T300 Typical 65%" in material_dic.keys()
    assert (
        len(material_dic["Variable Plain woven Resin Epoxy/UD Resin Epoxy/T300 Typical 65%"].models)
        == 5
    )
    fabric_fiber_angle = material_dic[
        "Variable Plain woven Resin Epoxy/UD Resin Epoxy/T300 Typical 65%"
    ].models[3]
    assert fabric_fiber_angle.name == "Fabric Fiber Angle"
    assert fabric_fiber_angle.model_qualifiers[0].name == "Field Variable Compatible"
    assert fabric_fiber_angle.model_qualifiers[0].value == "Temperature"
    assert fabric_fiber_angle.interpolation_options.algorithm_type == "Linear Multivariate"
    assert fabric_fiber_angle.interpolation_options.cached == True
    assert fabric_fiber_angle.interpolation_options.normalized == True
    assert fabric_fiber_angle.fabric_fiber_angle == [55, 52.5, 50, 47.5, 45, 42.5, 40, 37.5, 35]
    assert fabric_fiber_angle.independent_parameters[0].name == "Shear Angle"
    assert fabric_fiber_angle.independent_parameters[0].values == [
        -0.349065850398866,
        -0.261799387799149,
        -0.174532925199433,
        -0.0872664625997165,
        0,
        0.0872664625997165,
        0.174532925199433,
        0.261799387799149,
        0.349065850398866,
    ]
    assert fabric_fiber_angle.independent_parameters[0].unit == "radian"
    assert fabric_fiber_angle.independent_parameters[0].upper_limit == 0.349065850398866
    assert fabric_fiber_angle.independent_parameters[0].lower_limit == -0.3490658503988659
    assert fabric_fiber_angle.independent_parameters[0].default_value == 0.0


def test_read_ply_type():
    material_dic = read_matml_file(XML_FILE_PATH)
    assert "Plain woven Resin Epoxy/UD Resin Epoxy/T300 Typical 65%; angle=0" in material_dic.keys()
    assert (
        len(material_dic["Plain woven Resin Epoxy/UD Resin Epoxy/T300 Typical 65%; angle=0"].models)
        == 5
    )
    ply_type = material_dic[
        "Plain woven Resin Epoxy/UD Resin Epoxy/T300 Typical 65%; angle=0"
    ].models[0]
    assert ply_type.name == "Ply Type"
    assert ply_type.model_qualifiers[0].name == "source"
    assert ply_type.model_qualifiers[0].value == "ACP"
    assert ply_type.model_qualifiers[1].name == "Type"
    assert ply_type.model_qualifiers[1].value == "Woven"


def test_write_constant_fabric_fiber_angle_0_deg():
    materials = [
        Material(
            name="Plain woven Resin Epoxy/UD Resin Epoxy/T300 Typical 65%; angle=0",
            models=[
                FabricFiberAngle(
                    fabric_fiber_angle=[0.0],
                ),
            ],
        )
    ]
    writer = MatmlWriter(materials)
    tree = writer._to_etree()
    material_string, _ = get_material_and_metadata_from_xml(tree)
    assert material_string == FABRIC_FIBER_ANGLE


def test_write_variable_fabric_fiber_angle():
    materials = [
        Material(
            name="Variable Plain woven Resin Epoxy/UD Resin Epoxy/T300 Typical 65%",
            models=[
                FabricFiberAngle(
                    fabric_fiber_angle=[55.0, 52.5, 50.0, 47.5, 45.0, 42.5, 40.0, 37.5, 35.0],
                    independent_parameters=[
                        IndependentParameter(
                            name="Shear Angle",
                            field_variable="Shear Angle",
                            default_value=0.0,
                            upper_limit=0.349065850398866,
                            lower_limit=-0.3490658503988659,
                            values=[
                                -0.349065850398866,
                                -0.261799387799149,
                                -0.174532925199433,
                                -0.0872664625997165,
                                0,
                                0.0872664625997165,
                                0.174532925199433,
                                0.261799387799149,
                                0.349065850398866,
                            ],
                            unit="radian",
                        )
                    ],
                    interpolation_options=InterpolationOptions(
                        algorithm_type="Linear Multivariate",
                        cached=True,
                        normalized=True,
                    ),
                ),
            ],
        )
    ]
    writer = MatmlWriter(materials)
    tree = writer._to_etree()
    material_string, metadata_string = get_material_and_metadata_from_xml(tree)
    assert material_string == FABRIC_FIBER_ANGLE_VARIABLE
    assert metadata_string == FABRIC_FIBER_ANGLE_METADATA


def test_write_ply_type():
    materials = [
        Material(
            name="Plain woven Resin Epoxy/UD Resin Epoxy/T300 Typical 65%; angle=0",
            models=[
                PlyType(
                    model_qualifiers=[
                        ModelQualifier(name="source", value="ACP"),
                        ModelQualifier(name="Type", value="Woven"),
                    ],
                ),
            ],
        )
    ]
    writer = MatmlWriter(materials)
    tree = writer._to_etree()
    material_string, metadata_string = get_material_and_metadata_from_xml(tree)
    assert material_string == PLY_TYPE
    assert metadata_string == PLY_TYPE_METADATA
