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

from ansys.materials.manager._models._common import (
    IndependentParameter,
    InterpolationOptions,
)
from ansys.materials.manager._models._material_models import ElasticityIsotropic
from ansys.materials.manager._models._material_models.elasticity_anisotropic import (
    ElasticityAnisotropic,
)
from ansys.materials.manager._models._material_models.elasticity_orthotropic import (
    ElasticityOrthotropic,
)
from ansys.materials.manager._models.material import Material
from ansys.materials.manager.parsers.mapdl.mapdl_writer import MapdlWriter

DIR_PATH = Path(__file__).resolve().parent
ELASTICITY_ISOTROPIC_CONSTANT = DIR_PATH.joinpath(
    "..", "data", "mapdl_elasticity_isotropic_constant.cdb"
)
ELASTICITY_ISOTROPIC_CONSTANT_REFERENCE_TEMPERATURE = DIR_PATH.joinpath(
    "..", "data", "mapdl_elasticity_isotropic_constant_reference_temperature.cdb"
)
ELASTICITY_ISOTROPIC_VARIABLE_TEMP = DIR_PATH.joinpath(
    "..", "data", "mapdl_elasticity_isotropic_variable.cdb"
)
ELASTICITY_ISOTROPIC_VARIABLE_TEMP_REFERENCE_TEMP = DIR_PATH.joinpath(
    "..", "data", "mapdl_elasticity_isotropic_variable_reference_temperature.cdb"
)
ELASTICITY_ORTHOTROPIC_CONSTANT = DIR_PATH.joinpath(
    "..", "data", "mapdl_elasticity_orthotropic_constant.cdb"
)
ELASTICITY_ORTHOTROPIC_VARIABLE = DIR_PATH.joinpath(
    "..", "data", "mapdl_elasticity_orthotropic_variable.cdb"
)
ELASTICITY_ORTHOTROPIC_VARIABLE_TEMP_A11_A22 = DIR_PATH.joinpath(
    "..", "data", "mapdl_elasticity_orthotropic_variable_temp_a11_a22.cdb"
)
ELASTICITY_ORTHOTROPIC_VARIABLE_A11_A22 = DIR_PATH.joinpath(
    "..", "data", "mapdl_elasticity_orthotropic_variable_a11_a22.cdb"
)
ELASTICITY_ANISOTROPIC_CONSTANT = DIR_PATH.joinpath(
    "..", "data", "mapdl_elasticity_anisotropic_constant.cdb"
)


def test_elasticity_isotropic_constant():
    elasticity = ElasticityIsotropic(
        youngs_modulus=Quantity(value=[1000000], units="Pa"),
        poissons_ratio=Quantity(value=[0.3], units=""),
    )

    material = Material(
        name="Material 2",
        material_id=2,
        models=[elasticity],
    )

    mapdl_writer = MapdlWriter(materials=[material])
    material_strings = mapdl_writer.write()
    with open(ELASTICITY_ISOTROPIC_CONSTANT, "r") as file:
        data = file.read()
        assert data == material_strings[0]


def test_elasticity_isotropic_constant_temperature():
    elasticity = ElasticityIsotropic(
        youngs_modulus=Quantity(value=[1000000], units="Pa"),
        poissons_ratio=Quantity(value=[0.3], units=""),
    )
    material = Material(
        name="Material 2",
        material_id=2,
        models=[elasticity],
    )

    mapdl_writer = MapdlWriter(materials=[material])
    material_strings = mapdl_writer.write(reference_temperatures=[22.0])
    with open(ELASTICITY_ISOTROPIC_CONSTANT_REFERENCE_TEMPERATURE, "r") as file:
        data = file.read()
    assert data == material_strings[0]


