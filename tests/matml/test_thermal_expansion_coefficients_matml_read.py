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
INSTANTANEOUS_XML_FILE_PATH = DIR_PATH.joinpath(
    "..", "data", "matml_unittest_instantaneous_thermal_coeffs.xml"
)
SECANT_XML_FILE_PATH = DIR_PATH.joinpath("..", "data", "matml_unittest_thermal_coeffs.xml")


def test_read_constant_isotropic_instantaneous_cte_material():
    matml_reader = MatmlReader(INSTANTANEOUS_XML_FILE_PATH)
    materials = matml_reader.convert_matml_materials()
    material = materials["Mat with constant isotropic instantaneous CTE"]
    assert len(material.models) == 1
    isotropic_cte = material.models[0]
    assert isotropic_cte.name == "Coefficient of Thermal Expansion"
    assert isotropic_cte.model_qualifiers[0].name == "Definition"
    assert isotropic_cte.model_qualifiers[0].value == "Instantaneous"
    assert isotropic_cte.model_qualifiers[1].name == "Behavior"
    assert isotropic_cte.model_qualifiers[1].value == "Isotropic"
    assert isotropic_cte.coefficient_of_thermal_expansion.value == [1.0e-05]
    assert isotropic_cte.coefficient_of_thermal_expansion.unit == "C^-1"
    assert isotropic_cte.independent_parameters[0].name == "Temperature"
    assert isotropic_cte.independent_parameters[0].values.value == [7.88860905221012e-31]
    assert isotropic_cte.independent_parameters[0].values.unit == "C"


def test_read_constant_orthotropic_instantaneous_cte_material():
    matml_reader = MatmlReader(INSTANTANEOUS_XML_FILE_PATH)
    materials = matml_reader.convert_matml_materials()
    material = materials["Mat with constant orthotropic instantaneous CTE"]
    assert len(material.models) == 1
    orthotropic_cte = material.models[0]
    assert orthotropic_cte.name == "Coefficient of Thermal Expansion"
    assert orthotropic_cte.model_qualifiers[0].name == "Definition"
    assert orthotropic_cte.model_qualifiers[0].value == "Instantaneous"
    assert orthotropic_cte.model_qualifiers[1].name == "Behavior"
    assert orthotropic_cte.model_qualifiers[1].value == "Orthotropic"
    assert orthotropic_cte.coefficient_of_thermal_expansion_x.value == [1.0e-05]
    assert orthotropic_cte.coefficient_of_thermal_expansion_x.unit == "C^-1"
    assert orthotropic_cte.coefficient_of_thermal_expansion_y.value == [2.0e-05]
    assert orthotropic_cte.coefficient_of_thermal_expansion_y.unit == "C^-1"
    assert orthotropic_cte.coefficient_of_thermal_expansion_z.value == [3.0e-05]
    assert orthotropic_cte.coefficient_of_thermal_expansion_z.unit == "C^-1"
    assert orthotropic_cte.independent_parameters[0].name == "Temperature"
    assert orthotropic_cte.independent_parameters[0].values.value == [7.88860905221012e-31]
    assert orthotropic_cte.independent_parameters[0].values.unit == "C"


def test_read_variable_isotropic_instantaneous_cte_material():
    matml_reader = MatmlReader(INSTANTANEOUS_XML_FILE_PATH)
    materials = matml_reader.convert_matml_materials()
    material = materials["Mat with variable isotropic instantaneous CTE"]
    assert len(material.models) == 1
    isotropic_cte = material.models[0]
    assert isotropic_cte.name == "Coefficient of Thermal Expansion"
    assert isotropic_cte.model_qualifiers[0].name == "Definition"
    assert isotropic_cte.model_qualifiers[0].value == "Instantaneous"
    assert isotropic_cte.model_qualifiers[1].name == "Behavior"
    assert isotropic_cte.model_qualifiers[1].value == "Isotropic"
    assert isotropic_cte.coefficient_of_thermal_expansion.value.tolist() == [1e-05, 1.2e-05]
    assert isotropic_cte.coefficient_of_thermal_expansion.unit == "C^-1"
    assert isotropic_cte.independent_parameters[0].name == "Temperature"
    assert isotropic_cte.independent_parameters[0].values.value.tolist() == [10, 20]
    assert isotropic_cte.independent_parameters[0].values.unit == "C"


