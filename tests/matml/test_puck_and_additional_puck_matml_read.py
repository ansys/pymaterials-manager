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

from ansys.materials.manager.util.visitors.matml_reader import MatmlReader

DIR_PATH = Path(__file__).resolve().parent
XML_FILE_PATH = DIR_PATH.joinpath("..", "data", "matml_unittest_puck_for_woven.xml")


def test_read_fiber_angle():
    matml_reader = MatmlReader(XML_FILE_PATH)
    materials = matml_reader.convert_matml_materials()
    material = materials["material with puck for woven"]
    assert len(material.models) == 4
    fiber_angle = material.models[0]
    assert fiber_angle.name == "Fiber Angle"
    assert fiber_angle.independent_parameters[0].name == "Fiber Angle"
    assert fiber_angle.independent_parameters[0].values.value == [90.0]
    assert fiber_angle.independent_parameters[0].values.unit == ""
    assert fiber_angle.model_qualifiers[0].name == "Data Set"
    assert fiber_angle.model_qualifiers[0].value == "2"
    assert fiber_angle.model_qualifiers[1].name == "Data Set Information"
    assert (
        fiber_angle.model_qualifiers[1].value
        == "minOccurrences::2$$maxOccurrences::2$$Name::Unidirectional"
    )


def test_read_puck_constants():
    matml_reader = MatmlReader(XML_FILE_PATH)
    materials = matml_reader.convert_matml_materials()
    material = materials["material with puck for woven"]
    assert len(material.models) == 4
    puck_constants = material.models[2]
    assert puck_constants.name == "Puck Constants"
    assert puck_constants.independent_parameters == None
    assert puck_constants.model_qualifiers[0].name == "Data Set"
    assert puck_constants.model_qualifiers[0].value == "2"
    assert puck_constants.model_qualifiers[1].name == "Data Set Information"
    assert (
        puck_constants.model_qualifiers[1].value
        == "minOccurrences::2$$maxOccurrences::2$$Name::Unidirectional"
    )
    assert puck_constants.model_qualifiers[2].name == "Material Classification"
    assert puck_constants.model_qualifiers[2].value == "Material Specific"
    assert puck_constants.compressive_inclination_xz.value == [0.0]
    assert puck_constants.compressive_inclination_xz.unit == ""
    assert puck_constants.compressive_inclination_yz.value == [0.0]
    assert puck_constants.compressive_inclination_yz.unit == ""
    assert puck_constants.tensile_inclination_xz.value == [0.0]
    assert puck_constants.tensile_inclination_xz.unit == ""
    assert puck_constants.tensile_inclination_yz.value == [0.0]
    assert puck_constants.tensile_inclination_yz.unit == ""


def test_read_puck_additional_constants():
    matml_reader = MatmlReader(XML_FILE_PATH)
    materials = matml_reader.convert_matml_materials()
    material = materials["material with puck for woven"]
    assert len(material.models) == 4
    puck_additional_constants = material.models[3]
    assert puck_additional_constants.name == "Additional Puck Constants"
    assert puck_additional_constants.independent_parameters == None
    assert puck_additional_constants.model_qualifiers[0].name == "Data Set"
    assert puck_additional_constants.model_qualifiers[0].value == "2"
    assert puck_additional_constants.model_qualifiers[1].name == "Data Set Information"
    assert (
        puck_additional_constants.model_qualifiers[1].value
        == "minOccurrences::2$$maxOccurrences::2$$Name::Unidirectional"
    )
    assert puck_additional_constants.degradation_parameter_s.value == [0.5]
    assert puck_additional_constants.degradation_parameter_s.unit == ""
    assert puck_additional_constants.degradation_parameter_m.value == [0.5]
    assert puck_additional_constants.degradation_parameter_m.unit == ""
    assert puck_additional_constants.interface_weakening_factor.value == [0.8]
    assert puck_additional_constants.interface_weakening_factor.unit == ""


def test_read_stress_limits_orthotropic():
    matml_reader = MatmlReader(XML_FILE_PATH)
    materials = matml_reader.convert_matml_materials()
    material = materials["material with puck for woven"]
    assert len(material.models) == 4
    stress_limits_orthotropic = material.models[1]
    assert stress_limits_orthotropic.name == "Stress Limits"
    assert stress_limits_orthotropic.independent_parameters == None
    assert stress_limits_orthotropic.model_qualifiers[0].name == "Behavior"
    assert stress_limits_orthotropic.model_qualifiers[0].value == "Orthotropic"
    assert stress_limits_orthotropic.model_qualifiers[1].name == "Data Set"
    assert stress_limits_orthotropic.model_qualifiers[1].value == "2"
    assert stress_limits_orthotropic.model_qualifiers[2].name == "Data Set Information"
    assert (
        stress_limits_orthotropic.model_qualifiers[2].value
        == "minOccurrences::2$$maxOccurrences::2$$Name::Unidirectional"
    )
    assert stress_limits_orthotropic.compressive_x_direction.value == [-100.0]
    assert stress_limits_orthotropic.compressive_x_direction.unit == "Pa"
    assert stress_limits_orthotropic.compressive_y_direction.value == [-101.0]
    assert stress_limits_orthotropic.compressive_y_direction.unit == "Pa"
    assert stress_limits_orthotropic.compressive_z_direction.value == [-102.0]
    assert stress_limits_orthotropic.compressive_z_direction.unit == "Pa"
    assert stress_limits_orthotropic.tensile_x_direction.value == [100.0]
    assert stress_limits_orthotropic.tensile_x_direction.unit == "Pa"
    assert stress_limits_orthotropic.tensile_y_direction.value == [101.0]
    assert stress_limits_orthotropic.tensile_y_direction.unit == "Pa"
    assert stress_limits_orthotropic.tensile_z_direction.value == [102.0]
    assert stress_limits_orthotropic.tensile_z_direction.unit == "Pa"
    assert stress_limits_orthotropic.shear_xy.value == [10.0]
    assert stress_limits_orthotropic.shear_xy.unit == "Pa"
    assert stress_limits_orthotropic.shear_xz.value == [14.0]
    assert stress_limits_orthotropic.shear_xz.unit == "Pa"
    assert stress_limits_orthotropic.shear_yz.value == [12.0]
    assert stress_limits_orthotropic.shear_yz.unit == "Pa"