def test_elasticity_isotropic_variable():
    elasticity = ElasticityIsotropic(
        youngs_modulus=Quantity(value=[2000000, 1000000], units="Pa"),
        poissons_ratio=Quantity(value=[0.35, 0.3], units=""),
        independent_parameters=[
            IndependentParameter(
                name="Temperature",
                values=Quantity(value=[12.0, 21.0], units="C"),
            )
        ],
    )

    material = Material(
        name="Material 3",
        material_id=3,
        models=[elasticity],
    )

    mapdl_writer = MapdlWriter(materials=[material])
    material_strings = mapdl_writer.write()
    with open(ELASTICITY_ISOTROPIC_VARIABLE_TEMP, "r") as file:
        data = file.read()
        assert data == material_strings[0]


def test_elasticity_isotropic_variable_reference_temperature():
    elasticity = ElasticityIsotropic(
        youngs_modulus=Quantity(value=[2000000, 1000000], units="Pa"),
        poissons_ratio=Quantity(value=[0.35, 0.3], units=""),
        independent_parameters=[
            IndependentParameter(
                name="Temperature",
                values=Quantity(value=[12.0, 77.0], units="C"),
            )
        ],
    )

    material = Material(
        name="Material 3",
        material_id=3,
        models=[elasticity],
    )

    mapdl_writer = MapdlWriter(materials=[material])
    material_strings = mapdl_writer.write(reference_temperatures=[35.0])
    with open(ELASTICITY_ISOTROPIC_VARIABLE_TEMP_REFERENCE_TEMP, "r") as file:
        data = file.read()
        assert data == material_strings[0]


def test_elasticity_orthotropic_constant():
    elasticity = ElasticityOrthotropic(
        youngs_modulus_x=Quantity(value=[1000000], units="Pa"),
        youngs_modulus_y=Quantity(value=[1500000], units="Pa"),
        youngs_modulus_z=Quantity(value=[2000000], units="Pa"),
        poissons_ratio_xy=Quantity(value=[0.2], units=""),
        poissons_ratio_yz=Quantity(value=[0.3], units=""),
        poissons_ratio_xz=Quantity(value=[0.4], units=""),
        shear_modulus_xy=Quantity(value=[1000000], units="Pa"),
        shear_modulus_yz=Quantity(value=[2000000], units="Pa"),
        shear_modulus_xz=Quantity(value=[3000000], units="Pa"),
    )

    material = Material(
        name="Material 1",
        material_id=1,
        models=[elasticity],
    )

    mapdl_writer = MapdlWriter(materials=[material])
    material_strings = mapdl_writer.write()

    with open(ELASTICITY_ORTHOTROPIC_CONSTANT, "r") as file:
        data = file.read()
        assert data == material_strings[0]


def test_elasticity_orthotropic_variable_temp():
    elasticity = ElasticityOrthotropic(
        youngs_modulus_x=Quantity(value=[1000000, 1100000, 1200000], units="Pa"),
        youngs_modulus_y=Quantity(value=[1500000, 1600000, 1700000], units="Pa"),
        youngs_modulus_z=Quantity(value=[2000000, 2200000, 2300000], units="Pa"),
        poissons_ratio_xy=Quantity(value=[0.2, 0.21, 0.22], units=""),
        poissons_ratio_yz=Quantity(value=[0.3, 0.31, 0.32], units=""),
        poissons_ratio_xz=Quantity(value=[0.4, 0.41, 0.42], units=""),
        shear_modulus_xy=Quantity(value=[1000000, 1100000, 1200000], units="Pa"),
        shear_modulus_yz=Quantity(value=[2000000, 2100000, 2200000], units="Pa"),
        shear_modulus_xz=Quantity(value=[3000000, 3100000, 3200000], units="Pa"),
        independent_parameters=[
            IndependentParameter(
                name="Temperature",
                values=Quantity(value=[12.0, 21.0, 31], units="C"),
            )
        ],
    )

    material = Material(
        name="Material 1",
        material_id=1,
        models=[elasticity],
    )

    mapdl_writer = MapdlWriter(materials=[material])
    material_strings = mapdl_writer.write()
    with open(ELASTICITY_ORTHOTROPIC_VARIABLE, "r") as file:
        data = file.read()
        assert data == material_strings[0]


