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

from utilities import get_material_and_metadata_from_xml, read_specific_material

from ansys.materials.manager._models._common import IndependentParameter
from ansys.materials.manager._models._material_models.strain_limits_isotropic import (
    StrainLimitsIsotropic,
)
from ansys.materials.manager._models._material_models.strain_limits_orthotropic import (
    StrainLimitsOrthotropic,
)
from ansys.materials.manager._models.material import Material
from ansys.materials.manager.util.matml.matml_from_material import MatmlWriter

from ansys.units import Quantity

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
XML_FILE_PATH = os.path.join(DIR_PATH, "..", "data", "matml_unittest_strain_limit.xml")
STRAIN_LIMITS_ORTHOTROPIC = os.path.join(DIR_PATH, "..", "data", "matml_strain_limits_orthotropic.txt")
STRAIN_LIMITS_ORTHOTROPIC_METADATA = os.path.join(DIR_PATH, "..", "data", "matml_strain_limits_orthotropic_metadata.txt")
STRAIN_LIMITS_ISOTROPIC = os.path.join(DIR_PATH, "..", "data", "matml_strain_limits_isotropic.txt")
STRAIN_LIMITS_ISOTROPIC_METADATA = os.path.join(DIR_PATH, "..", "data", "matml_strain_limits_isotropic_metadata.txt")
STRAIN_LIMITS_ISOTROPIC_VARIABLE = os.path.join(DIR_PATH, "..", "data", "matml_strain_limits_isotropic_variable.txt")
STRAIN_LIMITS_ORTHOTROPIC_VARIABLE = os.path.join(DIR_PATH, "..", "data", "matml_strain_limits_orthotropic_variable.txt")

def test_read_constant_strain_limit_isotropic():
    material = read_specific_material(XML_FILE_PATH, "isotropic material with strain limit")
    assert len(material.models) == 2
    isotropic_strain_limits = material.models[1]
    assert isotropic_strain_limits.name == "Strain Limits"
    assert isotropic_strain_limits.model_qualifiers[0].name == "Behavior"
    assert isotropic_strain_limits.model_qualifiers[0].value == "Isotropic"
    assert isotropic_strain_limits.von_mises.value == [213]
    assert isotropic_strain_limits.von_mises.unit == ""
    assert isotropic_strain_limits.independent_parameters[0].name == "Temperature"
    assert isotropic_strain_limits.independent_parameters[0].values.value.tolist() == [7.88860905221012e-31]
    assert isotropic_strain_limits.independent_parameters[0].values.unit == "C"

def test_read_variable_strain_limit_isotropic():
    material = read_specific_material(XML_FILE_PATH, "isotropic material with variable strain limit")
    assert len(material.models) == 2
    isotropic_strain_limits = material.models[1]
    assert isotropic_strain_limits.name == "Strain Limits"
    assert isotropic_strain_limits.model_qualifiers[0].name == "Behavior"
    assert isotropic_strain_limits.model_qualifiers[0].value == "Isotropic"
    assert isotropic_strain_limits.von_mises.value.tolist() == [2333, 2324, 2432]
    assert isotropic_strain_limits.von_mises.unit == ""
    assert isotropic_strain_limits.independent_parameters[0].name == "Temperature"
    assert isotropic_strain_limits.independent_parameters[0].values.value.tolist() == [23, 25, 27]
    assert isotropic_strain_limits.independent_parameters[0].values.unit == "C"

def test_read_constant_strain_limit_orthotropic():
    material = read_specific_material(XML_FILE_PATH, "orthotropic material with strain limit")
    assert len(material.models) == 2
    orthotropic_strain_limits = material.models[1]
    assert orthotropic_strain_limits.name == "Strain Limits"
    assert orthotropic_strain_limits.model_qualifiers[0].name == "Behavior"
    assert orthotropic_strain_limits.model_qualifiers[0].value == "Orthotropic"
    assert orthotropic_strain_limits.model_qualifiers[1].name == "Field Variable Compatible"
    assert orthotropic_strain_limits.model_qualifiers[1].value == "Temperature"
    assert orthotropic_strain_limits.interpolation_options.algorithm_type == "Linear Multivariate"
    assert orthotropic_strain_limits.interpolation_options.cached == True
    assert orthotropic_strain_limits.interpolation_options.normalized == True
    assert orthotropic_strain_limits.tensile_x_direction.value == [311.0]
    assert orthotropic_strain_limits.tensile_x_direction.unit == ""
    assert orthotropic_strain_limits.tensile_y_direction.value == [213.0]
    assert orthotropic_strain_limits.tensile_y_direction.unit == ""
    assert orthotropic_strain_limits.tensile_z_direction.value == [13.0]
    assert orthotropic_strain_limits.tensile_z_direction.unit == ""
    assert orthotropic_strain_limits.compressive_x_direction.value == [-132.0]
    assert orthotropic_strain_limits.compressive_x_direction.unit == ""
    assert orthotropic_strain_limits.compressive_y_direction.value == [-13.0]
    assert orthotropic_strain_limits.compressive_y_direction.unit == ""
    assert orthotropic_strain_limits.compressive_z_direction.value == [-13.0]
    assert orthotropic_strain_limits.compressive_z_direction.unit == ""
    assert orthotropic_strain_limits.shear_xy.value == [24.0]
    assert orthotropic_strain_limits.shear_xy.unit == ""
    assert orthotropic_strain_limits.shear_xz.value == [12.0]
    assert orthotropic_strain_limits.shear_xz.unit == ""
    assert orthotropic_strain_limits.shear_yz.value == [232.0]
    assert orthotropic_strain_limits.shear_yz.unit == ""
    assert orthotropic_strain_limits.independent_parameters[0].name == "Temperature"
    assert orthotropic_strain_limits.independent_parameters[0].values.value == [7.88860905221012e-31]
    assert orthotropic_strain_limits.independent_parameters[0].values.unit == "C"
    assert orthotropic_strain_limits.independent_parameters[0].field_units == "C"
    assert orthotropic_strain_limits.independent_parameters[0].upper_limit == "Program Controlled"
    assert orthotropic_strain_limits.independent_parameters[0].lower_limit == "Program Controlled"
    assert orthotropic_strain_limits.independent_parameters[0].default_value == 22.0


