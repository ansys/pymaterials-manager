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
NO_CREEP_XML_FILE_PATH = os.path.join(DIR_PATH, "..", "data", "MatML_unittest_hill_yield.xml")
CREEP_XML_FILE_PATH = os.path.join(DIR_PATH, "..", "data", "MatML_unittest_hill_yield_creep.xml")


def test_read_constant_hill_yield_no_creep():
    material_dic = read_matml_file(NO_CREEP_XML_FILE_PATH)
    assert "SFRP" in material_dic.keys()
    assert len(material_dic["SFRP"].models) == 2
    hill_yield = material_dic["SFRP"].models[1]
    assert hill_yield.name == "Hill Yield Criterion"
    assert (
        hill_yield.model_qualifiers[0].name == "Separated Hill Potentials for Plasticity and Creep"
    )
    assert hill_yield.model_qualifiers[0].value == "No"
    assert hill_yield.model_qualifiers[1].name == "Field Variable Compatible"
    assert hill_yield.model_qualifiers[1].value == "Temperature"
    assert hill_yield.interpolation_options.algorithm_type == "Linear Multivariate"
    assert hill_yield.interpolation_options.cached == True
    assert hill_yield.interpolation_options.normalized == True
    assert hill_yield.yield_stress_ratio_x == [1.2]
    assert hill_yield.yield_stress_ratio_xy == [0.12]
    assert hill_yield.yield_stress_ratio_xz == [0.23]
    assert hill_yield.yield_stress_ratio_y == [0.8]
    assert hill_yield.yield_stress_ratio_yz == [0.23]
    assert hill_yield.yield_stress_ratio_z == [0.5]
    assert hill_yield.yield_stress_ratio_x_for_plasticity == None
    assert hill_yield.yield_stress_ratio_y_for_plasticity == None
    assert hill_yield.yield_stress_ratio_z_for_plasticity == None
    assert hill_yield.yield_stress_ratio_xy_for_plasticity == None
    assert hill_yield.yield_stress_ratio_xz_for_plasticity == None
    assert hill_yield.yield_stress_ratio_yz_for_plasticity == None
    assert hill_yield.yield_stress_ratio_x_for_creep == None
    assert hill_yield.yield_stress_ratio_y_for_creep == None
    assert hill_yield.yield_stress_ratio_z_for_creep == None
    assert hill_yield.yield_stress_ratio_xy_for_creep == None
    assert hill_yield.yield_stress_ratio_xz_for_creep == None
    assert hill_yield.yield_stress_ratio_yz_for_creep == None
    assert hill_yield.independent_parameters[0].name == "Temperature"
    assert hill_yield.independent_parameters[0].units == "C"
    assert hill_yield.independent_parameters[0].default_value == "22"
    assert hill_yield.independent_parameters[0].upper_limit == "Program Controlled"
    assert hill_yield.independent_parameters[0].lower_limit == "Program Controlled"


def test_read_variable_temp_hill_yield_no_creep():
    material_dic = read_matml_file(NO_CREEP_XML_FILE_PATH)
    assert "SFRP Temp Dependent" in material_dic.keys()
    assert len(material_dic["SFRP Temp Dependent"].models) == 2
    hill_yield = material_dic["SFRP Temp Dependent"].models[1]
    assert hill_yield.name == "Hill Yield Criterion"
    assert (
        hill_yield.model_qualifiers[0].name == "Separated Hill Potentials for Plasticity and Creep"
    )
    assert hill_yield.model_qualifiers[0].value == "No"
    assert hill_yield.model_qualifiers[1].name == "Field Variable Compatible"
    assert hill_yield.model_qualifiers[1].value == "Temperature"
    assert hill_yield.interpolation_options.algorithm_type == "Linear Multivariate"
    assert hill_yield.interpolation_options.cached == True
    assert hill_yield.interpolation_options.normalized == True
    assert hill_yield.yield_stress_ratio_x == [1.2, 1.2, 1.4]
    assert hill_yield.yield_stress_ratio_xy == [0.12, 0.12, 0.12]
    assert hill_yield.yield_stress_ratio_xz == [0.23, 0.23, 0.23]
    assert hill_yield.yield_stress_ratio_y == [0.8, 0.8, 0.7]
    assert hill_yield.yield_stress_ratio_yz == [0.23, 0.23, 0.23]
    assert hill_yield.yield_stress_ratio_z == [0.5, 0.5, 0.4]
    assert hill_yield.yield_stress_ratio_x_for_plasticity == None
    assert hill_yield.yield_stress_ratio_y_for_plasticity == None
    assert hill_yield.yield_stress_ratio_z_for_plasticity == None
    assert hill_yield.yield_stress_ratio_xy_for_plasticity == None
    assert hill_yield.yield_stress_ratio_xz_for_plasticity == None
    assert hill_yield.yield_stress_ratio_yz_for_plasticity == None
    assert hill_yield.yield_stress_ratio_x_for_creep == None
    assert hill_yield.yield_stress_ratio_y_for_creep == None
    assert hill_yield.yield_stress_ratio_z_for_creep == None
    assert hill_yield.yield_stress_ratio_xy_for_creep == None
    assert hill_yield.yield_stress_ratio_xz_for_creep == None
    assert hill_yield.yield_stress_ratio_yz_for_creep == None
    assert hill_yield.independent_parameters[0].name == "Temperature"
    assert hill_yield.independent_parameters[0].values == [34, 78, 245]
    assert hill_yield.independent_parameters[0].units == "C"
    assert hill_yield.independent_parameters[0].default_value == "22"
    assert hill_yield.independent_parameters[0].upper_limit == "Program Controlled"
    assert hill_yield.independent_parameters[0].lower_limit == "Program Controlled"


