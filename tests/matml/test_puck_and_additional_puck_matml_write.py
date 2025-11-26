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
from ansys.materials.manager._models._material_models.fiber_angle import FiberAngle
from ansys.materials.manager._models._material_models.puck_constants import PuckConstants
from ansys.materials.manager._models._material_models.puck_constants_additional import (
    AdditionalPuckConstants,
)
from ansys.materials.manager._models._material_models.stress_limits_orthotropic import (
    StressLimitsOrthotropic,
)
from ansys.materials.manager._models.material import Material
from ansys.materials.manager.parsers.matml.matml_writer import MatmlWriter

DIR_PATH = Path(__file__).resolve().parent
FIBER_ANGLE = DIR_PATH.joinpath("..", "data", "matml_fiber_angle.txt")
FIBER_ANGLE_METADATA = DIR_PATH.joinpath("..", "data", "matml_fiber_angle_metadata.txt")
PUCK = DIR_PATH.joinpath("..", "data", "matml_puck.txt")
PUCK_METADATA = DIR_PATH.joinpath("..", "data", "matml_puck_metadata.txt")
PUCK_ADDITIONAL = DIR_PATH.joinpath("..", "data", "matml_puck_additional.txt")
PUCK_ADDITIONAL_METADATA = DIR_PATH.joinpath("..", "data", "matml_puck_additional_metadata.txt")
STRESS_LIMITS_ORTHOTROPIC = DIR_PATH.joinpath("..", "data", "matml_stress_limits_orthotropic.txt")
STRESS_LIMITS_ORTHOTROPIC_METADATA = DIR_PATH.joinpath(
    "..", "data", "matml_stress_limits_orthotropic_metadata.txt"
)


def test_write_fiber_angle():
    materials = [
        Material(
            name="material with puck for woven",
            models=[
                FiberAngle(
                    model_qualifiers=[
                        ModelQualifier(name="Data Set", values=["1"]),
                        ModelQualifier(
                            name="Data Set Information",
                            values=["minOccurrences::2$$maxOccurrences::2$$Name::Unidirectional"],
                        ),
                    ],
                    material_property="Woven Specification for Puck",
                    independent_parameters=[
                        IndependentParameter(
                            name="Fiber Angle", values=Quantity(value=[45.0], units="")
                        )
                    ],
                ),
            ],
        )
    ]
    writer = MatmlWriter(materials)
    tree = writer._to_etree()
    material_string, metadata_string = get_material_and_metadata_from_xml(tree)
    with open(FIBER_ANGLE, "r") as file:
        data = file.read()
        assert data == material_string
    with open(FIBER_ANGLE_METADATA, "r") as file:
        data = file.read()
        assert data == metadata_string


def test_write_puck_constants():
    materials = [
        Material(
            name="material with puck for woven",
            models=[
                PuckConstants(
                    compressive_inclination_xz=Quantity(value=[0.0], units=""),
                    compressive_inclination_yz=Quantity([0.0], units=""),
                    tensile_inclination_xz=Quantity([0.0], units=""),
                    tensile_inclination_yz=Quantity([0.0], units=""),
                    model_qualifiers=[
                        ModelQualifier(name="Data Set", values=["2"]),
                        ModelQualifier(
                            name="Data Set Information",
                            values=["minOccurrences::2$$maxOccurrences::2$$Name::Unidirectional"],
                        ),
                    ],
                    material_property="Woven Specification for Puck",
                ),
            ],
        )
    ]

    writer = MatmlWriter(materials)
    tree = writer._to_etree()
    material_string, metadata_string = get_material_and_metadata_from_xml(tree)
    with open(PUCK, "r") as file:
        data = file.read()
        assert data == material_string
    with open(PUCK_METADATA, "r") as file:
        data = file.read()
        assert data == metadata_string


def test_write_puck_additional_constants():
    materials = [
        Material(
            name="material with puck for woven",
            models=[
                AdditionalPuckConstants(
                    degradation_parameter_s=Quantity(value=[0.5], units=""),
                    degradation_parameter_m=Quantity(value=[0.5], units=""),
                    interface_weakening_factor=Quantity(value=[0.8], units=""),
                    model_qualifiers=[
                        ModelQualifier(name="Data Set", values=["2"]),
                        ModelQualifier(
                            name="Data Set Information",
                            values=["minOccurrences::2$$maxOccurrences::2$$Name::Unidirectional"],
                        ),
                    ],
                    material_property="Woven Specification for Puck",
                ),
            ],
        )
    ]

    writer = MatmlWriter(materials)
    tree = writer._to_etree()
    material_string, metadata_string = get_material_and_metadata_from_xml(tree)
    with open(PUCK_ADDITIONAL, "r") as file:
        data = file.read()
        assert data == material_string
    with open(PUCK_ADDITIONAL_METADATA, "r") as file:
        data = file.read()
        assert data == metadata_string


def test_write_stress_limits():
    materials = [
        Material(
            name="material with stress_limits",
            models=[
                StressLimitsOrthotropic(
                    compressive_x_direction=Quantity(value=[-100.0], units="Pa"),
                    compressive_y_direction=Quantity(value=[-101.0], units="Pa"),
                    compressive_z_direction=Quantity(value=[-102.0], units="Pa"),
                    tensile_x_direction=Quantity(value=[100.0], units="Pa"),
                    tensile_y_direction=Quantity(value=[101.0], units="Pa"),
                    tensile_z_direction=Quantity(value=[102.0], units="Pa"),
                    shear_xy=Quantity(value=[10.0], units="Pa"),
                    shear_xz=Quantity(value=[14.0], units="Pa"),
                    shear_yz=Quantity(value=[12.0], units="Pa"),
                ),
            ],
        )
    ]

    writer = MatmlWriter(materials)
    tree = writer._to_etree()
    material_string, metadata_string = get_material_and_metadata_from_xml(tree)
    with open(STRESS_LIMITS_ORTHOTROPIC, "r") as file:
        data = file.read()
        assert data == material_string
    with open(STRESS_LIMITS_ORTHOTROPIC_METADATA, "r") as file:
        data = file.read()
        assert data == metadata_string
