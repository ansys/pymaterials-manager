# Copyright (C) 2022 - 2026 ANSYS, Inc. and/or its affiliates.
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

from ansys.materials.manager._models._common import (
    IndependentParameter,
    InterpolationOptions,
    ModelQualifier,
)
from ansys.materials.manager._models._material_models.hill_yield_criterion import HillYieldCriterion
from ansys.materials.manager._models._material_models.kinematic_hardening import KinematicHardening
from ansys.materials.manager._models._material_models.strain_hardening import StrainHardening
from ansys.materials.manager._models.material import Material
from ansys.materials.manager.parsers.matml.matml_writer import MatmlWriter

DIR_PATH = Path(__file__).resolve().parent
HILL_YIELD = DIR_PATH.joinpath("..", "data", "matml_hill_yield.txt")
HILL_YIELD_METADATA = DIR_PATH.joinpath("..", "data", "matml_hill_yield_metadata.txt")
HILL_YIELD_VARIABLE = DIR_PATH.joinpath("..", "data", "matml_hill_yield_variable.txt")
HILL_YIELD_CREEP = DIR_PATH.joinpath("..", "data", "matml_hill_yield_creep.txt")
HILL_YIELD_CREEP_METADATA = DIR_PATH.joinpath("..", "data", "matml_hill_yield_creep_metadata.txt")
KINEMATIC_HARDENING = DIR_PATH.joinpath("..", "data", "matml_kinematic_harderning.txt")
KINEMATIC_HARDENING_METADATA = DIR_PATH.joinpath(
    "..", "data", "matml_kinematic_harderning_metadata.txt"
)
STRAIN_HARDENING = DIR_PATH.joinpath("..", "data", "matml_strain_hardening.txt")
STRAIN_HARDENING_METADATA = DIR_PATH.joinpath("..", "data", "matml_strain_hardening_metadata.txt")


def test_write_constant_hill_yield_no_creep():
    materials = [
        Material(
            name="SFRP",
            models=[
                HillYieldCriterion(
                    yield_stress_ratio_x=Quantity(value=[1.2], units=""),
                    yield_stress_ratio_xy=Quantity(value=[0.12], units=""),
                    yield_stress_ratio_xz=Quantity(value=[0.23], units=""),
                    yield_stress_ratio_y=Quantity(value=[0.8], units=""),
                    yield_stress_ratio_yz=Quantity(value=[0.23], units=""),
                    yield_stress_ratio_z=Quantity(value=[0.5], units=""),
                    independent_parameters=[
                        IndependentParameter(
                            name="Temperature",
                            values=Quantity(value=[7.88860905221012e-31], units="C"),
                            default_value=22.0,
                            upper_limit="Program Controlled",
                            lower_limit="Program Controlled",
                        ),
                    ],
                    interpolation_options=InterpolationOptions(
                        algorithm_type="Linear Multivariate",
                        cached=True,
                        normalized=True,
                    ),
                ),
            ],
        )
    ]

    writer = MatmlWriter(materials)
    tree = writer._to_etree()
    material_string, metadata_string = get_material_and_metadata_from_xml(tree)
    with open(HILL_YIELD, "r") as file:
        data = file.read()
        assert data == material_string
    with open(HILL_YIELD_METADATA, "r") as file:
        data = file.read()
        assert data == metadata_string


def test_write_variable_hill_yield_no_creep():
    materials = [
        Material(
            name="SFRP Temp Dependent",
            models=[
                HillYieldCriterion(
                    yield_stress_ratio_x=Quantity(value=[1.2, 1.2, 1.4], units=""),
                    yield_stress_ratio_xy=Quantity(value=[0.12, 0.12, 0.12], units=""),
                    yield_stress_ratio_xz=Quantity(value=[0.23, 0.23, 0.23], units=""),
                    yield_stress_ratio_y=Quantity(value=[0.8, 0.8, 0.7], units=""),
                    yield_stress_ratio_yz=Quantity(value=[0.23, 0.23, 0.23], units=""),
                    yield_stress_ratio_z=Quantity(value=[0.5, 0.5, 0.4], units=""),
                    independent_parameters=[
                        IndependentParameter(
                            name="Temperature",
                            values=Quantity(value=[34.0, 78.0, 245.0], units="C"),
                            default_value=22.0,
                            upper_limit="Program Controlled",
                            lower_limit="Program Controlled",
                        ),
                    ],
                    interpolation_options=InterpolationOptions(
                        algorithm_type="Linear Multivariate",
                        cached=True,
                        normalized=True,
                    ),
                ),
            ],
        )
    ]
    writer = MatmlWriter(materials)
    tree = writer._to_etree()
    material_string, metadata_string = get_material_and_metadata_from_xml(tree)
    with open(HILL_YIELD_VARIABLE, "r") as file:
        data = file.read()
        assert data == material_string
    with open(HILL_YIELD_METADATA, "r") as file:
        data = file.read()
        assert data == metadata_string