def test_read_variable_hill_yield_no_creep():
    material_dic = read_matml_file(NO_CREEP_XML_FILE_PATH)
    assert "Variable Short Fiber" in material_dic.keys()
    assert len(material_dic["Variable Short Fiber"].models) == 1
    hill_yield = material_dic["Variable Short Fiber"].models[0]
    assert hill_yield.name == "Hill Yield Criterion"
    assert (
        hill_yield.model_qualifiers[0].name == "Separated Hill Potentials for Plasticity and Creep"
    )
    assert hill_yield.model_qualifiers[0].value == "No"
    assert hill_yield.model_qualifiers[1].name == "Field Variable Compatible"
    assert hill_yield.model_qualifiers[1].value == "Temperature"
    assert hill_yield.interpolation_options.algorithm_type == "Linear Multivariate"
    assert hill_yield.interpolation_options.cached == True
    assert hill_yield.interpolation_options.normalized == True
    assert hill_yield.yield_stress_ratio_x == [
        1.0,
        1.38717930847789,
        3.00721990713311,
        1.2181891328774,
        1.0,
        1.38717930847789,
        1.0,
    ]
    assert hill_yield.yield_stress_ratio_xy == [
        1.27583858742812,
        1.27583858742812,
        1.27583858742812,
        1.27583858742812,
        1.27583858742812,
        1.27583858742812,
        1.27583858742812,
    ]
    assert hill_yield.yield_stress_ratio_xz == [
        1.27583858742812,
        1.27583858742812,
        1.27583858742812,
        1.27583858742812,
        1.27583858742812,
        1.27583858742812,
        1.27583858742812,
    ]
    assert hill_yield.yield_stress_ratio_y == [
        1.0,
        1.0,
        1.0,
        1.2181891328774,
        1.38717930847789,
        1.38717930847789,
        3.00721990713311,
    ]
    assert hill_yield.yield_stress_ratio_yz == [
        1.27583858742812,
        1.27583858742812,
        1.27583858742812,
        1.27583858742812,
        1.27583858742812,
        1.27583858742812,
        1.27583858742812,
    ]
    assert hill_yield.yield_stress_ratio_z == [
        3.00721990713311,
        1.38717930847789,
        1.0,
        1.21818913296279,
        1.38717930847789,
        1.0,
        1.0,
    ]
    assert hill_yield.yield_stress_ratio_x_for_plasticity == None
    assert hill_yield.yield_stress_ratio_y_for_plasticity == None
    assert hill_yield.yield_stress_ratio_z_for_plasticity == None
    assert hill_yield.yield_stress_ratio_xy_for_plasticity == None
    assert hill_yield.yield_stress_ratio_xz_for_plasticity == None
    assert hill_yield.yield_stress_ratio_yz_for_plasticity == None
    assert hill_yield.yield_stress_ratio_x_for_creep == None
    assert hill_yield.yield_stress_ratio_y_for_creep == None
    assert hill_yield.yield_stress_ratio_z_for_creep == None
    assert hill_yield.yield_stress_ratio_xy_for_creep == None
    assert hill_yield.yield_stress_ratio_xz_for_creep == None
    assert hill_yield.yield_stress_ratio_yz_for_creep == None
    assert hill_yield.independent_parameters[0].name == "Orientation Tensor A11"
    assert hill_yield.independent_parameters[0].values == [0, 0.5, 1, 0.3333333333, 0, 0.5, 0]
    assert hill_yield.independent_parameters[0].default_value == "Program Controlled"
    assert hill_yield.independent_parameters[0].upper_limit == "Program Controlled"
    assert hill_yield.independent_parameters[0].lower_limit == "Program Controlled"
    assert hill_yield.independent_parameters[1].name == "Orientation Tensor A22"
    assert hill_yield.independent_parameters[1].values == [0, 0, 0, 0.3333333333, 0.5, 0.5, 1]
    assert hill_yield.independent_parameters[1].default_value == "Program Controlled"
    assert hill_yield.independent_parameters[1].upper_limit == "Program Controlled"
    assert hill_yield.independent_parameters[1].lower_limit == "Program Controlled"


