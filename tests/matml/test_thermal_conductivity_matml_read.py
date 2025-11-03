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
XML_FILE_PATH = DIR_PATH.joinpath("..", "data", "matml_unittest_thermal_conductivity.xml")
THERMAL_CONDUCTIVITY_ISOTROPIC = DIR_PATH.joinpath(
    "..", "data", "matml_thermal_conductivity_isotropic.txt"
)
THERMAL_CONDUCTIVITY_ISOTROPIC_METADATA = DIR_PATH.joinpath(
    "..", "data", "matml_thermal_conductivity_isotropic_metadata.txt"
)
THERMAL_CONDUCTIVITY_ORTHOTROPIC = DIR_PATH.joinpath(
    "..", "data", "matml_thermal_conductivity_orthotropic.txt"
)
THERMAL_CONDUCTIVITY_ORTHOTROPIC_METADATA = DIR_PATH.joinpath(
    "..", "data", "matml_thermal_conductivity_orthotropic_metadata.txt"
)


def test_read_thermal_conductivity_isotropic_material():
    matml_reader = MatmlReader(XML_FILE_PATH)
    materials = matml_reader.convert_matml_materials()
    material = materials["Isotropic Convection Test Material"]
    assert len(material.models) == 1
    isotropic_conductivity = material.models[0]
    assert isotropic_conductivity.name == "Thermal Conductivity"
    assert isotropic_conductivity.model_qualifiers[0].name == "Behavior"
    assert isotropic_conductivity.model_qualifiers[0].value == "Isotropic"
    assert isotropic_conductivity.model_qualifiers[1].name == "Field Variable Compatible"
    assert isotropic_conductivity.model_qualifiers[1].value == "Temperature"
    assert isotropic_conductivity.thermal_conductivity.value == [10.0]
    assert isotropic_conductivity.thermal_conductivity.unit == "W m^-1 C^-1"
    assert isotropic_conductivity.independent_parameters[0].name == "Temperature"
    assert isotropic_conductivity.independent_parameters[0].values.value == [7.88860905221012e-31]
    assert isotropic_conductivity.independent_parameters[0].values.unit == "C"
    assert isotropic_conductivity.independent_parameters[0].upper_limit == "Program Controlled"
    assert isotropic_conductivity.independent_parameters[0].lower_limit == "Program Controlled"
    assert isotropic_conductivity.independent_parameters[0].default_value == 22.0


def test_read_thermal_conductivity_orthotropic_material():
    matml_reader = MatmlReader(XML_FILE_PATH)
    materials = matml_reader.convert_matml_materials()
    material = materials["Orthotropic Convection Test Material"]
    assert len(material.models) == 1
    orthotropic_conductivity = material.models[0]
    assert orthotropic_conductivity.name == "Thermal Conductivity"
    assert orthotropic_conductivity.model_qualifiers[0].name == "Behavior"
    assert orthotropic_conductivity.model_qualifiers[0].value == "Orthotropic"
    assert orthotropic_conductivity.thermal_conductivity_x.value == [10.0]
    assert orthotropic_conductivity.thermal_conductivity_x.unit == "W m^-1 C^-1"
    assert orthotropic_conductivity.thermal_conductivity_y.value == [15.0]
    assert orthotropic_conductivity.thermal_conductivity_y.unit == "W m^-1 C^-1"
    assert orthotropic_conductivity.thermal_conductivity_z.value == [20.0]
    assert orthotropic_conductivity.thermal_conductivity_z.unit == "W m^-1 C^-1"
    assert orthotropic_conductivity.independent_parameters[0].name == "Temperature"
    assert orthotropic_conductivity.independent_parameters[0].values.value == [7.88860905221012e-31]
    assert orthotropic_conductivity.independent_parameters[0].values.unit == "C"