def test_elasticity_orthotropic_variable_temp_a11_a22():
    elasticity = ElasticityOrthotropic(
        youngs_modulus_x=Quantity(
            value=[
                100,
                200,
                300,
                100,
                200,
                300,
                100,
                200,
                300,
                100,
                200,
                300,
                100,
                200,
                300,
                100,
                200,
                300,
            ],
            units="Pa",
        ),
        youngs_modulus_y=Quantity(
            value=[
                110,
                210,
                310,
                110,
                210,
                310,
                110,
                210,
                310,
                110,
                210,
                310,
                110,
                210,
                310,
                110,
                210,
                310,
            ],
            units="Pa",
        ),
        youngs_modulus_z=Quantity(
            value=[
                120,
                220,
                320,
                120,
                220,
                320,
                120,
                220,
                320,
                120,
                220,
                320,
                120,
                220,
                320,
                120,
                220,
                320,
            ],
            units="Pa",
        ),
        poissons_ratio_xy=Quantity(
            value=[
                0.1,
                0.2,
                0.3,
                0.1,
                0.2,
                0.3,
                0.1,
                0.2,
                0.3,
                0.1,
                0.2,
                0.3,
                0.1,
                0.2,
                0.3,
                0.1,
                0.2,
                0.3,
            ],
            units="",
        ),
        poissons_ratio_yz=Quantity(
            value=[
                0.11,
                0.21,
                0.31,
                0.11,
                0.21,
                0.31,
                0.11,
                0.21,
                0.31,
                0.11,
                0.21,
                0.31,
                0.11,
                0.21,
                0.31,
                0.11,
                0.21,
                0.31,
            ],
            units="",
        ),
        poissons_ratio_xz=Quantity(
            value=[
                0.12,
                0.22,
                0.32,
                0.12,
                0.22,
                0.32,
                0.12,
                0.22,
                0.32,
                0.12,
                0.22,
                0.32,
                0.12,
                0.22,
                0.23,
                0.12,
                0.22,
                0.32,
            ],
            units="",
        ),
        shear_modulus_xy=Quantity(
            value=[10, 20, 30, 10, 20, 30, 10, 20, 30, 10, 20, 30, 10, 20, 30, 10, 20, 30],
            units="Pa",
        ),
        shear_modulus_yz=Quantity(
            value=[11, 21, 31, 11, 21, 31, 11, 21, 31, 11, 21, 31, 11, 12, 31, 11, 21, 31],
            units="Pa",
        ),
        shear_modulus_xz=Quantity(
            value=[12, 22, 32, 12, 22, 32, 12, 22, 32, 12, 22, 32, 12, 22, 32, 12, 22, 32],
            units="Pa",
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
                ),
                default_value=22.0,
                upper_limit="Program Controlled",
                lower_limit="Program Controlled",
            ),
        ],
        interpolation_options=InterpolationOptions(
            algorithm_type="Linear Multivariate",
            extrapolation_type="Projection to the Convex Hull",
        ),
    )
    material = Material(
        name="Material 1",
        material_id=1,
        models=[elasticity],
    )

    mapdl_writer = MapdlWriter(materials=[material])
    material_strings = mapdl_writer.write(reference_temperatures=[22.0])
    with open(ELASTICITY_ORTHOTROPIC_VARIABLE_TEMP_A11_A22, "r") as file:
        data = file.read()
        assert data == material_strings[0]


