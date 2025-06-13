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
INSTANTANEOUS_XML_FILE_PATH = os.path.join(
    DIR_PATH, "..", "data", "MatML_unittest_instantaneous_thermal_coeffs.xml"
)
SECANT_XML_FILE_PATH = os.path.join(DIR_PATH, "..", "data", "MatML_unittest_thermal_coeffs.xml")


def test_read_constant_isotropic_instantaneous_cte_material():
    material_dic = read_matml_file(INSTANTANEOUS_XML_FILE_PATH)
    assert "Mat with constant isotropic instantaneous CTE" in material_dic.keys()
    assert len(material_dic["Mat with constant isotropic instantaneous CTE"].models) == 1
    isotropic_cte = material_dic["Mat with constant isotropic instantaneous CTE"].models[0]
    assert isotropic_cte.name == "Coefficient of Thermal Expansion"
    assert isotropic_cte.model_qualifiers[0].name == "Definition"
    assert isotropic_cte.model_qualifiers[0].value == "Instantaneous"
    assert isotropic_cte.model_qualifiers[1].name == "Behavior"
    assert isotropic_cte.model_qualifiers[1].value == "Isotropic"
    assert isotropic_cte.coefficient_of_thermal_expansion == [1.0e-05]
    assert isotropic_cte.independent_parameters[0].name == "Temperature"
    assert isotropic_cte.independent_parameters[0].values == [7.88860905221012e-31]


def test_read_constant_orthotropic_instantaneous_cte_material():
    material_dic = read_matml_file(INSTANTANEOUS_XML_FILE_PATH)
    assert "Mat with constant orthotropic instanteous CTE" in material_dic.keys()
    assert len(material_dic["Mat with constant orthotropic instanteous CTE"].models) == 1
    orthotropic_cte = material_dic["Mat with constant orthotropic instanteous CTE"].models[0]
    assert orthotropic_cte.name == "Coefficient of Thermal Expansion"
    assert orthotropic_cte.model_qualifiers[0].name == "Definition"
    assert orthotropic_cte.model_qualifiers[0].value == "Instantaneous"
    assert orthotropic_cte.model_qualifiers[1].name == "Behavior"
    assert orthotropic_cte.model_qualifiers[1].value == "Orthotropic"
    assert orthotropic_cte.coefficient_of_thermal_expansion_x == [1.0e-05]
    assert orthotropic_cte.coefficient_of_thermal_expansion_y == [2.0e-05]
    assert orthotropic_cte.coefficient_of_thermal_expansion_z == [3.0e-05]
    assert orthotropic_cte.independent_parameters[0].name == "Temperature"
    assert orthotropic_cte.independent_parameters[0].values == [7.88860905221012e-31]


def test_read_variable_isotropic_instantaneous_cte_material():
    material_dic = read_matml_file(INSTANTANEOUS_XML_FILE_PATH)
    assert "Mat with variable isotropic instantaneous CTE" in material_dic.keys()
    assert len(material_dic["Mat with variable isotropic instantaneous CTE"].models) == 1
    isotropic_cte = material_dic["Mat with variable isotropic instantaneous CTE"].models[0]
    assert isotropic_cte.name == "Coefficient of Thermal Expansion"
    assert isotropic_cte.model_qualifiers[0].name == "Definition"
    assert isotropic_cte.model_qualifiers[0].value == "Instantaneous"
    assert isotropic_cte.model_qualifiers[1].name == "Behavior"
    assert isotropic_cte.model_qualifiers[1].value == "Isotropic"
    assert isotropic_cte.coefficient_of_thermal_expansion == [1e-05, 1.2e-05]
    assert isotropic_cte.independent_parameters[0].name == "Temperature"
    assert isotropic_cte.independent_parameters[0].values == [10, 20]


def test_read_variable_orthotropic_instantaneous_cte_material():
    material_dic = read_matml_file(INSTANTANEOUS_XML_FILE_PATH)
    assert "Mat with variable orthotropic instantaneous CTE" in material_dic.keys()
    assert len(material_dic["Mat with variable orthotropic instantaneous CTE"].models) == 1
    orthotropic_cte = material_dic["Mat with variable orthotropic instantaneous CTE"].models[0]
    assert orthotropic_cte.name == "Coefficient of Thermal Expansion"
    assert orthotropic_cte.model_qualifiers[0].name == "Definition"
    assert orthotropic_cte.model_qualifiers[0].value == "Instantaneous"
    assert orthotropic_cte.model_qualifiers[1].name == "Behavior"
    assert orthotropic_cte.model_qualifiers[1].value == "Orthotropic"
    assert orthotropic_cte.coefficient_of_thermal_expansion_x == [1e-05, 1.2e-05]
    assert orthotropic_cte.coefficient_of_thermal_expansion_y == [2.0e-05, 2.2e-05]
    assert orthotropic_cte.coefficient_of_thermal_expansion_z == [3e-05, 3.2e-05]
    assert orthotropic_cte.independent_parameters[0].name == "Temperature"
    assert orthotropic_cte.independent_parameters[0].values == [10, 20]


