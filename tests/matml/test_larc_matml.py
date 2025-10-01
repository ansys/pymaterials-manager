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

from ansys.units import Quantity
from utilities import get_material_and_metadata_from_xml, read_specific_material

from ansys.materials.manager._models._common import IndependentParameter
from ansys.materials.manager._models._material_models.larc03_04_constants import LaRc0304Constants
from ansys.materials.manager._models.material import Material
from ansys.materials.manager.util.matml.matml_from_material import MatmlWriter

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
XML_FILE_PATH = os.path.join(DIR_PATH, "..", "data", "matml_unittest_larc.xml")
LARC = os.path.join(DIR_PATH, "..", "data", "matml_larc.txt")
LARC_METADATA = os.path.join(DIR_PATH, "..", "data", "matml_larc_metadata.txt")
LARC_VARIABLE = os.path.join(DIR_PATH, "..", "data", "matml_larc_variable.txt")


def test_read_constant_larc():
    material = read_specific_material(XML_FILE_PATH, "material with larc")
    assert len(material.models) == 2
    larc = material.models[1]
    assert larc.name == "LaRc03/04 Constants"
    assert larc.fracture_toughness_ratio.value == [1.0]
    assert larc.fracture_toughness_ratio.unit == ""
    assert larc.longitudinal_friction_coefficient.value == [2.0]
    assert larc.longitudinal_friction_coefficient.unit == ""
    assert larc.transverse_friction_coefficient.value == [3.0]
    assert larc.transverse_friction_coefficient.unit == ""
    assert larc.fracture_angle_under_compression.value == [4.0]
    assert larc.fracture_angle_under_compression.unit == ""
    assert larc.independent_parameters[0].name == "Temperature"
    assert larc.independent_parameters[0].values.value == [7.88860905221012e-31]
    assert larc.independent_parameters[0].values.unit == "C"


def test_read_variable_larc():
    material = read_specific_material(XML_FILE_PATH, "material with variable larc")
    assert len(material.models) == 2
    larc = material.models[1]
    assert larc.name == "LaRc03/04 Constants"
    assert larc.fracture_toughness_ratio.value.tolist() == [5.0, 9.0, 13.0]
    assert larc.fracture_toughness_ratio.unit == ""
    assert larc.longitudinal_friction_coefficient.value.tolist() == [6.0, 10.0, 14.0]
    assert larc.longitudinal_friction_coefficient.unit == ""
    assert larc.transverse_friction_coefficient.value.tolist() == [7.0, 11.0, 15.0]
    assert larc.transverse_friction_coefficient.unit == ""
    assert larc.fracture_angle_under_compression.value.tolist() == [8.0, 12.0, 16.0]
    assert larc.fracture_angle_under_compression.unit == ""
    assert larc.independent_parameters[0].name == "Temperature"
    assert larc.independent_parameters[0].values.value.tolist() == [22.0, 50.0, 70.0]
    assert larc.independent_parameters[0].values.unit == "C"


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
