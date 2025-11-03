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

from ansys.units import Quantity
from utilities import get_material_and_metadata_from_xml

from ansys.materials.manager._models._common import IndependentParameter, ModelQualifier
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
from ansys.materials.manager.util.visitors.matml_visitor import MatmlVisitor

DIR_PATH = Path(__file__).resolve().parent
CTE_ISOTROPIC = DIR_PATH.joinpath("..", "data", "matml_cte_isotropic.txt")
CTE_ISOTROPIC_METADATA = DIR_PATH.joinpath("..", "data", "matml_cte_isotropic_metadata.txt")
CTE_ORTHOTROPIC = DIR_PATH.joinpath("..", "data", "matml_cte_orthotropic.txt")
CTE_ORTHOTROPIC_METADATA = DIR_PATH.joinpath("..", "data", "matml_cte_orthotropic_metadata.txt")
CTE_ISOTROPIC_VARIABLE = DIR_PATH.joinpath("..", "data", "matml_cte_isotropic_variable.txt")
CTE_ORTHOTROPIC_VARIABLE = DIR_PATH.joinpath("..", "data", "matml_cte_orthotropic_variable.txt")


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

    writer = MatmlVisitor(materials)
    tree = writer._to_etree()
    material_string, metadata_string = get_material_and_metadata_from_xml(tree)
    with open(CTE_ISOTROPIC, "r") as file:
        data = file.read()
        assert data == material_string
    with open(CTE_ISOTROPIC_METADATA, "r") as file:
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

    writer = MatmlVisitor(materials)
    tree = writer._to_etree()
    material_string, metadata_string = get_material_and_metadata_from_xml(tree)
    with open(CTE_ORTHOTROPIC, "r") as file:
        data = file.read()
        assert data == material_string
    with open(CTE_ORTHOTROPIC_METADATA, "r") as file:
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

    writer = MatmlVisitor(materials)
    tree = writer._to_etree()
    material_string, metadata_string = get_material_and_metadata_from_xml(tree)
    with open(CTE_ISOTROPIC_VARIABLE, "r") as file:
        data = file.read()
        assert data == material_string
    with open(CTE_ISOTROPIC_METADATA, "r") as file:
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
                    coefficient_of_thermal_expansion_x=Quantity(
                        value=[0.1, 0.2, 0.3], units="C^-1"
                    ),
                    coefficient_of_thermal_expansion_y=Quantity(
                        value=[0.2, 0.15, 0.1], units="C^-1"
                    ),
                    coefficient_of_thermal_expansion_z=Quantity(
                        value=[0.3, 0.2, 0.1], units="C^-1"
                    ),
                    independent_parameters=[
                        IndependentParameter(
                            name="Temperature",
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

    writer = MatmlVisitor(materials)
    tree = writer._to_etree()
    material_string, metadata_string = get_material_and_metadata_from_xml(tree)
    with open(CTE_ORTHOTROPIC_VARIABLE, "r") as file:
        data = file.read()
        assert data == material_string
    with open(CTE_ORTHOTROPIC_METADATA, "r") as file:
        data = file.read()
        assert data == metadata_string