def test_read_constant_isotropic_secant_cte_material():
    material_dic = read_matml_file(SECANT_XML_FILE_PATH)
    assert "material with isotropic thermal expansion coefficients" in material_dic.keys()
    assert len(material_dic["material with isotropic thermal expansion coefficients"].models) == 2
    isotropic_cte = material_dic["material with isotropic thermal expansion coefficients"].models[0]
    zero_thermal_strain_reference_temperature = material_dic[
        "material with isotropic thermal expansion coefficients"
    ].models[1]
    assert isotropic_cte.name == "Coefficient of Thermal Expansion"
    assert isotropic_cte.model_qualifiers[0].name == "Definition"
    assert isotropic_cte.model_qualifiers[0].value == "Secant"
    assert isotropic_cte.model_qualifiers[1].name == "Behavior"
    assert isotropic_cte.model_qualifiers[1].value == "Isotropic"
    assert isotropic_cte.coefficient_of_thermal_expansion == [0.1]
    assert isotropic_cte.independent_parameters[0].name == "Temperature"
    assert isotropic_cte.independent_parameters[0].values == [7.88860905221012e-31]
    assert (
        zero_thermal_strain_reference_temperature.name
        == "Zero-Thermal-Strain Reference Temperature"
    )
    assert zero_thermal_strain_reference_temperature.model_qualifiers[0].name == "Definition"
    assert zero_thermal_strain_reference_temperature.model_qualifiers[0].value == "Secant"
    assert zero_thermal_strain_reference_temperature.model_qualifiers[1].name == "Behavior"
    assert zero_thermal_strain_reference_temperature.model_qualifiers[1].value == "Isotropic"
    assert zero_thermal_strain_reference_temperature.zero_thermal_strain_reference_temperature == [
        25.0
    ]
    assert (
        zero_thermal_strain_reference_temperature.material_property
        == "Coefficient of Thermal Expansion"
    )


def test_read_constant_orthotropic_secant_cte_material():
    material_dic = read_matml_file(SECANT_XML_FILE_PATH)
    assert "material with orthotropic thermal expansion coefficients" in material_dic.keys()
    assert len(material_dic["material with orthotropic thermal expansion coefficients"].models) == 2
    orthotropic_cte = material_dic[
        "material with orthotropic thermal expansion coefficients"
    ].models[0]
    zero_thermal_strain_reference_temperature = material_dic[
        "material with orthotropic thermal expansion coefficients"
    ].models[1]
    assert orthotropic_cte.name == "Coefficient of Thermal Expansion"
    assert orthotropic_cte.model_qualifiers[0].name == "Definition"
    assert orthotropic_cte.model_qualifiers[0].value == "Secant"
    assert orthotropic_cte.model_qualifiers[1].name == "Behavior"
    assert orthotropic_cte.model_qualifiers[1].value == "Orthotropic"
    assert orthotropic_cte.coefficient_of_thermal_expansion_x == [0.1]
    assert orthotropic_cte.coefficient_of_thermal_expansion_y == [0.2]
    assert orthotropic_cte.coefficient_of_thermal_expansion_z == [0.3]
    assert orthotropic_cte.independent_parameters[0].name == "Temperature"
    assert orthotropic_cte.independent_parameters[0].values == [7.88860905221012e-31]
    assert (
        zero_thermal_strain_reference_temperature.name
        == "Zero-Thermal-Strain Reference Temperature"
    )
    assert zero_thermal_strain_reference_temperature.model_qualifiers[0].name == "Definition"
    assert zero_thermal_strain_reference_temperature.model_qualifiers[0].value == "Secant"
    assert zero_thermal_strain_reference_temperature.model_qualifiers[1].name == "Behavior"
    assert zero_thermal_strain_reference_temperature.model_qualifiers[1].value == "Orthotropic"
    assert zero_thermal_strain_reference_temperature.zero_thermal_strain_reference_temperature == [
        27.0
    ]
    assert (
        zero_thermal_strain_reference_temperature.material_property
        == "Coefficient of Thermal Expansion"
    )


