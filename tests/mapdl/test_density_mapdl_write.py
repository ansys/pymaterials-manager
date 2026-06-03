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

from ansys.materials.manager._models._common.independent_parameter import IndependentParameter
from ansys.materials.manager._models._common.interpolation_options import InterpolationOptions
from ansys.materials.manager._models._material_models.density import Density
from ansys.materials.manager._models.material import Material
from ansys.materials.manager.parsers.mapdl.mapdl_writer import MapdlWriter

DIR_PATH = Path(__file__).resolve().parent
CONSTANT_DENSITY = DIR_PATH.joinpath("..", "data", "mapdl_density_constant.cdb")
VARIABLE_DENSITY_TEMP_1 = DIR_PATH.joinpath("..", "data", "mapdl_density_variable_1.cdb")
VARIABLE_DENSITY_TEMP_2 = DIR_PATH.joinpath("..", "data", "mapdl_density_variable_2.cdb")
VARIABLE_DENSITY_A11_A22 = DIR_PATH.joinpath("..", "data", "mapdl_density_a11_a22.cdb")
VARIABLE_DENSITY_TEMP_A11_A22 = DIR_PATH.joinpath("..", "data", "mapdl_density_a11_a22_temp.cdb")
VARIABLE_DENSITY_TEMP_A11_A22_INTERP = DIR_PATH.joinpath(
    "..", "data", "mapdl_density_a11_a22_temp_interp.cdb"
)


def test_density_constant_no_temp():
    density = Density(
        density=Quantity(value=[1.34], units="kg m^-3"),
    )

    material = Material(
        name="Material 1",
        material_id=1,
        models=[density],
    )

    mapdl_writer = MapdlWriter(materials=[material])
    material_strings = mapdl_writer.write()

    with open(CONSTANT_DENSITY, "r") as file:
        data = file.read()
        assert data == material_strings[0]


def test_density_single_temp():
    density = Density(
        density=Quantity(value=[1.34], units="kg m^-3"),
        independent_parameters=[
            IndependentParameter(name="Temperature", values=Quantity(value=[22], units="C"))
        ],
    )
    material = Material(
        name="Material 1",
        material_id=1,
        models=[density],
    )
    mapdl_writer = MapdlWriter(materials=[material])
    material_strings = mapdl_writer.write()

    with open(CONSTANT_DENSITY, "r") as file:
        data = file.read()
        assert data == material_strings[0]


def test_density_temp_1():
    density = Density(
        density=Quantity(value=[1.34, 2.25], units="kg m^-3"),
        independent_parameters=[
            IndependentParameter(name="Temperature", values=Quantity(value=[22, 40], units="C"))
        ],
    )
    material = Material(
        name="Material 1",
        material_id=1,
        models=[density],
    )

    mapdl_writer = MapdlWriter(materials=[material])
    material_strings = mapdl_writer.write()
    with open(VARIABLE_DENSITY_TEMP_1, "r") as file:
        data = file.read()
        assert data == material_strings[0]


def test_density_temp_2():
    density = Density(
        density=Quantity(value=[x / 10.0 for x in range(10, 100, 5)], units="kg m^-3"),
        independent_parameters=[
            IndependentParameter(
                name="Temperature", values=Quantity(value=list(range(10, 100, 5)), units="C")
            )
        ],
    )

    material = Material(
        name="Material 1",
        material_id=1,
        models=[density],
    )

    mapdl_writer = MapdlWriter(materials=[material])
    material_strings = mapdl_writer.write()
    with open(VARIABLE_DENSITY_TEMP_2, "r") as file:
        data = file.read()
        assert data == material_strings[0]