def test_read_constant_hill_yield_creep():
    material_dic = read_matml_file(CREEP_XML_FILE_PATH)
    assert "SFRP" in material_dic.keys()
    assert len(material_dic["SFRP"].models) == 4
    hill_yield = material_dic["SFRP"].models[1]
    assert hill_yield.name == "Hill Yield Criterion"
    assert (
        hill_yield.model_qualifiers[0].name == "Separated Hill Potentials for Plasticity and Creep"
    )
    assert hill_yield.model_qualifiers[0].value == "Yes"
    assert hill_yield.yield_stress_ratio_x == None
    assert hill_yield.yield_stress_ratio_xy == None
    assert hill_yield.yield_stress_ratio_xz == None
    assert hill_yield.yield_stress_ratio_y == None
    assert hill_yield.yield_stress_ratio_yz == None
    assert hill_yield.yield_stress_ratio_z == None
    assert hill_yield.yield_stress_ratio_x_for_plasticity == [1.0]
    assert hill_yield.yield_stress_ratio_y_for_plasticity == [1.0]
    assert hill_yield.yield_stress_ratio_z_for_plasticity == [1.0]
    assert hill_yield.yield_stress_ratio_xy_for_plasticity == [1.0]
    assert hill_yield.yield_stress_ratio_xz_for_plasticity == [1.0]
    assert hill_yield.yield_stress_ratio_yz_for_plasticity == [1.0]
    assert hill_yield.yield_stress_ratio_x_for_creep == [2.0]
    assert hill_yield.yield_stress_ratio_y_for_creep == [2.0]
    assert hill_yield.yield_stress_ratio_z_for_creep == [2.0]
    assert hill_yield.yield_stress_ratio_xy_for_creep == [2.0]
    assert hill_yield.yield_stress_ratio_xz_for_creep == [2.0]
    assert hill_yield.yield_stress_ratio_yz_for_creep == [2.0]
    assert hill_yield.independent_parameters[0].name == "Temperature"
    assert hill_yield.independent_parameters[0].values == [7.88860905221012e-31]


def test_read_constant_kinematic_hardening_creep():
    material_dic = read_matml_file(CREEP_XML_FILE_PATH)
    assert "SFRP" in material_dic.keys()
    assert len(material_dic["SFRP"].models) == 4
    kinematic_hardening = material_dic["SFRP"].models[2]
    assert kinematic_hardening.name == "Kinematic Hardening"
    assert kinematic_hardening.model_qualifiers[0].name == "Definition"
    assert kinematic_hardening.model_qualifiers[0].value == "Chaboche"
    assert kinematic_hardening.model_qualifiers[1].name == "Number of Kinematic Models"
    assert kinematic_hardening.model_qualifiers[1].value == "1"
    assert kinematic_hardening.model_qualifiers[2].name == "source"
    assert kinematic_hardening.model_qualifiers[2].value == "ANSYS"
    assert kinematic_hardening.yield_stress == [12.0]
    assert kinematic_hardening.material_constant_gamma_1 == [1.0]
    assert kinematic_hardening.material_constant_c_1 == [45.0]
    assert kinematic_hardening.material_constant_gamma_2 == None
    assert kinematic_hardening.material_constant_c_2 == None
    assert kinematic_hardening.material_constant_gamma_3 == None
    assert kinematic_hardening.material_constant_c_3 == None
    assert kinematic_hardening.material_constant_gamma_4 == None
    assert kinematic_hardening.material_constant_c_4 == None
    assert kinematic_hardening.material_constant_gamma_5 == None
    assert kinematic_hardening.material_constant_c_5 == None
    assert kinematic_hardening.independent_parameters[0].name == "Temperature"
    assert kinematic_hardening.independent_parameters[0].values == [7.88860905221012e-31]


def test_read_constant_strain_hardening_creep():
    material_dic = read_matml_file(CREEP_XML_FILE_PATH)
    assert "SFRP" in material_dic.keys()
    assert len(material_dic["SFRP"].models) == 4
    strain_hardening = material_dic["SFRP"].models[3]
    assert strain_hardening.name == "Strain Hardening"
    assert (
        strain_hardening.model_qualifiers[0].name
        == "Reference Units (Length, Time, Temperature, Force)"
    )
    assert strain_hardening.model_qualifiers[0].value == "m, s, K, N"
    assert strain_hardening.creep_constant_1 == [1.0]
    assert strain_hardening.creep_constant_2 == [2.0]
    assert strain_hardening.creep_constant_3 == [3.0]
    assert strain_hardening.creep_constant_4 == [4.0]
    assert strain_hardening.independent_parameters[0].name == "Temperature"
    assert strain_hardening.independent_parameters[0].values == [7.88860905221012e-31]
