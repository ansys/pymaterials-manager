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
XML_FILE_PATH = os.path.join(DIR_PATH, "..", "data", "MatML_unittest_elasticity.xml")


def test_read_constant_elastic_isotropic_material():
    material_dic = read_matml_file(XML_FILE_PATH)
    assert "Isotropic Test Material" in material_dic.keys()
    assert len(material_dic["Isotropic Test Material"].models) == 1
    isotropic_elasticity = material_dic["Isotropic Test Material"].models[0]

    assert isotropic_elasticity.name == "Elasticity"
    assert isotropic_elasticity.model_qualifiers[0].name == "Behavior"
    assert isotropic_elasticity.model_qualifiers[0].value == "Isotropic"
    assert isotropic_elasticity.model_qualifiers[1].name == "Derive from"
    assert isotropic_elasticity.model_qualifiers[1].value == "Young's Modulus and Poisson's Ratio"
    assert isotropic_elasticity.model_qualifiers[2].name == "Field Variable Compatible"
    assert isotropic_elasticity.model_qualifiers[2].value == "Temperature"
    assert isotropic_elasticity.interpolation_options.algorithm_type == "Linear Multivariate"
    assert isotropic_elasticity.interpolation_options.cached == True
    assert isotropic_elasticity.interpolation_options.normalized == True
    assert isotropic_elasticity.independent_parameters[0].name == "Temperature"
    assert isotropic_elasticity.independent_parameters[0].values == [7.88860905221012e-31]
    assert isotropic_elasticity.independent_parameters[0].units == "C"
    assert isotropic_elasticity.independent_parameters[0].upper_limit == "1.18329135783152E-30"
    assert isotropic_elasticity.independent_parameters[0].lower_limit == "3.94430452610506E-31"
    assert isotropic_elasticity.independent_parameters[0].default_value == "22"
    assert isotropic_elasticity.youngs_modulus == [1000000.0]
    assert isotropic_elasticity.poissons_ratio == [0.3]


def test_read_constant_elastic_orthotropic_material():
    material_dic = read_matml_file(XML_FILE_PATH)
    assert "Orthotropic Test Material" in material_dic.keys()
    assert len(material_dic["Orthotropic Test Material"].models) == 1
    orthotropic_elasticity = material_dic["Orthotropic Test Material"].models[0]
    assert orthotropic_elasticity.name == "Elasticity"
    assert orthotropic_elasticity.model_qualifiers[0].name == "Behavior"
    assert orthotropic_elasticity.model_qualifiers[0].value == "Orthotropic"
    assert orthotropic_elasticity.model_qualifiers[1].name == "Field Variable Compatible"
    assert orthotropic_elasticity.model_qualifiers[1].value == "Temperature"
    assert orthotropic_elasticity.interpolation_options.algorithm_type == "Linear Multivariate"
    assert orthotropic_elasticity.interpolation_options.cached == True
    assert orthotropic_elasticity.interpolation_options.normalized == True
    assert orthotropic_elasticity.youngs_modulus_x == [10000000.0]
    assert orthotropic_elasticity.youngs_modulus_y == [15000000.0]
    assert orthotropic_elasticity.youngs_modulus_z == [20000000.0]
    assert orthotropic_elasticity.poissons_ratio_xy == [0.2]
    assert orthotropic_elasticity.poissons_ratio_yz == [0.3]
    assert orthotropic_elasticity.poissons_ratio_xz == [0.4]
    assert orthotropic_elasticity.shear_modulus_xy == [1000000.0]
    assert orthotropic_elasticity.shear_modulus_yz == [2000000.0]
    assert orthotropic_elasticity.shear_modulus_xz == [3000000.0]
    assert orthotropic_elasticity.independent_parameters[0].name == "Temperature"
    assert orthotropic_elasticity.independent_parameters[0].values == [7.88860905221012e-31]
    assert orthotropic_elasticity.independent_parameters[0].units == "C"
    assert orthotropic_elasticity.independent_parameters[0].upper_limit == "1.18329135783152E-30"
    assert orthotropic_elasticity.independent_parameters[0].lower_limit == "3.94430452610506E-31"
    assert orthotropic_elasticity.independent_parameters[0].default_value == "22"