def test_elasticity_orthotropic_variable_a11_a22():
    elasticity = ElasticityOrthotropic(
        youngs_modulus_x=Quantity(value=[100, 200, 300, 100, 200, 300, 100, 200, 300], units="Pa"),
        youngs_modulus_y=Quantity(value=[110, 210, 310, 110, 210, 310, 110, 210, 310], units="Pa"),
        youngs_modulus_z=Quantity(value=[120, 220, 320, 120, 220, 320, 120, 220, 320], units="Pa"),
        poissons_ratio_xy=Quantity(value=[0.1, 0.2, 0.3, 0.1, 0.2, 0.3, 0.1, 0.2, 0.3], units=""),
        poissons_ratio_yz=Quantity(
            value=[0.11, 0.21, 0.31, 0.11, 0.21, 0.31, 0.11, 0.21, 0.31], units=""
        ),
        poissons_ratio_xz=Quantity(
            value=[0.12, 0.22, 0.32, 0.12, 0.22, 0.32, 0.12, 0.22, 0.32], units=""
        ),
        shear_modulus_xy=Quantity(value=[10, 20, 30, 10, 20, 30, 10, 20, 30], units="Pa"),
        shear_modulus_yz=Quantity(value=[11, 21, 31, 11, 21, 31, 11, 21, 31], units="Pa"),
        shear_modulus_xz=Quantity(value=[12, 22, 32, 12, 22, 32, 12, 22, 32], units="Pa"),
        independent_parameters=[
            IndependentParameter(
                name="Orientation Tensor A11",
                values=Quantity(
                    value=[0, 0.5, 1, 0, 0.5, 1, 0, 0.5, 1],
                    units="",
                ),
                default_value=0.0,
                upper_limit=1.0,
                lower_limit=0.0,
            ),
            IndependentParameter(
                name="Orientation Tensor A22",
                values=Quantity(value=[0, 0, 0, 0.5, 0.5, 0.5, 1, 1, 1], units=""),
                default_value=0.0,
                upper_limit=1.0,
                lower_limit=0.0,
            ),
        ],
    )

    material = Material(
        name="Material 1",
        material_id=1,
        models=[elasticity],
    )

    mapdl_writer = MapdlWriter(materials=[material])
    material_strings = mapdl_writer.write()
    with open(ELASTICITY_ORTHOTROPIC_VARIABLE_A11_A22, "r") as file:
        data = file.read()
        assert data == material_strings[0]


def test_elasticity_anisotropic_constant():
    elasticity = ElasticityAnisotropic(
        c_11=Quantity(value=[100000000.0], units="Pa"),
        c_12=Quantity(value=[1000000.0], units="Pa"),
        c_13=Quantity(value=[2000000.0], units="Pa"),
        c_14=Quantity(value=[0.0], units="Pa"),
        c_15=Quantity(value=[0.0], units="Pa"),
        c_16=Quantity(value=[0.0], units="Pa"),
        c_22=Quantity(value=[150000000.0], units="Pa"),
        c_23=Quantity(value=[3000000.0], units="Pa"),
        c_24=Quantity(value=[0.0], units="Pa"),
        c_25=Quantity(value=[0.0], units="Pa"),
        c_26=Quantity(value=[0.0], units="Pa"),
        c_33=Quantity(value=[200000000.0], units="Pa"),
        c_34=Quantity(value=[0.0], units="Pa"),
        c_35=Quantity(value=[0.0], units="Pa"),
        c_36=Quantity(value=[0.0], units="Pa"),
        c_44=Quantity(value=[50000000.0], units="Pa"),
        c_45=Quantity(value=[0.0], units="Pa"),
        c_46=Quantity(value=[0.0], units="Pa"),
        c_55=Quantity(value=[60000000.0], units="Pa"),
        c_56=Quantity(value=[0.0], units="Pa"),
        c_66=Quantity(value=[70000000.0], units="Pa"),
    )
    material = Material(
        name="Material 1",
        material_id=1,
        models=[elasticity],
    )

    mapdl_writer = MapdlWriter(materials=[material])
    material_strings = mapdl_writer.write()

    with open(ELASTICITY_ANISOTROPIC_CONSTANT, "r") as file:
        data = file.read()
        assert data == material_strings[0]
