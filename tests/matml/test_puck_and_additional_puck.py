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

from utilities import read_matml_file

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
XML_FILE_PATH = os.path.join(DIR_PATH, "..", "data", "MatML_unittest_puck_for_woven.xml")


# def test_read_puck_and_additional_puck():
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
