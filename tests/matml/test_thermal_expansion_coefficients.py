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

from utilities import get_material_and_metadata_from_xml, read_matml_file

from ansys.materials.manager._models._common.independent_parameter import IndependentParameter
from ansys.materials.manager._models._common.model_qualifier import ModelQualifier
from ansys.materials.manager._models._material_models.cofficient_of_thermal_expansion_isotropic import (  # noqa: E501
    CoefficientofThermalExpansionIsotropic,
)
from ansys.materials.manager._models._material_models.cofficient_of_thermal_expansion_orthotropic import (  # noqa: E501
    CoefficientofThermalExpansionOrthotropic,
)
from ansys.materials.manager._models._material_models.zero_thermal_strain_reference_temperature_isotropic import (  # noqa: E501
    ZeroThermalStrainReferenceTemperatureIsotropic,
)
from ansys.materials.manager._models._material_models.zero_thermal_strain_reference_temperature_orthotropic import (  # noqa: E501
    ZeroThermalStrainReferenceTemperatureOrthotropic,
)
from ansys.materials.manager._models.material import Material
from ansys.materials.manager.util.matml.matml_from_material import MatmlWriter

from ansys.units import Quantity

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
INSTANTANEOUS_XML_FILE_PATH = os.path.join(
    DIR_PATH, "..", "data", "MatML_unittest_instantaneous_thermal_coeffs.xml"
)
SECANT_XML_FILE_PATH = os.path.join(DIR_PATH, "..", "data", "MatML_unittest_thermal_coeffs.xml")

CTE_ISOTROPIC = os.path.join(DIR_PATH, "..", "data", "cte_isotropic.txt")
CTE_ISOTROPIC_METADATA = os.path.join(DIR_PATH, "..", "data", "cte_isotropic_metadata.txt")
CTE_ORTHOTROPIC = os.path.join(DIR_PATH, "..", "data", "cte_orthotropic.txt")
CTE_ORTHOTROPIC_METADATA = os.path.join(DIR_PATH, "..", "data", "cte_orthotropic_metadata.txt")
CTE_ISOTROPIC_VARIABLE = os.path.join(DIR_PATH, "..", "data", "cte_isotropic_variable.txt")
CTE_ORTHOTROPIC_VARIABLE = os.path.join(DIR_PATH, "..", "data", "cte_orthotropic_variable.txt")

def test_read_constant_isotropic_instantaneous_cte_material():
    material_dic = read_matml_file(INSTANTANEOUS_XML_FILE_PATH)
    assert "Mat with constant isotropic instantaneous CTE" in material_dic.keys()
    assert len(material_dic["Mat with constant isotropic instantaneous CTE"].models) == 2
    isotropic_cte = material_dic["Mat with constant isotropic instantaneous CTE"].models[1]
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
    material_dic = read_matml_file(INSTANTANEOUS_XML_FILE_PATH)
    assert "Mat with constant orthotropic instanteous CTE" in material_dic.keys()
    assert len(material_dic["Mat with constant orthotropic instanteous CTE"].models) == 2
    orthotropic_cte = material_dic["Mat with constant orthotropic instanteous CTE"].models[1]
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
    material_dic = read_matml_file(INSTANTANEOUS_XML_FILE_PATH)
    assert "Mat with variable isotropic instantaneous CTE" in material_dic.keys()
    assert len(material_dic["Mat with variable isotropic instantaneous CTE"].models) == 2
    isotropic_cte = material_dic["Mat with variable isotropic instantaneous CTE"].models[1]
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
    material_dic = read_matml_file(INSTANTANEOUS_XML_FILE_PATH)
    assert "Mat with variable orthotropic instantaneous CTE" in material_dic.keys()
    assert len(material_dic["Mat with variable orthotropic instantaneous CTE"].models) == 2
    orthotropic_cte = material_dic["Mat with variable orthotropic instantaneous CTE"].models[1]
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
    material_dic = read_matml_file(SECANT_XML_FILE_PATH)
    assert "material with isotropic thermal expansion coefficients" in material_dic.keys()
    assert len(material_dic["material with isotropic thermal expansion coefficients"].models) == 3
    isotropic_cte = material_dic["material with isotropic thermal expansion coefficients"].models[1]
    zero_thermal_strain_reference_temperature = material_dic[
        "material with isotropic thermal expansion coefficients"
    ].models[2]
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
    assert zero_thermal_strain_reference_temperature.zero_thermal_strain_reference_temperature.value == [
        25.0
    ]
    assert zero_thermal_strain_reference_temperature.zero_thermal_strain_reference_temperature.unit == "C"
    assert (
        zero_thermal_strain_reference_temperature.material_property
        == "Coefficient of Thermal Expansion"
    )


