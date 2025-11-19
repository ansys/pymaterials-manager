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
XML_FILE_PATH = DIR_PATH.joinpath("..", "data", "matml_unittest_neo_hookean.xml")


def test_neo_hookean_constant_matml_read():
    matml_reader = MatmlReader(XML_FILE_PATH)
    materials = matml_reader.convert_matml_materials()
    material = materials["Neo Hookean constant"]
    assert len(material.models) == 1
    neo_hookean = material.models[0]
    assert neo_hookean.name == "Neo-Hookean"
    assert neo_hookean.initial_shear_modulus.value == [27104.0]
    assert neo_hookean.initial_shear_modulus.unit == "Pa"
    assert neo_hookean.incompressibility_modulus.value == [1e-05]
    assert neo_hookean.incompressibility_modulus.unit == "Pa^-1"


def test_neo_hookean_variable_matml_read():
    matml_reader = MatmlReader(XML_FILE_PATH)
    materials = matml_reader.convert_matml_materials()
    material = materials["Neo Hookean variable"]
    assert len(material.models) == 1
    neo_hookean = material.models[0]
    assert neo_hookean.name == "Neo-Hookean"
    assert neo_hookean.initial_shear_modulus.value.tolist() == [27104.0, 2700.0, 2600.0]
    assert neo_hookean.initial_shear_modulus.unit == "Pa"
    assert neo_hookean.incompressibility_modulus.value.tolist() == [1e-05, 2e-05, 3e-05]
    assert neo_hookean.incompressibility_modulus.unit == "Pa^-1"
    assert neo_hookean.independent_parameters[0].values.value.tolist() == [22.0, 24.0, 26.0]
    assert neo_hookean.independent_parameters[0].values.unit == "C"