def test_read_variable_strain_limit_orthotropic():
    material = read_specific_material(XML_FILE_PATH, "orthotropic material with variable strain limit")
    assert len(material.models) == 2
    orthotropic_strain_limits = material.models[1]
    assert orthotropic_strain_limits.name == "Strain Limits"
    assert orthotropic_strain_limits.model_qualifiers[0].name == "Behavior"
    assert orthotropic_strain_limits.model_qualifiers[0].value == "Orthotropic"
    assert orthotropic_strain_limits.model_qualifiers[1].name == "Field Variable Compatible"
    assert orthotropic_strain_limits.model_qualifiers[1].value == "Temperature"
    assert orthotropic_strain_limits.interpolation_options.algorithm_type == "Linear Multivariate"
    assert orthotropic_strain_limits.interpolation_options.cached == True
    assert orthotropic_strain_limits.interpolation_options.normalized == True
    assert orthotropic_strain_limits.tensile_x_direction.value.tolist() == [324.0, 311.0, 312.0]
    assert orthotropic_strain_limits.tensile_x_direction.unit == ""
    assert orthotropic_strain_limits.tensile_y_direction.value.tolist() == [236.0, 213.0, 234.0]
    assert orthotropic_strain_limits.tensile_y_direction.unit == ""
    assert orthotropic_strain_limits.tensile_z_direction.value.tolist() == [15.0, 13.0, 14.0]
    assert orthotropic_strain_limits.tensile_z_direction.unit == ""
    assert orthotropic_strain_limits.compressive_x_direction.value.tolist() == [-110.0, -132.0, -120.0]
    assert orthotropic_strain_limits.compressive_x_direction.unit == ""
    assert orthotropic_strain_limits.compressive_y_direction.value.tolist() == [-11.0, -13.0, -12.0]
    assert orthotropic_strain_limits.compressive_y_direction.unit == ""
    assert orthotropic_strain_limits.compressive_z_direction.value.tolist() == [-9.0, -13.0, -11.0]
    assert orthotropic_strain_limits.compressive_z_direction.unit == ""
    assert orthotropic_strain_limits.shear_xy.value.tolist() == [26.0, 24.0, 25.0]
    assert orthotropic_strain_limits.shear_xy.unit == ""
    assert orthotropic_strain_limits.shear_xz.value.tolist() == [16.0, 12.0, 14.0]
    assert orthotropic_strain_limits.shear_xz.unit == ""
    assert orthotropic_strain_limits.shear_yz.value.tolist() == [255.0, 232.0, 244.0]
    assert orthotropic_strain_limits.shear_yz.unit == ""
    assert orthotropic_strain_limits.independent_parameters[0].name == "Temperature"
    assert orthotropic_strain_limits.independent_parameters[0].values.value.tolist() == [13.0, 21.0, 23.0]
    assert orthotropic_strain_limits.independent_parameters[0].values.unit == "C"
    assert orthotropic_strain_limits.independent_parameters[0].field_units == "C"
    assert orthotropic_strain_limits.independent_parameters[0].upper_limit == "Program Controlled"
    assert orthotropic_strain_limits.independent_parameters[0].lower_limit == "Program Controlled"
    assert orthotropic_strain_limits.independent_parameters[0].default_value == 22.0