def test_read_variable_orthotropic_instantaneous_cte_material():
    matml_reader = MatmlReader(INSTANTANEOUS_XML_FILE_PATH)
    materials = matml_reader.convert_matml_materials()
    material = materials["Mat with variable orthotropic instantaneous CTE"]
    assert len(material.models) == 1
    orthotropic_cte = material.models[0]
    assert orthotropic_cte.name == "Coefficient of Thermal Expansion"
    assert orthotropic_cte.model_qualifiers[0].name == "Definition"
    assert orthotropic_cte.model_qualifiers[0].value == "Instantaneous"
    assert orthotropic_cte.model_qualifiers[1].name == "Behavior"
    assert orthotropic_cte.model_qualifiers[1].value == "Orthotropic"
    assert orthotropic_cte.coefficient_of_thermal_expansion_x.value.tolist() == [1e-05, 1.2e-05]
    assert orthotropic_cte.coefficient_of_thermal_expansion_x.unit == "C^-1"
    assert orthotropic_cte.coefficient_of_thermal_expansion_y.value.tolist() == [2.0e-05, 2.2e-05]
    assert orthotropic_cte.coefficient_of_thermal_expansion_y.unit == "C^-1"
    assert orthotropic_cte.coefficient_of_thermal_expansion_z.value.tolist() == [3e-05, 3.2e-05]
    assert orthotropic_cte.coefficient_of_thermal_expansion_z.unit == "C^-1"
    assert orthotropic_cte.independent_parameters[0].name == "Temperature"
    assert orthotropic_cte.independent_parameters[0].values.value.tolist() == [10, 20]
    assert orthotropic_cte.independent_parameters[0].values.unit == "C"


def test_read_constant_isotropic_secant_cte_material():
    matml_reader = MatmlReader(SECANT_XML_FILE_PATH)
    materials = matml_reader.convert_matml_materials()
    material = materials["material with isotropic thermal expansion coefficients"]
    assert len(material.models) == 2
    isotropic_cte = material.models[0]
    zero_thermal_strain_reference_temperature = material.models[1]
    assert isotropic_cte.name == "Coefficient of Thermal Expansion"
    assert isotropic_cte.model_qualifiers[0].name == "Definition"
    assert isotropic_cte.model_qualifiers[0].value == "Secant"
    assert isotropic_cte.model_qualifiers[1].name == "Behavior"
    assert isotropic_cte.model_qualifiers[1].value == "Isotropic"
    assert isotropic_cte.coefficient_of_thermal_expansion.value == [0.1]
    assert isotropic_cte.coefficient_of_thermal_expansion.unit == "C^-1"
    assert isotropic_cte.independent_parameters[0].name == "Temperature"
    assert isotropic_cte.independent_parameters[0].values.value == [7.88860905221012e-31]
    assert (
        zero_thermal_strain_reference_temperature.name
        == "Zero-Thermal-Strain Reference Temperature"
    )
    assert isotropic_cte.independent_parameters[0].values.unit == "C"
    assert zero_thermal_strain_reference_temperature.model_qualifiers[0].name == "Definition"
    assert zero_thermal_strain_reference_temperature.model_qualifiers[0].value == "Secant"
    assert zero_thermal_strain_reference_temperature.model_qualifiers[1].name == "Behavior"
    assert zero_thermal_strain_reference_temperature.model_qualifiers[1].value == "Isotropic"
    assert (
        zero_thermal_strain_reference_temperature.zero_thermal_strain_reference_temperature.value
        == [25.0]
    )
    assert (
        zero_thermal_strain_reference_temperature.zero_thermal_strain_reference_temperature.unit
        == "C"
    )


def test_read_constant_orthotropic_secant_cte_material():
    matml_reader = MatmlReader(SECANT_XML_FILE_PATH)
    materials = matml_reader.convert_matml_materials()
    material = materials["material with orthotropic thermal expansion coefficients"]
    assert len(material.models) == 2
    orthotropic_cte = material.models[0]
    zero_thermal_strain_reference_temperature = material.models[1]
    assert orthotropic_cte.name == "Coefficient of Thermal Expansion"
    assert orthotropic_cte.model_qualifiers[0].name == "Definition"
    assert orthotropic_cte.model_qualifiers[0].value == "Secant"
    assert orthotropic_cte.model_qualifiers[1].name == "Behavior"
    assert orthotropic_cte.model_qualifiers[1].value == "Orthotropic"
    assert orthotropic_cte.coefficient_of_thermal_expansion_x.value == [0.1]
    assert orthotropic_cte.coefficient_of_thermal_expansion_x.unit == "C^-1"
    assert orthotropic_cte.coefficient_of_thermal_expansion_y.value == [0.2]
    assert orthotropic_cte.coefficient_of_thermal_expansion_y.unit == "C^-1"
    assert orthotropic_cte.coefficient_of_thermal_expansion_z.value == [0.3]
    assert orthotropic_cte.coefficient_of_thermal_expansion_z.unit == "C^-1"
    assert orthotropic_cte.independent_parameters[0].name == "Temperature"
    assert orthotropic_cte.independent_parameters[0].values.value == [7.88860905221012e-31]
    assert orthotropic_cte.independent_parameters[0].values.unit == "C"
    assert (
        zero_thermal_strain_reference_temperature.name
        == "Zero-Thermal-Strain Reference Temperature"
    )
    assert zero_thermal_strain_reference_temperature.model_qualifiers[0].name == "Definition"
    assert zero_thermal_strain_reference_temperature.model_qualifiers[0].value == "Secant"
    assert zero_thermal_strain_reference_temperature.model_qualifiers[1].name == "Behavior"
    assert zero_thermal_strain_reference_temperature.model_qualifiers[1].value == "Orthotropic"
    assert (
        zero_thermal_strain_reference_temperature.zero_thermal_strain_reference_temperature.value
        == [27.0]
    )
    assert (
        zero_thermal_strain_reference_temperature.zero_thermal_strain_reference_temperature.unit
        == "C"
    )


