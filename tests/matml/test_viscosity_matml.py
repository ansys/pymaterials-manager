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
from utilities import get_material_and_metadata_from_xml, read_specific_material

from ansys.materials.manager._models._common import IndependentParameter
from ansys.materials.manager._models._material_models.viscosity import Viscosity
from ansys.materials.manager._models.material import Material
from ansys.materials.manager.util.matml.writer_matml import WriterMatml

DIR_PATH = Path(__file__).resolve().parent
XML_FILE_PATH = DIR_PATH.joinpath("..", "data", "matml_unittest_viscosity.xml")
VISCOSITY = DIR_PATH.joinpath("..", "data", "matml_viscosity.txt")
VISCOSITY_METADATA = DIR_PATH.joinpath("..", "data", "matml_viscosity_metadata.txt")
VISCOSITY_VARIABLE = DIR_PATH.joinpath("..", "data", "matml_viscosity_variable.txt")


def test_read_constant_viscosity():
    material = read_specific_material(XML_FILE_PATH, "material with viscosity")
    assert len(material.models) == 2
    viscosity = material.models[1]
    assert viscosity.name == "Viscosity"
    assert viscosity.model_qualifiers[0].name == "BETA"
    assert viscosity.model_qualifiers[0].value == "Mechanical.ModalAcoustics"
    assert viscosity.model_qualifiers[1].name == "Field Variable Compatible"
    assert viscosity.model_qualifiers[1].value == "Temperature"
    assert viscosity.viscosity.value == [1.0]
    assert viscosity.viscosity.unit == "Pa s"
    assert viscosity.independent_parameters[0].name == "Temperature"
    assert viscosity.independent_parameters[0].values.value == [7.88860905221012e-31]
    assert viscosity.independent_parameters[0].values.unit == "C"
    assert viscosity.independent_parameters[0].upper_limit == "Program Controlled"
    assert viscosity.independent_parameters[0].lower_limit == "Program Controlled"
    assert viscosity.independent_parameters[0].default_value == 22.0


def test_read_variable_viscosity():
    material = read_specific_material(XML_FILE_PATH, "material with variable viscosity")
    assert len(material.models) == 2
    viscosity = material.models[1]
    assert viscosity.name == "Viscosity"
    assert viscosity.model_qualifiers[0].name == "BETA"
    assert viscosity.model_qualifiers[0].value == "Mechanical.ModalAcoustics"
    assert viscosity.model_qualifiers[1].name == "Field Variable Compatible"
    assert viscosity.model_qualifiers[1].value == "Temperature"
    assert viscosity.viscosity.value.tolist() == [2.0, 3.0, 4.0]
    assert viscosity.viscosity.unit == "Pa s"
    assert viscosity.independent_parameters[0].name == "Temperature"
    assert viscosity.independent_parameters[0].values.value.tolist() == [22.0, 50.0, 70.0]
    assert viscosity.independent_parameters[0].values.unit == "C"
    assert viscosity.independent_parameters[0].upper_limit == "Program Controlled"
    assert viscosity.independent_parameters[0].lower_limit == "Program Controlled"
    assert viscosity.independent_parameters[0].default_value == 22.0


def test_write_constant_viscosity():
    materials = [
        Material(
            name="material with viscosity",
            models=[
                Viscosity(
                    viscosity=Quantity(value=[1.0], units="Pa s"),
                    independent_parameters=[
                        IndependentParameter(
                            name="Temperature",
                            values=Quantity(value=[22.0], units="C"),
                        ),
                    ],
                ),
            ],
        )
    ]

    writer = WriterMatml(materials)
    tree = writer._to_etree()
    material_string, metadata_string = get_material_and_metadata_from_xml(tree)
    with open(VISCOSITY, "r") as file:
        data = file.read()
        assert data == material_string
    with open(VISCOSITY_METADATA, "r") as file:
        data = file.read()
        assert data == metadata_string


def test_write_variable_viscosity():
    materials = [
        Material(
            name="material with variable viscosity",
            models=[
                Viscosity(
                    viscosity=Quantity(value=[2.0, 3.0, 4.0], units="Pa s"),
                    independent_parameters=[
                        IndependentParameter(
                            name="Temperature",
                            values=Quantity(value=[22.0, 50.0, 70.0], units="C"),
                        ),
                    ],
                ),
            ],
        )
    ]

    writer = WriterMatml(materials)
    tree = writer._to_etree()
    material_string, metadata_string = get_material_and_metadata_from_xml(tree)
    with open(VISCOSITY_VARIABLE, "r") as file:
        data = file.read()
        assert data == material_string
    with open(VISCOSITY_METADATA, "r") as file:
        data = file.read()
        assert data == metadata_string
