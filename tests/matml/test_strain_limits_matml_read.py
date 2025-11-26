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

from pathlib import Path

from ansys.materials.manager.parsers.matml.matml_reader import MatmlReader

DIR_PATH = Path(__file__).resolve().parent
XML_FILE_PATH = DIR_PATH.joinpath("..", "data", "matml_unittest_strain_limit.xml")
STRAIN_LIMITS_ORTHOTROPIC = DIR_PATH.joinpath("..", "data", "matml_strain_limits_orthotropic.txt")
STRAIN_LIMITS_ORTHOTROPIC_METADATA = DIR_PATH.joinpath(
    "..", "data", "matml_strain_limits_orthotropic_metadata.txt"
)
STRAIN_LIMITS_ISOTROPIC = DIR_PATH.joinpath("..", "data", "matml_strain_limits_isotropic.txt")
STRAIN_LIMITS_ISOTROPIC_METADATA = DIR_PATH.joinpath(
    "..", "data", "matml_strain_limits_isotropic_metadata.txt"
)
STRAIN_LIMITS_ISOTROPIC_VARIABLE = DIR_PATH.joinpath(
    "..", "data", "matml_strain_limits_isotropic_variable.txt"
)
STRAIN_LIMITS_ORTHOTROPIC_VARIABLE = DIR_PATH.joinpath(
    "..", "data", "matml_strain_limits_orthotropic_variable.txt"
)


def test_read_constant_strain_limit_isotropic():
    matml_reader = MatmlReader(XML_FILE_PATH)
    materials = matml_reader.convert_matml_materials()
    material = materials["isotropic material with strain limit"]
    assert len(material.models) == 1
    isotropic_strain_limits = material.models[0]
    assert isotropic_strain_limits.name == "Strain Limits"
    assert isotropic_strain_limits.model_qualifiers[0].name == "Behavior"
    assert isotropic_strain_limits.model_qualifiers[0].value == "Isotropic"
    assert isotropic_strain_limits.von_mises.value == [213]
    assert isotropic_strain_limits.von_mises.unit == ""
    assert isotropic_strain_limits.independent_parameters[0].name == "Temperature"
    assert isotropic_strain_limits.independent_parameters[0].values.value.tolist() == [
        7.88860905221012e-31
    ]
    assert isotropic_strain_limits.independent_parameters[0].values.unit == "C"


def test_read_variable_strain_limit_isotropic():
    matml_reader = MatmlReader(XML_FILE_PATH)
    materials = matml_reader.convert_matml_materials()
    material = materials["isotropic material with variable strain limit"]
    assert len(material.models) == 1
    isotropic_strain_limits = material.models[0]
    assert isotropic_strain_limits.name == "Strain Limits"
    assert isotropic_strain_limits.model_qualifiers[0].name == "Behavior"
    assert isotropic_strain_limits.model_qualifiers[0].value == "Isotropic"
    assert isotropic_strain_limits.von_mises.value.tolist() == [2333, 2324, 2432]
    assert isotropic_strain_limits.von_mises.unit == ""
    assert isotropic_strain_limits.independent_parameters[0].name == "Temperature"
    assert isotropic_strain_limits.independent_parameters[0].values.value.tolist() == [23, 25, 27]
    assert isotropic_strain_limits.independent_parameters[0].values.unit == "C"


def test_read_constant_strain_limit_orthotropic():
    matml_reader = MatmlReader(XML_FILE_PATH)
    materials = matml_reader.convert_matml_materials()
    material = materials["orthotropic material with strain limit"]
    assert len(material.models) == 1
    orthotropic_strain_limits = material.models[0]
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
    assert orthotropic_strain_limits.independent_parameters[0].values.value == [
        7.88860905221012e-31
    ]
    assert orthotropic_strain_limits.independent_parameters[0].values.unit == "C"
    assert orthotropic_strain_limits.independent_parameters[0].upper_limit == "Program Controlled"
    assert orthotropic_strain_limits.independent_parameters[0].lower_limit == "Program Controlled"
    assert orthotropic_strain_limits.independent_parameters[0].default_value == 22.0


def test_read_variable_strain_limit_orthotropic():
    matml_reader = MatmlReader(XML_FILE_PATH)
    materials = matml_reader.convert_matml_materials()
    material = materials["orthotropic material with variable strain limit"]
    assert len(material.models) == 1
    orthotropic_strain_limits = material.models[0]
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
    assert orthotropic_strain_limits.compressive_x_direction.value.tolist() == [
        -110.0,
        -132.0,
        -120.0,
    ]
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
    assert orthotropic_strain_limits.independent_parameters[0].values.value.tolist() == [
        13.0,
        21.0,
        23.0,
    ]
    assert orthotropic_strain_limits.independent_parameters[0].values.unit == "C"
    assert orthotropic_strain_limits.independent_parameters[0].upper_limit == "Program Controlled"
    assert orthotropic_strain_limits.independent_parameters[0].lower_limit == "Program Controlled"
    assert orthotropic_strain_limits.independent_parameters[0].default_value == 22.0
