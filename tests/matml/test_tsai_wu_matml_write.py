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
from ansys.materials.manager._models._material_models.tsai_wu_constants import TsaiWuConstants
from ansys.materials.manager._models.material import Material
from ansys.materials.manager.util.visitors.matml_visitor import MatmlWriter

DIR_PATH = Path(__file__).resolve().parent
TSAI_WU = DIR_PATH.joinpath("..", "data", "matml_tsai_wu.txt")
TSAI_WU_METADATA = DIR_PATH.joinpath("..", "data", "matml_tsai_wu_metadata.txt")
TSAI_WU_VARIABLE = DIR_PATH.joinpath("..", "data", "matml_tsai_wu_variable.txt")


def test_write_constant_tsai_wu():
    materials = [
        Material(
            name="material with tsai-wu",
            models=[
                TsaiWuConstants(
                    coupling_coefficient_xy=Quantity(value=[-1.0], unit=""),
                    coupling_coefficient_xz=Quantity(value=[-1.0], unit=""),
                    coupling_coefficient_yz=Quantity(value=[-1.0], unit=""),
                    independent_parameters=[
                        IndependentParameter(
                            name="Temperature",
                            values=Quantity(value=[7.88860905221012e-31], unit="C"),
                        ),
                    ],
                ),
            ],
        )
    ]

    writer = MatmlWriter(materials)
    tree = writer._to_etree()
    material_string, metadata_string = get_material_and_metadata_from_xml(tree)
    with open(TSAI_WU, "r") as file:
        data = file.read()
        assert data == material_string
    with open(TSAI_WU_METADATA, "r") as file:
        data = file.read()
        assert data == metadata_string


def test_write_variable_tsai_wu():
    materials = [
        Material(
            name="material with variable tsai-wu",
            models=[
                TsaiWuConstants(
                    coupling_coefficient_xy=Quantity(value=[-1.0, -1.0, -1.0], unit=""),
                    coupling_coefficient_xz=Quantity(value=[-1.0, -1.0, -1.0], unit=""),
                    coupling_coefficient_yz=Quantity(value=[-1.0, -1.0, -1.0], unit=""),
                    independent_parameters=[
                        IndependentParameter(
                            name="Temperature",
                            values=Quantity(value=[22.0, 50.0, 70.0], unit="C"),
                        ),
                    ],
                ),
            ],
        )
    ]

    writer = MatmlWriter(materials)
    tree = writer._to_etree()
    material_string, metadata_string = get_material_and_metadata_from_xml(tree)
    with open(TSAI_WU_VARIABLE, "r") as file:
        data = file.read()
        assert data == material_string
    with open(TSAI_WU_METADATA, "r") as file:
        data = file.read()
        assert data == metadata_string
