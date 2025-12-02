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

from ansys.materials.manager._models._common.independent_parameter import IndependentParameter
from ansys.materials.manager._models._material_models.neo_hookean import NeoHookean
from ansys.materials.manager._models.material import Material
from ansys.materials.manager.parsers.matml.matml_writer import MatmlWriter

DIR_PATH = Path(__file__).resolve().parent
NEO_HOOKEAN_CONSTANT = DIR_PATH.joinpath("..", "data", "matml_neo_hookean.xml")


def test_neo_hookean_constant_matml_write():
    neo_hookean = NeoHookean(
        initial_shear_modulus=Quantity(value=[27104.0], units="Pa"),
        incompressibility_modulus=Quantity(value=[1e-05], units="Pa^-1"),
    )
    material = Material(
        name="Neo Hookean constant",
        models=[neo_hookean],
    )

    writer = MatmlWriter(materials=[material])
    tree = writer._to_etree()
    material_string, metadata_string = get_material_and_metadata_from_xml(tree)
    with open(DIR_PATH.joinpath("..", "data", "matml_neo_hookean_constant.txt"), "r") as file:
        data = file.read()
        assert data == material_string
    with open(
        DIR_PATH.joinpath("..", "data", "matml_neo_hookean_constant_metadata.txt"),
        "r",
    ) as file:
        data = file.read()
        assert data == metadata_string


def test_neo_hookean_variable_matml_write():
    neo_hookean = NeoHookean(
        initial_shear_modulus=Quantity(value=[27104.0, 2700.0, 2600.0], units="Pa"),
        incompressibility_modulus=Quantity(value=[1e-05, 2e-05, 3e-05], units="Pa^-1"),
        independent_parameters=[
            IndependentParameter(
                name="Temperature",
                values=Quantity(value=[100, 300, 816], units="C"),
            )
        ],
    )
    material = Material(
        name="Neo Hookean variable",
        models=[neo_hookean],
    )
    writer = MatmlWriter(materials=[material])
    tree = writer._to_etree()
    material_string, metadata_string = get_material_and_metadata_from_xml(tree)
    with open(DIR_PATH.joinpath("..", "data", "matml_neo_hookean_variable.txt"), "r") as file:
        data = file.read()
        assert data == material_string
    with open(
        DIR_PATH.joinpath("..", "data", "matml_neo_hookean_variable_metadata.txt"),
        "r",
    ) as file:
        data = file.read()
        assert data == metadata_string
