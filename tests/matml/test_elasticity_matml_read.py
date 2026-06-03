# Copyright (C) 2022 - 2026 ANSYS, Inc. and/or its affiliates.
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
XML_FILE_PATH = DIR_PATH.joinpath("..", "data", "matml_unittest_elasticity.xml")


def test_read_constant_elastic_isotropic_material():
    matml_reader = MatmlReader(XML_FILE_PATH)
    materials = matml_reader.convert_matml_materials()
    material = materials["Isotropic Test Material"]
    assert len(material.models) == 1
    isotropic_elasticity = material.models[0]
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
    assert isotropic_elasticity.independent_parameters[0].values.value == [7.88860905221012e-31]
    assert isotropic_elasticity.independent_parameters[0].values.unit == "C"
    assert isotropic_elasticity.independent_parameters[0].upper_limit == 1.18329135783152e-30
    assert isotropic_elasticity.independent_parameters[0].lower_limit == 3.94430452610506e-31
    assert isotropic_elasticity.independent_parameters[0].default_value == 22.0
    assert isotropic_elasticity.youngs_modulus.value == [1000000.0]
    assert isotropic_elasticity.youngs_modulus.unit == "Pa"
    assert isotropic_elasticity.poissons_ratio.value == [0.3]
    assert isotropic_elasticity.poissons_ratio.unit == ""


def test_read_constant_elastic_orthotropic_material():
    matml_reader = MatmlReader(XML_FILE_PATH)
    materials = matml_reader.convert_matml_materials()
    material = materials["Orthotropic Test Material"]
    assert len(material.models) == 1
    orthotropic_elasticity = material.models[0]
    assert orthotropic_elasticity.name == "Elasticity"
    assert orthotropic_elasticity.model_qualifiers[0].name == "Behavior"
    assert orthotropic_elasticity.model_qualifiers[0].value == "Orthotropic"
    assert orthotropic_elasticity.model_qualifiers[1].name == "Field Variable Compatible"
    assert orthotropic_elasticity.model_qualifiers[1].value == "Temperature"
    assert orthotropic_elasticity.interpolation_options.algorithm_type == "Linear Multivariate"
    assert orthotropic_elasticity.interpolation_options.cached == True
    assert orthotropic_elasticity.interpolation_options.normalized == True
    assert orthotropic_elasticity.youngs_modulus_x.value == [10000000.0]
    assert orthotropic_elasticity.youngs_modulus_x.unit == "Pa"
    assert orthotropic_elasticity.youngs_modulus_y.value == [15000000.0]
    assert orthotropic_elasticity.youngs_modulus_y.unit == "Pa"
    assert orthotropic_elasticity.youngs_modulus_z.value == [20000000.0]
    assert orthotropic_elasticity.youngs_modulus_z.unit == "Pa"
    assert orthotropic_elasticity.poissons_ratio_xy.value == [0.2]
    assert orthotropic_elasticity.poissons_ratio_xy.unit == ""
    assert orthotropic_elasticity.poissons_ratio_yz.value == [0.3]
    assert orthotropic_elasticity.poissons_ratio_yz.unit == ""
    assert orthotropic_elasticity.poissons_ratio_xz.value == [0.4]
    assert orthotropic_elasticity.poissons_ratio_xz.unit == ""
    assert orthotropic_elasticity.shear_modulus_xy.value == [1000000.0]
    assert orthotropic_elasticity.shear_modulus_xy.unit == "Pa"
    assert orthotropic_elasticity.shear_modulus_yz.value == [2000000.0]
    assert orthotropic_elasticity.shear_modulus_yz.unit == "Pa"
    assert orthotropic_elasticity.shear_modulus_xz.value == [3000000.0]
    assert orthotropic_elasticity.shear_modulus_xz.unit == "Pa"
    assert orthotropic_elasticity.independent_parameters[0].name == "Temperature"
    assert orthotropic_elasticity.independent_parameters[0].values.value == [7.88860905221012e-31]
    assert orthotropic_elasticity.independent_parameters[0].values.unit == "C"
    assert orthotropic_elasticity.independent_parameters[0].upper_limit == 1.18329135783152e-30
    assert orthotropic_elasticity.independent_parameters[0].lower_limit == 3.94430452610506e-31
    assert orthotropic_elasticity.independent_parameters[0].default_value == 22.0


