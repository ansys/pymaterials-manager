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
from ansys.materials.manager._models._material_models.specific_heat import SpecificHeat
from ansys.materials.manager._models.material import Material
from ansys.materials.manager.util.visitors.matml_visitor import MatmlWriter

DIR_PATH = Path(__file__).resolve().parent
SPECIFIC_HEAT_VOLUME = DIR_PATH.joinpath("..", "data", "matml_specific_heat_volume.txt")
SPECIFIC_HEAT_METADATA = DIR_PATH.joinpath("..", "data", "matml_specific_heat_volume_metadata.txt")
SPECIFIC_HEAT_VOLUME_VARIABLE = DIR_PATH.joinpath(
    "..", "data", "matml_specific_heat_volume_variable.txt"
)
SPECIFIC_HEAT_PRESSURE = DIR_PATH.joinpath("..", "data", "matml_specific_heat_pressure.txt")
SPECIFIC_HEAT_PRESSURE_VARIABLE = DIR_PATH.joinpath(
    "..", "data", "matml_specific_heat_pressure_variable.txt"
)


def test_write_constant_specific_heat_volume():
    materials = [
        Material(
            name="material with specific heat volume",
            models=[
                SpecificHeat(
                    model_qualifiers=[
                        ModelQualifier(name="Definition", value="Constant Volume"),
                        ModelQualifier(name="Field Variable Compatible", value="Temperature"),
                        ModelQualifier(name="Symbol", value="Cᵥ"),
                    ],
                    specific_heat=Quantity(value=[2.0], units="J kg^-1 C^-1"),
                    independent_parameters=[
                        IndependentParameter(
                            name="Temperature",
                            values=Quantity(value=[22.0], units="C"),
                            default_value=22.0,
                            upper_limit="Program Controlled",
                            lower_limit="Program Controlled",
                        ),
                    ],
                ),
            ],
        )
    ]

    writer = MatmlWriter(materials)
    tree = writer._to_etree()
    material_string, metadata_string = get_material_and_metadata_from_xml(tree)
    with open(SPECIFIC_HEAT_VOLUME, "r", encoding="utf8") as file:
        data = file.read()
        assert data == material_string
    with open(SPECIFIC_HEAT_METADATA, "r") as file:
        data = file.read()
        assert data == metadata_string


def test_write_variable_specific_heat_volume():
    materials = [
        Material(
            name="material with variable specific heat volume",
            models=[
                SpecificHeat(
                    model_qualifiers=[
                        ModelQualifier(name="Definition", value="Constant Volume"),
                        ModelQualifier(name="Field Variable Compatible", value="Temperature"),
                        ModelQualifier(name="Symbol", value="Cᵥ"),
                    ],
                    specific_heat=Quantity(value=[10.0, 20.0, 30.0], units="J kg^-1 C^-1"),
                    independent_parameters=[
                        IndependentParameter(
                            name="Temperature",
                            values=Quantity(value=[22.0, 40.0, 60.0], units="C"),
                            default_value=22.0,
                            upper_limit="Program Controlled",
                            lower_limit="Program Controlled",
                        ),
                    ],
                ),
            ],
        )
    ]

    writer = MatmlWriter(materials)
    tree = writer._to_etree()
    material_string, metadata_string = get_material_and_metadata_from_xml(tree)
    with open(SPECIFIC_HEAT_VOLUME_VARIABLE, "r", encoding="utf8") as file:
        data = file.read()
        assert data == material_string
    with open(SPECIFIC_HEAT_METADATA, "r") as file:
        data = file.read()
        assert data == metadata_string


def test_write_constant_specific_heat_pressure():
    materials = [
        Material(
            name="material with specific heat pressure",
            models=[
                SpecificHeat(
                    model_qualifiers=[
                        ModelQualifier(name="Definition", value="Constant Pressure"),
                        ModelQualifier(name="Field Variable Compatible", value="Temperature"),
                        ModelQualifier(name="Symbol", value="Cᵨ"),
                    ],
                    specific_heat=Quantity(value=[1.0], units="J kg^-1 C^-1"),
                    independent_parameters=[
                        IndependentParameter(
                            name="Temperature",
                            values=Quantity(value=[22.0], units="C"),
                            default_value=22.0,
                            upper_limit="Program Controlled",
                            lower_limit="Program Controlled",
                        ),
                    ],
                ),
            ],
        )
    ]

    writer = MatmlWriter(materials)
    tree = writer._to_etree()
    material_string, metadata_string = get_material_and_metadata_from_xml(tree)
    with open(SPECIFIC_HEAT_PRESSURE, "r", encoding="utf8") as file:
        data = file.read()
        assert data == material_string
    with open(SPECIFIC_HEAT_METADATA, "r") as file:
        data = file.read()
        assert data == metadata_string


def test_write_variable_specific_heat_pressure():
    materials = [
        Material(
            name="material with variable specific heat pressure",
            models=[
                SpecificHeat(
                    model_qualifiers=[
                        ModelQualifier(name="Definition", value="Constant Pressure"),
                        ModelQualifier(name="Field Variable Compatible", value="Temperature"),
                        ModelQualifier(name="Symbol", value="Cᵨ"),
                    ],
                    specific_heat=Quantity(value=[1.0, 2.0, 3.0], units="J kg^-1 C^-1"),
                    independent_parameters=[
                        IndependentParameter(
                            name="Temperature",
                            values=Quantity(value=[22.0, 40.0, 60.0], units="C"),
                            default_value=22.0,
                            upper_limit="Program Controlled",
                            lower_limit="Program Controlled",
                        ),
                    ],
                ),
            ],
        )
    ]

    writer = MatmlWriter(materials)
    tree = writer._to_etree()
    material_string, metadata_string = get_material_and_metadata_from_xml(tree)
    with open(SPECIFIC_HEAT_PRESSURE_VARIABLE, "r", encoding="utf8") as file:
        data = file.read()
        assert data == material_string
    with open(SPECIFIC_HEAT_METADATA, "r") as file:
        data = file.read()
        assert data == metadata_string