def test_write_constant_strain_limits_orthotropic():
    materials = [
        Material(
            name="orthotropic material with strain limit",
            models=[
                StrainLimitsOrthotropic(
                    compressive_x_direction=Quantity(value=[-132.0], units=""),
                    compressive_y_direction=Quantity(value=[-13.0], units=""),
                    compressive_z_direction=Quantity(value=[-13.0], units=""),
                    tensile_x_direction=Quantity(value=[311.0], units=""),
                    tensile_y_direction=Quantity(value=[213.0], units=""),
                    tensile_z_direction=Quantity(value=[13.0], units=""),
                    shear_xy=Quantity(value=[24.0], units=""),
                    shear_xz=Quantity(value=[12.0], units=""),
                    shear_yz=Quantity(value=[232.0], units=""),
                    independent_parameters=[
                        IndependentParameter(
                            name="Temperature",
                            field_variable="Temperature",
                            values=Quantity(value=[7.88860905221012e-31], units="C"),
                            field_units="C",
                            upper_limit="Program Controlled",
                            lower_limit="Program Controlled",
                            default_value=22.0,
                        )
                    ],
                ),
            ],
        )
    ]

    writer = MatmlWriter(materials)
    tree = writer._to_etree()
    material_string, metadata_string = get_material_and_metadata_from_xml(tree)
    with open(STRAIN_LIMITS_ORTHOTROPIC, 'r', encoding="utf8") as file:
        data = file.read()
        assert data == material_string
    with open(STRAIN_LIMITS_ORTHOTROPIC_METADATA, 'r') as file:
      data = file.read()
      assert data == metadata_string


def test_write_constant_strain_limits_isotropic():
    materials = [
        Material(
            name="isotropic material with strain limit",
            models=[
                StrainLimitsIsotropic(
                    von_mises=Quantity(value=[213], units=""),
                    independent_parameters=[
                        IndependentParameter(name="Temperature", values=Quantity(value=[7.88860905221012e-31], units="C"))
                    ],
                ),
            ],
        )
    ]
    writer = MatmlWriter(materials)
    tree = writer._to_etree()
    material_string, metadata_string = get_material_and_metadata_from_xml(tree)
    with open(STRAIN_LIMITS_ISOTROPIC, 'r', encoding="utf8") as file:
        data = file.read()
        assert data == material_string
    with open(STRAIN_LIMITS_ISOTROPIC_METADATA, 'r') as file:
      data = file.read()
      assert data == metadata_string



def test_write_variable_strain_limits_isotropic():
    materials = [
        Material(
            name="isotropic material with variable strain limit",
            models=[
                StrainLimitsIsotropic(
                    von_mises=Quantity(value=[2333, 2324, 2432], units=""),
                    independent_parameters=[
                        IndependentParameter(name="Temperature", values=Quantity(value=[23, 25, 27], units="C"))
                    ],
                ),
            ],
        )
    ]
    writer = MatmlWriter(materials)
    tree = writer._to_etree()
    material_string, metadata_string = get_material_and_metadata_from_xml(tree)
    with open(STRAIN_LIMITS_ISOTROPIC_VARIABLE, 'r', encoding="utf8") as file:
        data = file.read()
        assert data == material_string
    with open(STRAIN_LIMITS_ISOTROPIC_METADATA, 'r') as file:
      data = file.read()
      assert data == metadata_string


def test_write_variable_strain_limits_orthotropic():
    materials = [
        Material(
            name="orthotropic material with variable strain limit",
            models=[
                StrainLimitsOrthotropic(
                    tensile_x_direction=Quantity(value=[324.0, 311.0, 312.0], units=""),
                    tensile_y_direction=Quantity(value=[236.0, 213.0, 234.0], units=""),
                    tensile_z_direction=Quantity(value=[15.0, 13.0, 14.0], units=""),
                    compressive_x_direction=Quantity(value=[-110.0, -132.0, -120.0], units=""),
                    compressive_y_direction=Quantity(value=[-11.0, -13.0, -12.0], units=""),
                    compressive_z_direction=Quantity(value=[-9.0, -13.0, -11.0], units=""),
                    shear_xy=Quantity(value=[26.0, 24.0, 25.0], units=""),
                    shear_xz=Quantity(value=[16.0, 12.0, 14.0], units=""),
                    shear_yz=Quantity(value=[255.0, 232.0, 244.0], units=""),
                    independent_parameters=[
                        IndependentParameter(
                            name="Temperature",
                            values=Quantity(value=[13.0, 21.0, 23.0], units="C"),
                            field_units="C",
                            upper_limit="Program Controlled",
                            lower_limit="Program Controlled",
                            default_value=22.0,
                        )
                    ],
                ),
            ],
        )
    ]

    writer = MatmlWriter(materials)
    tree = writer._to_etree()
    material_string, metadata_string = get_material_and_metadata_from_xml(tree)
    with open(STRAIN_LIMITS_ORTHOTROPIC_VARIABLE, 'r', encoding="utf8") as file:
        data = file.read()
        assert data == material_string
    with open(STRAIN_LIMITS_ORTHOTROPIC_METADATA, 'r') as file:
      data = file.read()
      assert data == metadata_string

# writer = MatmlWriter(materials)
# tree = writer._to_etree()
# material_string, metadata_string = get_material_and_metadata_from_xml(tree)
# path = r"D:\AnsysDev\pymaterials-manager\tests\data"
# writer.export("trial.xml", indent=True)
# with open(path + "\\strain_limit_orthotropic_variable.txt", 'w') as file:
#   file.write(material_string)
# with open(path + "\\strain_limit_isotropic_metadata.txt", 'w') as file:
#   file.write(metadata_string)