def test_density_a11_a22():
    density = Density(
        density=Quantity(value=[1, 2, 3, 1, 2, 3, 1, 2, 3], units="kg m^-3"),
        independent_parameters=[
            IndependentParameter(
                name="Orientation Tensor A11",
                values=Quantity(value=[0, 0.5, 1, 0, 0.5, 1, 0, 0.5, 1], units=""),
            ),
            IndependentParameter(
                name="Orientation Tensor A22",
                values=Quantity(value=[0, 0, 0, 0.5, 0.5, 0.5, 1, 1, 1], units=""),
            ),
        ],
    )
    material = Material(
        name="Material 1",
        material_id=1,
        models=[density],
    )

    mapdl_writer = MapdlWriter(materials=[material])
    material_strings = mapdl_writer.write()
    with open(VARIABLE_DENSITY_A11_A22, "r") as file:
        data = file.read()
        assert data == material_strings[0]


def test_density_temp_a11_a22():
    density = Density(
        density=Quantity(
            value=[1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3], units="kg m^-3"
        ),
        independent_parameters=[
            IndependentParameter(
                name="Orientation Tensor A11",
                values=Quantity(
                    value=[0, 0.5, 1, 0, 0.5, 1, 0, 0.5, 1, 0, 0.5, 1, 0, 0.5, 1, 0, 0.5, 1],
                    units="",
                ),
            ),
            IndependentParameter(
                name="Orientation Tensor A22",
                values=Quantity(
                    value=[0, 0, 0, 0.5, 0.5, 0.5, 1, 1, 1, 0, 0, 0, 0.5, 0.5, 0.5, 1, 1, 1],
                    units="",
                ),
            ),
            IndependentParameter(
                name="Temperature",
                values=Quantity(
                    value=[
                        50,
                        50,
                        50,
                        50,
                        50,
                        50,
                        50,
                        50,
                        50,
                        100,
                        100,
                        100,
                        100,
                        100,
                        100,
                        100,
                        100,
                        100,
                    ],
                    units="C",
                ),
            ),
        ],
    )
    material = Material(
        name="Material 1",
        material_id=1,
        models=[density],
    )

    mapdl_writer = MapdlWriter(materials=[material])
    material_strings = mapdl_writer.write()

    with open(VARIABLE_DENSITY_TEMP_A11_A22, "r") as file:
        data = file.read()
        assert data == material_strings[0]


def test_temp_a11_a22_interpolation():
    density = Density(
        density=Quantity(
            value=[1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3], units="kg m^-3"
        ),
        independent_parameters=[
            IndependentParameter(
                name="Orientation Tensor A11",
                values=Quantity(
                    value=[0, 0.5, 1, 0, 0.5, 1, 0, 0.5, 1, 0, 0.5, 1, 0, 0.5, 1, 0, 0.5, 1],
                    units="",
                ),
                default_value=0.0,
                upper_limit=1.0,
                lower_limit=0.0,
            ),
            IndependentParameter(
                name="Orientation Tensor A22",
                values=Quantity(
                    value=[0, 0, 0, 0.5, 0.5, 0.5, 1, 1, 1, 0, 0, 0, 0.5, 0.5, 0.5, 1, 1, 1],
                    units="",
                ),
                default_value=0.0,
                upper_limit=1.0,
                lower_limit=0.0,
            ),
            IndependentParameter(
                name="Temperature",
                values=Quantity(
                    value=[
                        50,
                        50,
                        50,
                        50,
                        50,
                        50,
                        50,
                        50,
                        50,
                        100,
                        100,
                        100,
                        100,
                        100,
                        100,
                        100,
                        100,
                        100,
                    ],
                    units="C",
                    default_value=22.0,
                    upper_limit=100.0,
                    lower_limit=50.0,
                ),
            ),
        ],
        interpolation_options=InterpolationOptions(
            algorithm_type="Linear Multivariate",
            extrapolation_type="Projection to the Convex Hull",
            normalized=False,
            cached=False,
        ),
    )

    material = Material(
        name="Material 1",
        material_id=1,
        models=[density],
    )

    mapdl_writer = MapdlWriter(materials=[material])
    material_strings = mapdl_writer.write()

    with open(VARIABLE_DENSITY_TEMP_A11_A22_INTERP, "r") as file:
        data = file.read()
        assert data == material_strings[0]
