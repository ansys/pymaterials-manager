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
XML_FILE_PATH = DIR_PATH.joinpath("..", "data", "matml_unittest_specific_heat.xml")
SPECIFIC_HEAT_VOLUME = DIR_PATH.joinpath("..", "data", "matml_specific_heat_volume.txt")
SPECIFIC_HEAT_METADATA = DIR_PATH.joinpath("..", "data", "matml_specific_heat_volume_metadata.txt")
SPECIFIC_HEAT_VOLUME_VARIABLE = DIR_PATH.joinpath(
    "..", "data", "matml_specific_heat_volume_variable.txt"
)
SPECIFIC_HEAT_PRESSURE = DIR_PATH.joinpath("..", "data", "matml_specific_heat_pressure.txt")
SPECIFIC_HEAT_PRESSURE_VARIABLE = DIR_PATH.joinpath(
    "..", "data", "matml_specific_heat_pressure_variable.txt"
)


def test_read_constant_specific_heat_volume():
    matml_reader = MatmlReader(XML_FILE_PATH)
    materials = matml_reader.convert_matml_materials()
    material = materials["material with specific heat volume"]
    assert len(material.models) == 1
    specific_heat = material.models[0]
    assert specific_heat.name == "Specific Heat"
    assert specific_heat.model_qualifiers[0].name == "Definition"
    assert specific_heat.model_qualifiers[0].value == "Constant Volume"
    assert specific_heat.model_qualifiers[1].name == "Field Variable Compatible"
    assert specific_heat.model_qualifiers[1].value == "Temperature"
    assert specific_heat.model_qualifiers[2].name == "Symbol"
    assert specific_heat.model_qualifiers[2].value == "Cᵥ"
    assert specific_heat.independent_parameters[0].name == "Temperature"
    assert specific_heat.independent_parameters[0].values.value == [22.0]
    assert specific_heat.independent_parameters[0].values.unit == "C"
    assert specific_heat.independent_parameters[0].upper_limit == "Program Controlled"
    assert specific_heat.independent_parameters[0].lower_limit == "Program Controlled"
    assert specific_heat.independent_parameters[0].default_value == 22.0
    assert specific_heat.specific_heat.value == [2.0]
    assert specific_heat.specific_heat.unit == "J kg^-1 C^-1"


def test_read_variable_specific_heat_volume():
    matml_reader = MatmlReader(XML_FILE_PATH)
    materials = matml_reader.convert_matml_materials()
    material = materials["material with variable specific heat volume"]
    assert len(material.models) == 1
    specific_heat = material.models[0]
    assert specific_heat.name == "Specific Heat"
    assert specific_heat.model_qualifiers[0].name == "Definition"
    assert specific_heat.model_qualifiers[0].value == "Constant Volume"
    assert specific_heat.model_qualifiers[1].name == "Field Variable Compatible"
    assert specific_heat.model_qualifiers[1].value == "Temperature"
    assert specific_heat.model_qualifiers[2].name == "Symbol"
    assert specific_heat.model_qualifiers[2].value == "Cᵥ"
    assert specific_heat.independent_parameters[0].name == "Temperature"
    assert specific_heat.independent_parameters[0].values.value.tolist() == [22.0, 40.0, 60.0]
    assert specific_heat.independent_parameters[0].values.unit == "C"
    assert specific_heat.independent_parameters[0].upper_limit == "Program Controlled"
    assert specific_heat.independent_parameters[0].lower_limit == "Program Controlled"
    assert specific_heat.independent_parameters[0].default_value == 22.0
    assert specific_heat.specific_heat.value.tolist() == [10.0, 20.0, 30.0]
    assert specific_heat.specific_heat.unit == "J kg^-1 C^-1"


def test_read_constant_specific_heat_pressure():
    matml_reader = MatmlReader(XML_FILE_PATH)
    materials = matml_reader.convert_matml_materials()
    material = materials["material with specific heat pressure"]
    assert len(material.models) == 1
    specific_heat = material.models[0]
    assert specific_heat.name == "Specific Heat"
    assert specific_heat.model_qualifiers[0].name == "Definition"
    assert specific_heat.model_qualifiers[0].value == "Constant Pressure"
    assert specific_heat.model_qualifiers[1].name == "Field Variable Compatible"
    assert specific_heat.model_qualifiers[1].value == "Temperature"
    assert specific_heat.model_qualifiers[2].name == "Symbol"
    assert specific_heat.model_qualifiers[2].value == "Cᵨ"
    assert specific_heat.independent_parameters[0].name == "Temperature"
    assert specific_heat.independent_parameters[0].values.value == [22.0]
    assert specific_heat.independent_parameters[0].values.unit == "C"
    assert specific_heat.independent_parameters[0].upper_limit == "Program Controlled"
    assert specific_heat.independent_parameters[0].lower_limit == "Program Controlled"
    assert specific_heat.independent_parameters[0].default_value == 22.0
    assert specific_heat.specific_heat.value == [1.0]
    assert specific_heat.specific_heat.unit == "J kg^-1 C^-1"
    assert specific_heat.interpolation_options.algorithm_type == "Linear Multivariate"
    assert specific_heat.interpolation_options.cached is True
    assert specific_heat.interpolation_options.normalized is True
    assert (
        specific_heat.interpolation_options.extrapolation_type == "Projection to the Bounding Box"
    )


def test_read_variable_specific_heat_pressure():
    matml_reader = MatmlReader(XML_FILE_PATH)
    materials = matml_reader.convert_matml_materials()
    material = materials["material with variable specific heat pressure"]
    assert len(material.models) == 1
    specific_heat = material.models[0]
    assert specific_heat.name == "Specific Heat"
    assert specific_heat.model_qualifiers[0].name == "Definition"
    assert specific_heat.model_qualifiers[0].value == "Constant Pressure"
    assert specific_heat.model_qualifiers[1].name == "Field Variable Compatible"
    assert specific_heat.model_qualifiers[1].value == "Temperature"
    assert specific_heat.model_qualifiers[2].name == "Symbol"
    assert specific_heat.model_qualifiers[2].value == "Cᵨ"
    assert specific_heat.independent_parameters[0].name == "Temperature"
    assert specific_heat.independent_parameters[0].values.value.tolist() == [22.0, 50.0, 75.0]
    assert specific_heat.independent_parameters[0].values.unit == "C"
    assert specific_heat.independent_parameters[0].upper_limit == "Program Controlled"
    assert specific_heat.independent_parameters[0].lower_limit == "Program Controlled"
    assert specific_heat.independent_parameters[0].default_value == 22.0
    assert specific_heat.specific_heat.value.tolist() == [1.0, 2.0, 3.0]
    assert specific_heat.specific_heat.unit == "J kg^-1 C^-1"
    assert specific_heat.interpolation_options.algorithm_type == "Linear Multivariate"
    assert specific_heat.interpolation_options.cached is True
    assert specific_heat.interpolation_options.normalized is True
    assert (
        specific_heat.interpolation_options.extrapolation_type == "Projection to the Bounding Box"
    )