def test_read_constant_elastic_anisotropic_material():
    matml_reader = MatmlReader(XML_FILE_PATH)
    materials = matml_reader.convert_matml_materials()
    material = materials["Anisotropic Test Material"]
    assert len(material.models) == 1
    anisotropic_elasticity = material.models[0]
    assert anisotropic_elasticity.name == "Elasticity"
    assert anisotropic_elasticity.model_qualifiers[0].name == "Behavior"
    assert anisotropic_elasticity.model_qualifiers[0].value == "Anisotropic"
    assert anisotropic_elasticity.c_11.value.tolist() == [100000000]
    assert anisotropic_elasticity.c_11.unit == "Pa"
    assert anisotropic_elasticity.c_12.value.tolist() == [1000000]
    assert anisotropic_elasticity.c_12.unit == "Pa"
    assert anisotropic_elasticity.c_13.value.tolist() == [2000000]
    assert anisotropic_elasticity.c_13.unit == "Pa"
    assert anisotropic_elasticity.c_14.value.tolist() == [0]
    assert anisotropic_elasticity.c_14.unit == "Pa"
    assert anisotropic_elasticity.c_15.value.tolist() == [0]
    assert anisotropic_elasticity.c_15.unit == "Pa"
    assert anisotropic_elasticity.c_16.value.tolist() == [0]
    assert anisotropic_elasticity.c_16.unit == "Pa"
    assert anisotropic_elasticity.c_22.value.tolist() == [150000000]
    assert anisotropic_elasticity.c_22.unit == "Pa"
    assert anisotropic_elasticity.c_23.value.tolist() == [3000000]
    assert anisotropic_elasticity.c_23.unit == "Pa"
    assert anisotropic_elasticity.c_24.value.tolist() == [0]
    assert anisotropic_elasticity.c_24.unit == "Pa"
    assert anisotropic_elasticity.c_25.value.tolist() == [0]
    assert anisotropic_elasticity.c_25.unit == "Pa"
    assert anisotropic_elasticity.c_26.value.tolist() == [0]
    assert anisotropic_elasticity.c_26.unit == "Pa"
    assert anisotropic_elasticity.c_33.value.tolist() == [200000000]
    assert anisotropic_elasticity.c_33.unit == "Pa"
    assert anisotropic_elasticity.c_34.value.tolist() == [0]
    assert anisotropic_elasticity.c_34.unit == "Pa"
    assert anisotropic_elasticity.c_35.value.tolist() == [0]
    assert anisotropic_elasticity.c_35.unit == "Pa"
    assert anisotropic_elasticity.c_36.value.tolist() == [0]
    assert anisotropic_elasticity.c_36.unit == "Pa"
    assert anisotropic_elasticity.c_44.value.tolist() == [50000000]
    assert anisotropic_elasticity.c_44.unit == "Pa"
    assert anisotropic_elasticity.c_45.value.tolist() == [0]
    assert anisotropic_elasticity.c_45.unit == "Pa"
    assert anisotropic_elasticity.c_46.value.tolist() == [0]
    assert anisotropic_elasticity.c_46.unit == "Pa"
    assert anisotropic_elasticity.c_55.value.tolist() == [60000000]
    assert anisotropic_elasticity.c_55.unit == "Pa"
    assert anisotropic_elasticity.c_56.value.tolist() == [0]
    assert anisotropic_elasticity.c_56.unit == "Pa"
    assert anisotropic_elasticity.c_66.value.tolist() == [70000000]
    assert anisotropic_elasticity.c_66.unit == "Pa"