def test_read_variable_isotropic_secant_cte_material():
    material_dic = read_matml_file(SECANT_XML_FILE_PATH)
    assert "material with variable isotropic thermal expansion coefficients" in material_dic.keys()
    assert (
        len(material_dic["material with variable isotropic thermal expansion coefficients"].models)
        == 2
    )
    isotropic_cte = material_dic[
        "material with variable isotropic thermal expansion coefficients"
    ].models[0]
    zero_thermal_strain_reference_temperature = material_dic[
        "material with variable isotropic thermal expansion coefficients"
    ].models[1]
    assert isotropic_cte.name == "Coefficient of Thermal Expansion"
    assert isotropic_cte.model_qualifiers[0].name == "Definition"
    assert isotropic_cte.model_qualifiers[0].value == "Secant"
    assert isotropic_cte.model_qualifiers[1].name == "Behavior"
    assert isotropic_cte.model_qualifiers[1].value == "Isotropic"
    assert isotropic_cte.coefficient_of_thermal_expansion == [0.1, 0.4, 0.2]
    assert isotropic_cte.independent_parameters[0].name == "Temperature"
    assert isotropic_cte.independent_parameters[0].values == [12, 21, 24]
    assert (
        zero_thermal_strain_reference_temperature.name
        == "Zero-Thermal-Strain Reference Temperature"
    )
    assert zero_thermal_strain_reference_temperature.model_qualifiers[0].name == "Definition"
    assert zero_thermal_strain_reference_temperature.model_qualifiers[0].value == "Secant"
    assert zero_thermal_strain_reference_temperature.model_qualifiers[1].name == "Behavior"
    assert zero_thermal_strain_reference_temperature.model_qualifiers[1].value == "Isotropic"
    assert zero_thermal_strain_reference_temperature.zero_thermal_strain_reference_temperature == [
        25.0
    ]
    assert (
        zero_thermal_strain_reference_temperature.material_property
        == "Coefficient of Thermal Expansion"
    )


def test_read_variable_orthotropic_secant_cte_material():
    material_dic = read_matml_file(SECANT_XML_FILE_PATH)
    assert (
        "material with variable orthotropic thermal expansion coefficients" in material_dic.keys()
    )
    assert (
        len(
            material_dic["material with variable orthotropic thermal expansion coefficients"].models
        )
        == 2
    )
    orthotropic_cte = material_dic[
        "material with variable orthotropic thermal expansion coefficients"
    ].models[0]
    zero_thermal_strain_reference_temperature = material_dic[
        "material with variable orthotropic thermal expansion coefficients"
    ].models[1]
    assert orthotropic_cte.name == "Coefficient of Thermal Expansion"
    assert orthotropic_cte.model_qualifiers[0].name == "Definition"
    assert orthotropic_cte.model_qualifiers[0].value == "Secant"
    assert orthotropic_cte.model_qualifiers[1].name == "Behavior"
    assert orthotropic_cte.model_qualifiers[1].value == "Orthotropic"
    assert orthotropic_cte.coefficient_of_thermal_expansion_x == [0.1, 0.2, 0.3]
    assert orthotropic_cte.coefficient_of_thermal_expansion_y == [0.2, 0.15, 0.1]
    assert orthotropic_cte.coefficient_of_thermal_expansion_z == [0.3, 0.2, 0.1]
    assert orthotropic_cte.independent_parameters[0].name == "Temperature"
    assert orthotropic_cte.independent_parameters[0].values == [12, 23, 26]
    assert (
        zero_thermal_strain_reference_temperature.name
        == "Zero-Thermal-Strain Reference Temperature"
    )
    assert zero_thermal_strain_reference_temperature.model_qualifiers[0].name == "Definition"
    assert zero_thermal_strain_reference_temperature.model_qualifiers[0].value == "Secant"
    assert zero_thermal_strain_reference_temperature.model_qualifiers[1].name == "Behavior"
    assert zero_thermal_strain_reference_temperature.model_qualifiers[1].value == "Orthotropic"
    assert zero_thermal_strain_reference_temperature.zero_thermal_strain_reference_temperature == [
        27.0
    ]
    assert (
        zero_thermal_strain_reference_temperature.material_property
        == "Coefficient of Thermal Expansion"
    )
