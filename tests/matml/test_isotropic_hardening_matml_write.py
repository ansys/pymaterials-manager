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

from ansys.materials.manager._models._common import IndependentParameter
from ansys.materials.manager._models._material_models.isotropic_hardening import IsotropicHardening
from ansys.materials.manager._models._material_models.isotropic_hardening_voce_law import (
    IsotropicHardeningVoceLaw,
)
from ansys.materials.manager._models.material import Material
from ansys.materials.manager.parsers.matml.matml_writer import MatmlWriter

DIR_PATH = Path(__file__).resolve().parent

ISOTROPIC_HARDENING_MULTILINEAR = DIR_PATH.joinpath(
    "..", "data", "matml_isotropic_hardening_multilinear.txt"
)
ISOTROPIC_HARDENING_MULTILINEAR_METADATA = DIR_PATH.joinpath(
    "..", "data", "matml_isotropic_hardening_multilinear_metadata.txt"
)
ISOTROPIC_HARDENING_MULTILINEAR_VARIABLE = DIR_PATH.joinpath(
    "..", "data", "matml_isotropic_hardening_multilinear_variable.txt"
)
ISOTROPIC_HARDENING_VOCE = DIR_PATH.joinpath("..", "data", "matml_isotropic_hardening_voce.txt")
ISOTROPIC_HARDENING_VOCE_METADATA = DIR_PATH.joinpath(
    "..", "data", "matml_isotropic_hardening_voce_metadata.txt"
)
ISOTROPIC_HARDENING_VOCE_VARIABLE = DIR_PATH.joinpath(
    "..", "data", "matml_isotropic_hardening_voce_variable.txt"
)


def test_write_constant_multilinear_isotropic_hardening():
    materials = [
        Material(
            name="SFRP",
            models=[
                IsotropicHardening(
                    stress=Quantity(
                        value=[
                            29.52801806,
                            30.93946596,
                            31.56895322,
                            32.83324607,
                            34.28804632,
                            35.45779394,
                            36.7206105,
                            37.86550163,
                            38.9800331,
                            40.37409873,
                            41.70507301,
                            42.87224516,
                            43.84021506,
                            44.94150614,
                            45.83281545,
                            46.81708774,
                            47.66814815,
                            48.32197593,
                            49.03683773,
                            49.69403185,
                            50.38934957,
                            50.9180887,
                            51.42733217,
                            52.07041013,
                            52.53035234,
                            52.99417352,
                            53.42471716,
                            54.00033621,
                            54.36001955,
                            54.71963936,
                            55.13624926,
                        ],
                        units="Pa",
                    ),
                    independent_parameters=[
                        IndependentParameter(
                            name="Plastic Strain",
                            values=Quantity(
                                value=[
                                    0.0,
                                    0.000175189,
                                    0.000257223,
                                    0.00043005,
                                    0.000643825,
                                    0.000828966,
                                    0.00104416,
                                    0.001255108,
                                    0.001477263,
                                    0.00178269,
                                    0.002108789,
                                    0.002428809,
                                    0.002723618,
                                    0.003098638,
                                    0.003439709,
                                    0.003864545,
                                    0.004281943,
                                    0.004640923,
                                    0.00507901,
                                    0.005531357,
                                    0.006070993,
                                    0.006529747,
                                    0.007015966,
                                    0.007698042,
                                    0.008235242,
                                    0.008819543,
                                    0.009399517,
                                    0.010228087,
                                    0.010773853,
                                    0.011338467,
                                    0.01201311,
                                ],
                                units="m m^-1",
                            ),
                        ),
                        IndependentParameter(
                            name="Temperature",
                            values=Quantity(
                                value=[
                                    7.88860905221012e-31,
                                    7.88860905221012e-31,
                                    7.88860905221012e-31,
                                    7.88860905221012e-31,
                                    7.88860905221012e-31,
                                    7.88860905221012e-31,
                                    7.88860905221012e-31,
                                    7.88860905221012e-31,
                                    7.88860905221012e-31,
                                    7.88860905221012e-31,
                                    7.88860905221012e-31,
                                    7.88860905221012e-31,
                                    7.88860905221012e-31,
                                    7.88860905221012e-31,
                                    7.88860905221012e-31,
                                    7.88860905221012e-31,
                                    7.88860905221012e-31,
                                    7.88860905221012e-31,
                                    7.88860905221012e-31,
                                    7.88860905221012e-31,
                                    7.88860905221012e-31,
                                    7.88860905221012e-31,
                                    7.88860905221012e-31,
                                    7.88860905221012e-31,
                                    7.88860905221012e-31,
                                    7.88860905221012e-31,
                                    7.88860905221012e-31,
                                    7.88860905221012e-31,
                                    7.88860905221012e-31,
                                    7.88860905221012e-31,
                                    7.88860905221012e-31,
                                ],
                                units="C",
                            ),
                        ),
                    ],
                ),
            ],
        )
    ]

    writer = MatmlWriter(materials)
    tree = writer._to_etree()
    material_string, metadata_string = get_material_and_metadata_from_xml(tree)
    with open(ISOTROPIC_HARDENING_MULTILINEAR, "r") as file:
        data = file.read()
        assert data == material_string
    with open(ISOTROPIC_HARDENING_MULTILINEAR_METADATA, "r") as file:
        data = file.read()
        assert data == metadata_string