def test_read_constant_orthotropic_secant_cte_material():
    material_dic = read_matml_file(SECANT_XML_FILE_PATH)
    assert "material with orthotropic thermal expansion coefficients" in material_dic.keys()
    assert len(material_dic["material with orthotropic thermal expansion coefficients"].models) == 3
    orthotropic_cte = material_dic[
        "material with orthotropic thermal expansion coefficients"
    ].models[1]
    zero_thermal_strain_reference_temperature = material_dic[
        "material with orthotropic thermal expansion coefficients"
    ].models[2]
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
    assert zero_thermal_strain_reference_temperature.zero_thermal_strain_reference_temperature.value == [
        27.0
    ]
    assert (
        zero_thermal_strain_reference_temperature.material_property
        == "Coefficient of Thermal Expansion"
    )
    assert zero_thermal_strain_reference_temperature.zero_thermal_strain_reference_temperature.unit == "C"



def test_read_variable_isotropic_secant_cte_material():
    material_dic = read_matml_file(SECANT_XML_FILE_PATH)
    assert "material with variable isotropic thermal expansion coefficients" in material_dic.keys()
    assert (
        len(material_dic["material with variable isotropic thermal expansion coefficients"].models)
        == 3
    )
    isotropic_cte = material_dic[
        "material with variable isotropic thermal expansion coefficients"
    ].models[1]
    zero_thermal_strain_reference_temperature = material_dic[
        "material with variable isotropic thermal expansion coefficients"
    ].models[2]
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
    assert zero_thermal_strain_reference_temperature.zero_thermal_strain_reference_temperature.value == [
        25.0
    ]
    assert zero_thermal_strain_reference_temperature.zero_thermal_strain_reference_temperature.unit == "C"
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
        == 3
    )
    orthotropic_cte = material_dic[
        "material with variable orthotropic thermal expansion coefficients"
    ].models[1]
    zero_thermal_strain_reference_temperature = material_dic[
        "material with variable orthotropic thermal expansion coefficients"
    ].models[2]
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
    assert zero_thermal_strain_reference_temperature.zero_thermal_strain_reference_temperature.value == [
        27.0
    ]
    assert zero_thermal_strain_reference_temperature.zero_thermal_strain_reference_temperature.unit == "C"
    assert (
        zero_thermal_strain_reference_temperature.material_property
        == "Coefficient of Thermal Expansion"
    )


def test_write_constant_cte_isotropic():
    materials = [
        Material(
            name="material with isotropic thermal expansion coefficients",
            models=[
                CoefficientofThermalExpansionIsotropic(
                    model_qualifiers=[
                        ModelQualifier(name="Definition", value="Secant"),
                        ModelQualifier(name="Behavior", value="Isotropic"),
                    ],
                    coefficient_of_thermal_expansion=Quantity(value=[0.1], units="C^-1"),
                    independent_parameters=[
                        IndependentParameter(
                            name="Temperature",
                            field_variable="Temperature",
                            values=Quantity(value=[7.88860905221012e-31], units="C"),
                        ),
                    ],
                ),
                ZeroThermalStrainReferenceTemperatureIsotropic(
                    model_qualifiers=[
                        ModelQualifier(name="Definition", value="Secant"),
                        ModelQualifier(name="Behavior", value="Isotropic"),
                    ],
                    zero_thermal_strain_reference_temperature=Quantity(value=[25.0], units="C"),
                ),
            ],
        )
    ]

    writer = MatmlWriter(materials)
    tree = writer._to_etree()
    material_string, metadata_string = get_material_and_metadata_from_xml(tree)
    with open(CTE_ISOTROPIC, 'r') as file:
        data = file.read()
        assert data == material_string
    with open(CTE_ISOTROPIC_METADATA, 'r') as file:
      data = file.read()
      assert data == metadata_string


