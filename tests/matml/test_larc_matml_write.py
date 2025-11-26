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

from ansys.materials.manager._models._common import IndependentParameter
from ansys.materials.manager._models._material_models.larc03_04_constants import LaRc0304Constants
from ansys.materials.manager._models.material import Material
from ansys.materials.manager.parsers.matml.matml_writer import MatmlWriter

DIR_PATH = Path(__file__).resolve().parent
LARC = DIR_PATH.joinpath("..", "data", "matml_larc.txt")
LARC_METADATA = DIR_PATH.joinpath("..", "data", "matml_larc_metadata.txt")
LARC_VARIABLE = DIR_PATH.joinpath("..", "data", "matml_larc_variable.txt")


def test_write_constant_larc():
    materials = [
        Material(
            name="material with larc",
            models=[
                LaRc0304Constants(
                    fracture_toughness_ratio=Quantity(value=[1.0], units=""),
                    longitudinal_friction_coefficient=Quantity(value=[2.0], units=""),
                    transverse_friction_coefficient=Quantity(value=[3.0], units=""),
                    fracture_angle_under_compression=Quantity(value=[4.0], units=""),
                    independent_parameters=[
                        IndependentParameter(
                            name="Temperature",
                            values=Quantity(value=[7.88860905221012e-31], units="C"),
                        )
                    ],
                ),
            ],
        )
    ]

    writer = MatmlWriter(materials)
    tree = writer._to_etree()
    material_string, metadata_string = get_material_and_metadata_from_xml(tree)
    with open(LARC, "r") as file:
        data = file.read()
        assert data == material_string
    with open(LARC_METADATA, "r") as file:
        data = file.read()
        assert data == metadata_string


def test_write_variable_larc():
    materials = [
        Material(
            name="material with variable larc",
            models=[
                LaRc0304Constants(
                    fracture_toughness_ratio=Quantity(value=[5.0, 9.0, 13.0], units=""),
                    longitudinal_friction_coefficient=Quantity(value=[6.0, 10.0, 14.0], units=""),
                    transverse_friction_coefficient=Quantity(value=[7.0, 11.0, 15.0], units=""),
                    fracture_angle_under_compression=Quantity(value=[8.0, 12.0, 16.0], units=""),
                    independent_parameters=[
                        IndependentParameter(
                            name="Temperature", values=Quantity(value=[22.0, 50.0, 70.0], units="C")
                        )
                    ],
                ),
            ],
        )
    ]

    writer = MatmlWriter(materials)
    tree = writer._to_etree()
    material_string, metadata_string = get_material_and_metadata_from_xml(tree)
    with open(LARC_VARIABLE, "r") as file:
        data = file.read()
        assert data == material_string
    with open(LARC_METADATA, "r") as file:
        data = file.read()
        assert data == metadata_string