def test_write_variable_mutilinear_isotropic_hardening():
    materials = [
        Material(
            name="SFRP Temp Dependent",
            models=[
                IsotropicHardening(
                    stress=Quantity(
                        value=[
                            29.52801806,
                            30.93946596,
                            31.56895322,
                            32.83324607,
                            34.28804632,
                            35.45779394,
                            36.7206105,
                            37.86550163,
                            38.9800331,
                            40.37409873,
                        ],
                        units="Pa",
                    ),
                    independent_parameters=[
                        IndependentParameter(
                            name="Plastic Strain",
                            values=Quantity(
                                value=[
                                    0.0,
                                    0.000175189,
                                    0.000257223,
                                    0.00043005,
                                    0.000643825,
                                    0.0,
                                    0.00104416,
                                    0.001255108,
                                    0.001477263,
                                    0.00178269,
                                ],
                                units="m m^-1",
                            ),
                        ),
                        IndependentParameter(
                            name="Temperature",
                            values=Quantity(
                                value=[22, 22, 22, 22, 22, 45, 45, 45, 45, 45], units="C"
                            ),
                        ),
                    ],
                ),
            ],
        )
    ]

    writer = MatmlWriter(materials)
    tree = writer._to_etree()
    material_string, metadata_string = get_material_and_metadata_from_xml(tree)
    with open(ISOTROPIC_HARDENING_MULTILINEAR_VARIABLE, "r") as file:
        data = file.read()
        assert data == material_string
    with open(ISOTROPIC_HARDENING_MULTILINEAR_METADATA, "r") as file:
        data = file.read()
        assert data == metadata_string


def test_write_constant_voce_isotropic_hardening():
    materials = [
        Material(
            name="SFRP",
            models=[
                IsotropicHardeningVoceLaw(
                    initial_yield_stress=Quantity(value=[28264641.0], units="Pa"),
                    linear_coefficient=Quantity(value=[526886855.0], units="Pa"),
                    exponential_coefficient=Quantity(value=[18328164.0], units="Pa"),
                    exponential_saturation_parameter=Quantity(value=[406.479025], units=""),
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
    with open(ISOTROPIC_HARDENING_VOCE, "r") as file:
        data = file.read()
        assert data == material_string
    with open(ISOTROPIC_HARDENING_VOCE_METADATA, "r") as file:
        data = file.read()
        assert data == metadata_string


def test_read_variable_voce_isotropic_hardening():
    materials = [
        Material(
            name="SFRP Temp Dependent",
            models=[
                IsotropicHardeningVoceLaw(
                    initial_yield_stress=Quantity(value=[28264641, 34264641, 39264641], units="Pa"),
                    linear_coefficient=Quantity(
                        value=[526886855, 670000000, 870000000], units="Pa"
                    ),
                    exponential_coefficient=Quantity(
                        value=[18328164, 15000000, 15347000], units="Pa"
                    ),
                    exponential_saturation_parameter=Quantity(
                        value=[406.479025, 387, 387], units=""
                    ),
                    independent_parameters=[
                        IndependentParameter(
                            name="Temperature", values=Quantity(value=[22, 112.4, 267], units="C")
                        )
                    ],
                ),
            ],
        )
    ]

    writer = MatmlWriter(materials)
    tree = writer._to_etree()
    material_string, metadata_string = get_material_and_metadata_from_xml(tree)
    with open(ISOTROPIC_HARDENING_VOCE_VARIABLE, "r") as file:
        data = file.read()
        assert data == material_string
    with open(ISOTROPIC_HARDENING_VOCE_METADATA, "r") as file:
        data = file.read()
        assert data == metadata_string