def test_write_constant_cte_orthotropic():
    materials = [
        Material(
            name="material with orthotropic thermal expansion coefficients",
            models=[
                CoefficientofThermalExpansionOrthotropic(
                    model_qualifiers=[
                        ModelQualifier(name="Definition", value="Secant"),
                        ModelQualifier(name="Behavior", value="Orthotropic"),
                    ],
                    coefficient_of_thermal_expansion_x=Quantity(value=[0.1], units="C^-1"),
                    coefficient_of_thermal_expansion_y=Quantity(value=[0.2], units="C^-1"),
                    coefficient_of_thermal_expansion_z=Quantity(value=[0.3], units="C^-1"),
                    independent_parameters=[
                        IndependentParameter(
                            name="Temperature",
                            field_variable="Temperature",
                            values=Quantity(value=[7.88860905221012e-31], units="C"),
                        ),
                    ],
                ),
                ZeroThermalStrainReferenceTemperatureOrthotropic(
                    model_qualifiers=[
                        ModelQualifier(name="Definition", value="Secant"),
                        ModelQualifier(name="Behavior", value="Orthotropic"),
                    ],
                    zero_thermal_strain_reference_temperature=Quantity(value=[27.0], units="C"),
                ),
            ],
        )
    ]

    writer = MatmlWriter(materials)
    tree = writer._to_etree()
    material_string, metadata_string = get_material_and_metadata_from_xml(tree)
    with open(CTE_ORTHOTROPIC, 'r') as file:
        data = file.read()
        assert data == material_string
    with open(CTE_ORTHOTROPIC_METADATA, 'r') as file:
      data = file.read()
      assert data == metadata_string


def test_write_variable_cte_isotropic():
    materials = [
        Material(
            name="material with variable isotropic thermal expansion coefficients",
            models=[
                CoefficientofThermalExpansionIsotropic(
                    model_qualifiers=[
                        ModelQualifier(name="Definition", value="Secant"),
                        ModelQualifier(name="Behavior", value="Isotropic"),
                    ],
                    coefficient_of_thermal_expansion=Quantity(value=[0.1, 0.4, 0.2], units="C^-1"),
                    independent_parameters=[
                        IndependentParameter(
                            name="Temperature",
                            field_variable="Temperature",
                            values=Quantity(value=[12, 21, 24], units="C"),
                        ),
                    ],
                ),
                ZeroThermalStrainReferenceTemperatureIsotropic(
                    model_qualifiers=[
                        ModelQualifier(name="Definition", value="Secant"),
                        ModelQualifier(name="Behavior", value="Isotropic"),
                    ],
                    zero_thermal_strain_reference_temperature=Quantity(value=[25.0], units="C"),
                ),
            ],
        )
    ]

    writer = MatmlWriter(materials)
    tree = writer._to_etree()
    material_string, metadata_string = get_material_and_metadata_from_xml(tree)
    with open(CTE_ISOTROPIC_VARIABLE, 'r') as file:
        data = file.read()
        assert data == material_string
    with open(CTE_ISOTROPIC_METADATA, 'r') as file:
      data = file.read()
      assert data == metadata_string


def test_write_variable_cte_orthotropic():
    materials = [
        Material(
            name="material with variable orthotropic thermal expansion coefficients",
            models=[
                CoefficientofThermalExpansionOrthotropic(
                    model_qualifiers=[
                        ModelQualifier(name="Definition", value="Secant"),
                        ModelQualifier(name="Behavior", value="Orthotropic"),
                    ],
                    coefficient_of_thermal_expansion_x=Quantity(value=[0.1, 0.2, 0.3], units="C^-1"),
                    coefficient_of_thermal_expansion_y=Quantity(value=[0.2, 0.15, 0.1], units="C^-1"),
                    coefficient_of_thermal_expansion_z=Quantity(value=[0.3, 0.2, 0.1], units="C^-1"),
                    independent_parameters=[
                        IndependentParameter(
                            name="Temperature",
                            field_variable="Temperature",
                            values=Quantity(value=[12, 23, 26], units="C"),
                        ),
                    ],
                ),
                ZeroThermalStrainReferenceTemperatureOrthotropic(
                    model_qualifiers=[
                        ModelQualifier(name="Definition", value="Secant"),
                        ModelQualifier(name="Behavior", value="Orthotropic"),
                    ],
                    zero_thermal_strain_reference_temperature=Quantity(value=[27.0], units="C"),
                ),
            ],
        )
    ]

    writer = MatmlWriter(materials)
    tree = writer._to_etree()
    material_string, metadata_string = get_material_and_metadata_from_xml(tree)
    with open(CTE_ORTHOTROPIC_VARIABLE, 'r') as file:
        data = file.read()
        assert data == material_string
    with open(CTE_ORTHOTROPIC_METADATA, 'r') as file:
      data = file.read()
      assert data == metadata_string