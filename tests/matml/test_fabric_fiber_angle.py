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

from ansys.units import Quantity

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
XML_FILE_PATH = os.path.join(DIR_PATH, "..", "data", "MatML_unittest_fabric_fiber_angle.xml")

FABRIC_FIBER_ANGLE = os.path.join(DIR_PATH, "..", "data", "fabric_fiber_angle.txt")
FABRIC_FIBER_ANGLE_METADATA = os.path.join(DIR_PATH, "..", "data", "fabric_fiber_angle_metadata.txt")
FABRIC_FIBER_ANGLE_VARIABLE = os.path.join(DIR_PATH, "..", "data", "fabric_fiber_angle_variable.txt")
FABRIC_FIBER_ANGLE_VARIABLE_METADATA = os.path.join(DIR_PATH, "..", "data", "fabric_fiber_angle_variable_metadata.txt")
PLY_TYPE = os.path.join(DIR_PATH, "..", "data", "ply_type.txt")
PLY_TYPE_METADATA = os.path.join(DIR_PATH, "..", "data", "ply_type_metadata.txt")

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
    assert fabric_fiber_angle.fabric_fiber_angle.value == [0.0]
    assert fabric_fiber_angle.fabric_fiber_angle.unit == "degree"
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
    assert fabric_fiber_angle.fabric_fiber_angle.value == [35.0]
    assert fabric_fiber_angle.fabric_fiber_angle.unit == "degree"
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
    assert fabric_fiber_angle.fabric_fiber_angle.value == [45.0]
    assert fabric_fiber_angle.fabric_fiber_angle.unit == "degree"
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
    assert fabric_fiber_angle.fabric_fiber_angle.value.tolist() == [55, 52.5, 50, 47.5, 45, 42.5, 40, 37.5, 35]
    assert fabric_fiber_angle.fabric_fiber_angle.unit == "degree"
    assert fabric_fiber_angle.independent_parameters[0].name == "Shear Angle"
    assert fabric_fiber_angle.independent_parameters[0].values.value.tolist() == [
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
    assert fabric_fiber_angle.independent_parameters[0].values.unit == "radian"
    assert fabric_fiber_angle.independent_parameters[0].upper_limit == 0.349065850398866
    assert fabric_fiber_angle.independent_parameters[0].lower_limit == -0.3490658503988659
    assert fabric_fiber_angle.independent_parameters[0].default_value == 0.0
    assert fabric_fiber_angle.independent_parameters[0].field_variable == "Shear Angle"
    assert fabric_fiber_angle.independent_parameters[0].field_units == "radian"


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
                    fabric_fiber_angle=Quantity(value=[0.0], units="degree"),
                ),
            ],
        )
    ]
    writer = MatmlWriter(materials)
    tree = writer._to_etree()
    material_string, metadata_string = get_material_and_metadata_from_xml(tree)
    with open(FABRIC_FIBER_ANGLE, 'r') as file:
        data = file.read()
        assert data == material_string
    with open(FABRIC_FIBER_ANGLE_METADATA, 'r') as file:
      data = file.read()
      assert data == metadata_string

def test_write_variable_fabric_fiber_angle():
    materials = [
        Material(
            name="Variable Plain woven Resin Epoxy/UD Resin Epoxy/T300 Typical 65%",
            models=[
                FabricFiberAngle(
                    fabric_fiber_angle=Quantity(value=[55.0, 52.5, 50.0, 47.5, 45.0, 42.5, 40.0, 37.5, 35.0], units="degree"),
                    independent_parameters=[
                        IndependentParameter(
                            name="Shear Angle",
                            default_value=0.0,
                            upper_limit=0.349065850398866,
                            lower_limit=-0.3490658503988659,
                            values=Quantity(value=[
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
                            units="radian"),
                            field_variable="Shear Angle",
                            field_units="radian",
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
    with open(FABRIC_FIBER_ANGLE_VARIABLE, 'r') as file:
        data = file.read()
        assert data == material_string
    with open(FABRIC_FIBER_ANGLE_VARIABLE_METADATA, 'r') as file:
      data = file.read()
      assert data == metadata_string


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
    with open(PLY_TYPE, 'r') as file:
        data = file.read()
        assert data == material_string
    with open(PLY_TYPE_METADATA, 'r') as file:
      data = file.read()
      assert data == metadata_string