def test_read_variable_elastic_isotropic_material():
    matml_reader = MatmlReader(XML_FILE_PATH)
    materials = matml_reader.convert_matml_materials()
    material = materials["Variable Isotropic Test Material"]
    assert len(material.models) == 1
    isotropic_elasticity = material.models[0]
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
    assert isotropic_elasticity.independent_parameters[0].values.value.tolist() == [12, 21]
    assert isotropic_elasticity.independent_parameters[0].values.unit == "C"
    assert isotropic_elasticity.independent_parameters[0].upper_limit == 1.18329135783152e-30
    assert isotropic_elasticity.independent_parameters[0].lower_limit == 3.94430452610506e-31
    assert isotropic_elasticity.independent_parameters[0].default_value == 22.0
    assert isotropic_elasticity.youngs_modulus.value.tolist() == [2000000, 1000000]
    assert isotropic_elasticity.youngs_modulus.unit == "Pa"
    assert isotropic_elasticity.poissons_ratio.value.tolist() == [0.35, 0.3]
    assert isotropic_elasticity.poissons_ratio.unit == ""


def test_read_variable_elastic_orthotropic_material():
    matml_reader = MatmlReader(XML_FILE_PATH)
    materials = matml_reader.convert_matml_materials()
    material = materials["Variable Orthotropic Test Material"]
    assert len(material.models) == 1
    orthotropic_elasticity = material.models[0]
    assert orthotropic_elasticity.name == "Elasticity"
    assert orthotropic_elasticity.model_qualifiers[0].name == "Behavior"
    assert orthotropic_elasticity.model_qualifiers[0].value == "Orthotropic"
    assert orthotropic_elasticity.model_qualifiers[1].name == "Field Variable Compatible"
    assert orthotropic_elasticity.model_qualifiers[1].value == "Temperature"
    assert orthotropic_elasticity.interpolation_options.algorithm_type == "Linear Multivariate"
    assert orthotropic_elasticity.interpolation_options.cached == True
    assert orthotropic_elasticity.interpolation_options.normalized == True
    assert orthotropic_elasticity.youngs_modulus_x.value.tolist() == [10000000.0, 11000000.0]
    assert orthotropic_elasticity.youngs_modulus_x.unit == "Pa"
    assert orthotropic_elasticity.youngs_modulus_y.value.tolist() == [15000000.0, 15100000]
    assert orthotropic_elasticity.youngs_modulus_y.unit == "Pa"
    assert orthotropic_elasticity.youngs_modulus_z.value.tolist() == [20000000.0, 21000000]
    assert orthotropic_elasticity.youngs_modulus_z.unit == "Pa"
    assert orthotropic_elasticity.poissons_ratio_xy.value.tolist() == [0.2, 0.21]
    assert orthotropic_elasticity.poissons_ratio_xy.unit == ""
    assert orthotropic_elasticity.poissons_ratio_yz.value.tolist() == [0.3, 0.31]
    assert orthotropic_elasticity.poissons_ratio_yz.unit == ""
    assert orthotropic_elasticity.poissons_ratio_xz.value.tolist() == [0.4, 0.41]
    assert orthotropic_elasticity.poissons_ratio_xz.unit == ""
    assert orthotropic_elasticity.shear_modulus_xy.value.tolist() == [1000000.0, 1100000]
    assert orthotropic_elasticity.shear_modulus_xy.unit == "Pa"
    assert orthotropic_elasticity.shear_modulus_yz.value.tolist() == [2000000.0, 2100000]
    assert orthotropic_elasticity.shear_modulus_yz.unit == "Pa"
    assert orthotropic_elasticity.shear_modulus_xz.value.tolist() == [3000000.0, 3100000]
    assert orthotropic_elasticity.shear_modulus_xz.unit == "Pa"
    assert orthotropic_elasticity.independent_parameters[0].name == "Temperature"
    assert orthotropic_elasticity.independent_parameters[0].values.value.tolist() == [21, 22]
    assert orthotropic_elasticity.independent_parameters[0].values.unit == "C"
    assert orthotropic_elasticity.independent_parameters[0].upper_limit == 1.18329135783152e-30
    assert orthotropic_elasticity.independent_parameters[0].lower_limit == 3.94430452610506e-31
    assert orthotropic_elasticity.independent_parameters[0].default_value == 22.0