def test_read_constant_elastic_anisotropic_material():
    material_dic = read_matml_file(XML_FILE_PATH)
    assert "Anisotropic Test Material" in material_dic.keys()
    assert len(material_dic["Anisotropic Test Material"].models) == 1
    orthotropic_elasticity = material_dic["Anisotropic Test Material"].models[0]
    assert orthotropic_elasticity.name == "Elasticity"
    assert orthotropic_elasticity.model_qualifiers[0].name == "Behavior"
    assert orthotropic_elasticity.model_qualifiers[0].value == "Anisotropic"
    assert orthotropic_elasticity.column_1 == [
        100000000,
        1000000,
        2000000,
        3000000,
        4000000,
        5000000,
    ]
    assert orthotropic_elasticity.column_2 == [
        7.88860905221012e-31,
        150000000,
        6000000,
        7000000,
        8000000,
        9000000,
    ]
    assert orthotropic_elasticity.column_3 == [
        7.88860905221012e-31,
        7.88860905221012e-31,
        200000000,
        10000000,
        11000000,
        12000000,
    ]
    assert orthotropic_elasticity.column_4 == [
        7.88860905221012e-31,
        7.88860905221012e-31,
        7.88860905221012e-31,
        50000000,
        13000000,
        14000000,
    ]
    assert orthotropic_elasticity.column_5 == [
        7.88860905221012e-31,
        7.88860905221012e-31,
        7.88860905221012e-31,
        7.88860905221012e-31,
        60000000,
        15000000,
    ]
    assert orthotropic_elasticity.column_6 == [
        7.88860905221012e-31,
        7.88860905221012e-31,
        7.88860905221012e-31,
        7.88860905221012e-31,
        7.88860905221012e-31,
        70000000,
    ]


def test_read_variable_elastic_isotropic_material():
    material_dic = read_matml_file(XML_FILE_PATH)
    assert "Variable Isotropic Test Material" in material_dic.keys()
    assert len(material_dic["Variable Isotropic Test Material"].models) == 1
    isotropic_elasticity = material_dic["Variable Isotropic Test Material"].models[0]
    assert isotropic_elasticity.name == "Elasticity"
    assert isotropic_elasticity.model_qualifiers[0].name == "Behavior"
    assert isotropic_elasticity.model_qualifiers[0].value == "Isotropic"
    assert isotropic_elasticity.model_qualifiers[1].name == "Derive from"
    assert isotropic_elasticity.model_qualifiers[1].value == "Young's Modulus and Poisson's Ratio"
    assert isotropic_elasticity.model_qualifiers[2].name == "Field Variable Compatible"
    assert isotropic_elasticity.model_qualifiers[2].value == "Temperature"
    assert isotropic_elasticity.interpolation_options.algorithm_type == "Linear Multivariate"
    assert isotropic_elasticity.interpolation_options.cached == True
    assert isotropic_elasticity.interpolation_options.normalized == True
    assert isotropic_elasticity.independent_parameters[0].name == "Temperature"
    assert isotropic_elasticity.independent_parameters[0].values == [12, 21]
    assert isotropic_elasticity.independent_parameters[0].units == "C"
    assert isotropic_elasticity.independent_parameters[0].upper_limit == "1.18329135783152E-30"
    assert isotropic_elasticity.independent_parameters[0].lower_limit == "3.94430452610506E-31"
    assert isotropic_elasticity.independent_parameters[0].default_value == "22"
    assert isotropic_elasticity.youngs_modulus == [2000000, 1000000]
    assert isotropic_elasticity.poissons_ratio == [0.35, 0.3]


def test_read_variable_elastic_orthotropic_material():
    material_dic = read_matml_file(XML_FILE_PATH)
    assert "Variable Orthotropic Test Material" in material_dic.keys()
    assert len(material_dic["Variable Orthotropic Test Material"].models) == 1
    orthotropic_elasticity = material_dic["Variable Orthotropic Test Material"].models[0]
    assert orthotropic_elasticity.name == "Elasticity"
    assert orthotropic_elasticity.model_qualifiers[0].name == "Behavior"
    assert orthotropic_elasticity.model_qualifiers[0].value == "Orthotropic"
    assert orthotropic_elasticity.model_qualifiers[1].name == "Field Variable Compatible"
    assert orthotropic_elasticity.model_qualifiers[1].value == "Temperature"
    assert orthotropic_elasticity.interpolation_options.algorithm_type == "Linear Multivariate"
    assert orthotropic_elasticity.interpolation_options.cached == True
    assert orthotropic_elasticity.interpolation_options.normalized == True
    assert orthotropic_elasticity.youngs_modulus_x == [10000000.0, 11000000.0]
    assert orthotropic_elasticity.youngs_modulus_y == [15000000.0, 15100000]
    assert orthotropic_elasticity.youngs_modulus_z == [20000000.0, 21000000]
    assert orthotropic_elasticity.poissons_ratio_xy == [0.2, 0.21]
    assert orthotropic_elasticity.poissons_ratio_yz == [0.3, 0.31]
    assert orthotropic_elasticity.poissons_ratio_xz == [0.4, 0.41]
    assert orthotropic_elasticity.shear_modulus_xy == [1000000.0, 1100000]
    assert orthotropic_elasticity.shear_modulus_yz == [2000000.0, 2100000]
    assert orthotropic_elasticity.shear_modulus_xz == [3000000.0, 3100000]
    assert orthotropic_elasticity.independent_parameters[0].name == "Temperature"
    assert orthotropic_elasticity.independent_parameters[0].values == [21, 22]
    assert orthotropic_elasticity.independent_parameters[0].units == "C"
    assert orthotropic_elasticity.independent_parameters[0].upper_limit == "1.18329135783152E-30"
    assert orthotropic_elasticity.independent_parameters[0].lower_limit == "3.94430452610506E-31"
    assert orthotropic_elasticity.independent_parameters[0].default_value == "22"