def test_read_variable_isotropic_secant_cte_material():
    matml_reader = MatmlReader(SECANT_XML_FILE_PATH)
    materials = matml_reader.convert_matml_materials()
    material = materials["material with variable isotropic thermal expansion coefficients"]
    assert len(material.models) == 2
    isotropic_cte = material.models[0]
    zero_thermal_strain_reference_temperature = material.models[1]
    assert isotropic_cte.name == "Coefficient of Thermal Expansion"
    assert isotropic_cte.model_qualifiers[0].name == "Definition"
    assert isotropic_cte.model_qualifiers[0].value == "Secant"
    assert isotropic_cte.model_qualifiers[1].name == "Behavior"
    assert isotropic_cte.model_qualifiers[1].value == "Isotropic"
    assert isotropic_cte.coefficient_of_thermal_expansion.value.tolist() == [0.1, 0.4, 0.2]
    assert isotropic_cte.coefficient_of_thermal_expansion.unit == "C^-1"
    assert isotropic_cte.independent_parameters[0].name == "Temperature"
    assert isotropic_cte.independent_parameters[0].values.value.tolist() == [12, 21, 24]
    assert isotropic_cte.independent_parameters[0].values.unit == "C"
    assert (
        zero_thermal_strain_reference_temperature.name
        == "Zero-Thermal-Strain Reference Temperature"
    )
    assert zero_thermal_strain_reference_temperature.model_qualifiers[0].name == "Definition"
    assert zero_thermal_strain_reference_temperature.model_qualifiers[0].value == "Secant"
    assert zero_thermal_strain_reference_temperature.model_qualifiers[1].name == "Behavior"
    assert zero_thermal_strain_reference_temperature.model_qualifiers[1].value == "Isotropic"
    assert (
        zero_thermal_strain_reference_temperature.zero_thermal_strain_reference_temperature.value
        == [25.0]
    )
    assert (
        zero_thermal_strain_reference_temperature.zero_thermal_strain_reference_temperature.unit
        == "C"
    )
    assert (
        zero_thermal_strain_reference_temperature.material_property
        == "Coefficient of Thermal Expansion"
    )


def test_read_variable_orthotropic_secant_cte_material():
    matml_reader = MatmlReader(SECANT_XML_FILE_PATH)
    materials = matml_reader.convert_matml_materials()
    material = materials["material with variable orthotropic thermal expansion coefficients"]
    assert len(material.models) == 2
    orthotropic_cte = material.models[0]
    zero_thermal_strain_reference_temperature = material.models[1]
    assert orthotropic_cte.name == "Coefficient of Thermal Expansion"
    assert orthotropic_cte.model_qualifiers[0].name == "Definition"
    assert orthotropic_cte.model_qualifiers[0].value == "Secant"
    assert orthotropic_cte.model_qualifiers[1].name == "Behavior"
    assert orthotropic_cte.model_qualifiers[1].value == "Orthotropic"
    assert orthotropic_cte.coefficient_of_thermal_expansion_x.value.tolist() == [0.1, 0.2, 0.3]
    assert orthotropic_cte.coefficient_of_thermal_expansion_x.unit == "C^-1"
    assert orthotropic_cte.coefficient_of_thermal_expansion_y.value.tolist() == [0.2, 0.15, 0.1]
    assert orthotropic_cte.coefficient_of_thermal_expansion_y.unit == "C^-1"
    assert orthotropic_cte.coefficient_of_thermal_expansion_z.value.tolist() == [0.3, 0.2, 0.1]
    assert orthotropic_cte.coefficient_of_thermal_expansion_z.unit == "C^-1"
    assert orthotropic_cte.independent_parameters[0].name == "Temperature"
    assert orthotropic_cte.independent_parameters[0].values.value.tolist() == [12, 23, 26]
    assert orthotropic_cte.independent_parameters[0].values.unit == "C"
    assert (
        zero_thermal_strain_reference_temperature.name
        == "Zero-Thermal-Strain Reference Temperature"
    )
    assert zero_thermal_strain_reference_temperature.model_qualifiers[0].name == "Definition"
    assert zero_thermal_strain_reference_temperature.model_qualifiers[0].value == "Secant"
    assert zero_thermal_strain_reference_temperature.model_qualifiers[1].name == "Behavior"
    assert zero_thermal_strain_reference_temperature.model_qualifiers[1].value == "Orthotropic"
    assert (
        zero_thermal_strain_reference_temperature.zero_thermal_strain_reference_temperature.value
        == [27.0]
    )
    assert (
        zero_thermal_strain_reference_temperature.zero_thermal_strain_reference_temperature.unit
        == "C"
    )
