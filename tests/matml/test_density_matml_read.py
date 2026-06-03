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
XML_FILE_PATH = DIR_PATH.joinpath("..", "data", "matml_unittest_density.xml")


def test_read_material_with_constant_density():
    matml_reader = MatmlReader(XML_FILE_PATH)
    materials = matml_reader.convert_matml_materials()
    constant_density_material = materials["material with density"]
    assert len(constant_density_material.models) == 1
    density = constant_density_material.models[0]
    assert density.name == "Density"
    assert density.density.value == [1.34]
    assert density.density.unit == "kg m^-3"
    assert len(density.independent_parameters) == 1
    assert density.independent_parameters[0].name == "Temperature"
    assert density.independent_parameters[0].values.value == [7.88860905221012e-31]
    assert density.independent_parameters[0].values.unit == "C"


def test_read_model_with_variable_density():
    matml_reader = MatmlReader(XML_FILE_PATH)
    materials = matml_reader.convert_matml_materials()
    variable_density_material = materials["material with variable density"]
    assert len(variable_density_material.models) == 1
    density = variable_density_material.models[0]
    assert density.name == "Density"
    assert density.density.value.tolist() == [12.0, 32.0, 38.0]
    assert density.density.unit == "kg m^-3"
    assert len(density.independent_parameters) == 1
    assert density.independent_parameters[0].name == "Temperature"
    assert density.independent_parameters[0].values.value.tolist() == [
        20.0,
        21.0,
        23.0,
    ]
    assert density.independent_parameters[0].values.unit == "C"
