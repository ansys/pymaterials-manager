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
XML_FILE_PATH = os.path.join(DIR_PATH, "..", "data", "MatML_unittest_specific_heat.xml")


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
    assert specific_heat.independent_parameters[0].units == "C"
    assert specific_heat.independent_parameters[0].upper_limit == "Program Controlled"
    assert specific_heat.independent_parameters[0].lower_limit == "Program Controlled"
    assert specific_heat.independent_parameters[0].default_value == "22"
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
    assert specific_heat.independent_parameters[0].units == "C"
    assert specific_heat.independent_parameters[0].upper_limit == "Program Controlled"
    assert specific_heat.independent_parameters[0].lower_limit == "Program Controlled"
    assert specific_heat.independent_parameters[0].default_value == "22"
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
    assert specific_heat.independent_parameters[0].units == "C"
    assert specific_heat.independent_parameters[0].upper_limit == "Program Controlled"
    assert specific_heat.independent_parameters[0].lower_limit == "Program Controlled"
    assert specific_heat.independent_parameters[0].default_value == "22"
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
    assert specific_heat.independent_parameters[0].units == "C"
    assert specific_heat.independent_parameters[0].upper_limit == "Program Controlled"
    assert specific_heat.independent_parameters[0].lower_limit == "Program Controlled"
    assert specific_heat.independent_parameters[0].default_value == "22"
    assert specific_heat.specific_heat == [1.0, 2.0, 3.0]
    assert specific_heat.interpolation_options.algorithm_type == "Linear Multivariate"
    assert specific_heat.interpolation_options.cached is True
    assert specific_heat.interpolation_options.normalized is True
    assert (
        specific_heat.interpolation_options.extrapolation_type == "Projection to the Bounding Box"
    )