def test_write_constant_hill_yield_creep():
    materials = [
        Material(
            name="SFRP",
            models=[
                HillYieldCriterion(
                    yield_stress_ratio_x=Quantity(value=[1.0], units=""),
                    yield_stress_ratio_y=Quantity(value=[1.0], units=""),
                    yield_stress_ratio_z=Quantity(value=[1.0], units=""),
                    yield_stress_ratio_xy=Quantity(value=[1.0], units=""),
                    yield_stress_ratio_yz=Quantity(value=[1.0], units=""),
                    yield_stress_ratio_xz=Quantity(value=[1.0], units=""),
                    creep_stress_ratio_x=Quantity(value=[2.0], units=""),
                    creep_stress_ratio_y=Quantity(value=[2.0], units=""),
                    creep_stress_ratio_z=Quantity(value=[2.0], units=""),
                    creep_stress_ratio_xy=Quantity(value=[2.0], units=""),
                    creep_stress_ratio_yz=Quantity(value=[2.0], units=""),
                    creep_stress_ratio_xz=Quantity(value=[2.0], units=""),
                    independent_parameters=[
                        IndependentParameter(
                            name="Temperature",
                            values=Quantity(value=[7.88860905221012e-31], units="C"),
                            default_value=22.0,
                            upper_limit="Program Controlled",
                            lower_limit="Program Controlled",
                        ),
                    ],
                    interpolation_options=InterpolationOptions(
                        algorithm_type="Linear Multivariate",
                        cached=True,
                        normalized=True,
                    ),
                    model_qualifiers=[
                        ModelQualifier(
                            name="Separated Hill Potentials for Plasticity and Creep", value="Yes"
                        )
                    ],
                ),
            ],
        )
    ]

    writer = MatmlWriter(materials)
    tree = writer._to_etree()
    material_string, metadata_string = get_material_and_metadata_from_xml(tree)
    with open(HILL_YIELD_CREEP, "r") as file:
        data = file.read()
        assert data == material_string
    with open(HILL_YIELD_CREEP_METADATA, "r") as file:
        data = file.read()
        assert data == metadata_string


def test_write_kinematic_hardening():
    materials = [
        Material(
            name="SFRP",
            models=[
                KinematicHardening(
                    yield_stress=Quantity(value=[12.0], units="Pa"),
                    material_constant_gamma_1=Quantity(value=[1.0], units=""),
                    material_constant_c_1=Quantity(value=[45.0], units="Pa"),
                    independent_parameters=[
                        IndependentParameter(
                            name="Temperature",
                            values=Quantity(value=[7.88860905221012e-31], units="C"),
                        ),
                    ],
                ),
            ],
        )
    ]

    writer = MatmlWriter(materials)
    tree = writer._to_etree()
    material_string, metadata_string = get_material_and_metadata_from_xml(tree)
    with open(KINEMATIC_HARDENING, "r") as file:
        data = file.read()
        assert data == material_string
    with open(KINEMATIC_HARDENING_METADATA, "r", encoding="utf-8") as file:
        data = file.read()
        assert data == metadata_string


def test_write_strain_hardening():
    materials = [
        Material(
            name="SFRP",
            models=[
                StrainHardening(
                    creep_constant_1=Quantity(value=[1.0], units=""),
                    creep_constant_2=Quantity(value=[2.0], units=""),
                    creep_constant_3=Quantity(value=[3.0], units=""),
                    creep_constant_4=Quantity(value=[4.0], units=""),
                    independent_parameters=[
                        IndependentParameter(
                            name="Temperature",
                            values=Quantity(value=[7.88860905221012e-31], units="C"),
                        ),
                    ],
                    model_qualifiers=[
                        ModelQualifier(
                            name="Reference Units (Length, Time, Temperature, Force)",
                            value="m, s, K, N",
                        )
                    ],
                ),
            ],
        )
    ]

    writer = MatmlWriter(materials)
    tree = writer._to_etree()
    material_string, metadata_string = get_material_and_metadata_from_xml(tree)
    with open(STRAIN_HARDENING, "r") as file:
        data = file.read()
        assert data == material_string
    with open(STRAIN_HARDENING_METADATA, "r") as file:
        data = file.read()
        assert data == metadata_string
