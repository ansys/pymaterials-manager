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
from ansys.materials.manager._models._material_models.strain_limits_isotropic import (
    StrainLimitsIsotropic,
)
from ansys.materials.manager._models._material_models.strain_limits_orthotropic import (
    StrainLimitsOrthotropic,
)
from ansys.materials.manager._models.material import Material
from ansys.materials.manager.util.visitors.matml_visitor import MatmlWriter

DIR_PATH = Path(__file__).resolve().parent
STRAIN_LIMITS_ORTHOTROPIC = DIR_PATH.joinpath("..", "data", "matml_strain_limits_orthotropic.txt")
STRAIN_LIMITS_ORTHOTROPIC_METADATA = DIR_PATH.joinpath(
    "..", "data", "matml_strain_limits_orthotropic_metadata.txt"
)
STRAIN_LIMITS_ISOTROPIC = DIR_PATH.joinpath("..", "data", "matml_strain_limits_isotropic.txt")
STRAIN_LIMITS_ISOTROPIC_METADATA = DIR_PATH.joinpath(
    "..", "data", "matml_strain_limits_isotropic_metadata.txt"
)
STRAIN_LIMITS_ISOTROPIC_VARIABLE = DIR_PATH.joinpath(
    "..", "data", "matml_strain_limits_isotropic_variable.txt"
)
STRAIN_LIMITS_ORTHOTROPIC_VARIABLE = DIR_PATH.joinpath(
    "..", "data", "matml_strain_limits_orthotropic_variable.txt"
)


def test_write_constant_strain_limits_orthotropic():
    materials = [
        Material(
            name="orthotropic material with strain limit",
            models=[
                StrainLimitsOrthotropic(
                    compressive_x_direction=Quantity(value=[-132.0], units=""),
                    compressive_y_direction=Quantity(value=[-13.0], units=""),
                    compressive_z_direction=Quantity(value=[-13.0], units=""),
                    tensile_x_direction=Quantity(value=[311.0], units=""),
                    tensile_y_direction=Quantity(value=[213.0], units=""),
                    tensile_z_direction=Quantity(value=[13.0], units=""),
                    shear_xy=Quantity(value=[24.0], units=""),
                    shear_xz=Quantity(value=[12.0], units=""),
                    shear_yz=Quantity(value=[232.0], units=""),
                    independent_parameters=[
                        IndependentParameter(
                            name="Temperature",
                            values=Quantity(value=[7.88860905221012e-31], units="C"),
                            upper_limit="Program Controlled",
                            lower_limit="Program Controlled",
                            default_value=22.0,
                        )
                    ],
                ),
            ],
        )
    ]

    writer = MatmlWriter(materials)
    tree = writer._to_etree()
    material_string, metadata_string = get_material_and_metadata_from_xml(tree)
    with open(STRAIN_LIMITS_ORTHOTROPIC, "r", encoding="utf8") as file:
        data = file.read()
        assert data == material_string
    with open(STRAIN_LIMITS_ORTHOTROPIC_METADATA, "r") as file:
        data = file.read()
        assert data == metadata_string


def test_write_constant_strain_limits_isotropic():
    materials = [
        Material(
            name="isotropic material with strain limit",
            models=[
                StrainLimitsIsotropic(
                    von_mises=Quantity(value=[213], units=""),
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
    with open(STRAIN_LIMITS_ISOTROPIC, "r", encoding="utf8") as file:
        data = file.read()
        assert data == material_string
    with open(STRAIN_LIMITS_ISOTROPIC_METADATA, "r") as file:
        data = file.read()
        assert data == metadata_string


def test_write_variable_strain_limits_isotropic():
    materials = [
        Material(
            name="isotropic material with variable strain limit",
            models=[
                StrainLimitsIsotropic(
                    von_mises=Quantity(value=[2333, 2324, 2432], units=""),
                    independent_parameters=[
                        IndependentParameter(
                            name="Temperature", values=Quantity(value=[23, 25, 27], units="C")
                        )
                    ],
                ),
            ],
        )
    ]
    writer = MatmlWriter(materials)
    tree = writer._to_etree()
    material_string, metadata_string = get_material_and_metadata_from_xml(tree)
    with open(STRAIN_LIMITS_ISOTROPIC_VARIABLE, "r", encoding="utf8") as file:
        data = file.read()
        assert data == material_string
    with open(STRAIN_LIMITS_ISOTROPIC_METADATA, "r") as file:
        data = file.read()
        assert data == metadata_string


def test_write_variable_strain_limits_orthotropic():
    materials = [
        Material(
            name="orthotropic material with variable strain limit",
            models=[
                StrainLimitsOrthotropic(
                    tensile_x_direction=Quantity(value=[324.0, 311.0, 312.0], units=""),
                    tensile_y_direction=Quantity(value=[236.0, 213.0, 234.0], units=""),
                    tensile_z_direction=Quantity(value=[15.0, 13.0, 14.0], units=""),
                    compressive_x_direction=Quantity(value=[-110.0, -132.0, -120.0], units=""),
                    compressive_y_direction=Quantity(value=[-11.0, -13.0, -12.0], units=""),
                    compressive_z_direction=Quantity(value=[-9.0, -13.0, -11.0], units=""),
                    shear_xy=Quantity(value=[26.0, 24.0, 25.0], units=""),
                    shear_xz=Quantity(value=[16.0, 12.0, 14.0], units=""),
                    shear_yz=Quantity(value=[255.0, 232.0, 244.0], units=""),
                    independent_parameters=[
                        IndependentParameter(
                            name="Temperature",
                            values=Quantity(value=[13.0, 21.0, 23.0], units="C"),
                            upper_limit="Program Controlled",
                            lower_limit="Program Controlled",
                            default_value=22.0,
                        )
                    ],
                ),
            ],
        )
    ]

    writer = MatmlWriter(materials)
    tree = writer._to_etree()
    material_string, metadata_string = get_material_and_metadata_from_xml(tree)
    with open(STRAIN_LIMITS_ORTHOTROPIC_VARIABLE, "r", encoding="utf8") as file:
        data = file.read()
        assert data == material_string
    with open(STRAIN_LIMITS_ORTHOTROPIC_METADATA, "r") as file:
        data = file.read()
        assert data == metadata_string
