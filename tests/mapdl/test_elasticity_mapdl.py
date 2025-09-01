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
from unittest.mock import MagicMock

from ansys.units import Quantity

from ansys.materials.manager._models._common import IndependentParameter, InterpolationOptions
from ansys.materials.manager._models._common._base import _MapdlCore
from ansys.materials.manager._models._material_models import ElasticityIsotropic
from ansys.materials.manager._models._material_models.elasticity_anisotropic import (
    ElasticityAnisotropic,
)
from ansys.materials.manager._models._material_models.elasticity_orthotropic import (
    ElasticityOrthotropic,
)

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
ELASTICITY_ISOTROPIC_CONSTANT = os.path.join(
    DIR_PATH, "..", "data", "mapdl_elasticity_isotropic_constant.cdb"
)
ELASTICITY_ISOTROPIC_CONSTANT_REFERENCE_TEMPERATURE = os.path.join(
    DIR_PATH, "..", "data", "mapdl_elasticity_isotropic_constant_reference_temperature.cdb"
)
ELASTICITY_ISOTROPIC_VARIABLE_TEMP = os.path.join(
    DIR_PATH, "..", "data", "mapdl_elasticity_isotropic_variable.cdb"
)
ELASTICITY_ISOTROPIC_VARIABLE_TEMP_REFERENCE_TEMP = os.path.join(
    DIR_PATH, "..", "data", "mapdl_elasticity_isotropic_variable_reference_temperature.cdb"
)
ELASTICITY_ORTHOTROPIC_CONSTANT = os.path.join(
    DIR_PATH, "..", "data", "mapdl_elasticity_orthotropic_constant.cdb"
)
ELASTICITY_ORTHOTROPIC_VARIABLE = os.path.join(
    DIR_PATH, "..", "data", "mapdl_elasticity_orthotropic_variable.cdb"
)
ELASTICITY_ORTHOTROPIC_VARIABLE_TEMP_A11_A22 = os.path.join(
    DIR_PATH, "..", "data", "mapdl_elasticity_orthotropic_variable_temp_a11_a22.cdb"
)
ELASTICITY_ORTHOTROPIC_VARIABLE_A11_A22 = os.path.join(
    DIR_PATH, "..", "data", "mapdl_elasticity_orthotropic_variable_a11_a22.cdb"
)
ELASTICITY_ANISOTROPIC_CONSTANT = os.path.join(
    DIR_PATH, "..", "data", "mapdl_elasticity_anisotropic_constant.cdb"
)


def test_elasticity_isotropic_constant():
    elasticity = ElasticityIsotropic(
        youngs_modulus=Quantity(value=[1000000], units="Pa"),
        poissons_ratio=Quantity(value=[0.3], units=""),
    )
    mock_mapdl = MagicMock(spec=_MapdlCore)
    material_string = elasticity.write_model(material_id=2, pyansys_session=mock_mapdl)
    with open(ELASTICITY_ISOTROPIC_CONSTANT, "r") as file:
        data = file.read()
        assert data == material_string


def test_elasticity_isotropic_constant_temperature():
    elasticity = ElasticityIsotropic(
        youngs_modulus=Quantity(value=[1000000], units="Pa"),
        poissons_ratio=Quantity(value=[0.3], units=""),
        independent_parameters=[
            IndependentParameter(
                name="Temperature",
                values=Quantity(value=[7.88860905221012e-31], units="C"),
                default_value=22.0,
            )
        ],
    )
    mock_mapdl = MagicMock(spec=_MapdlCore)
    material_string = elasticity.write_model(material_id=2, pyansys_session=mock_mapdl)
    with open(ELASTICITY_ISOTROPIC_CONSTANT_REFERENCE_TEMPERATURE, "r") as file:
        data = file.read()
    assert data == material_string


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
    mock_mapdl = MagicMock(spec=_MapdlCore)
    material_string = elasticity.write_model(material_id=3, pyansys_session=mock_mapdl)
    with open(ELASTICITY_ISOTROPIC_VARIABLE_TEMP, "r") as file:
        data = file.read()
        assert data == material_string


def test_elasticity_isotropic_variable_reference_temperature():
    elasticity = ElasticityIsotropic(
        youngs_modulus=Quantity(value=[2000000, 1000000], units="Pa"),
        poissons_ratio=Quantity(value=[0.35, 0.3], units=""),
        independent_parameters=[
            IndependentParameter(
                name="Temperature",
                values=Quantity(value=[12.0, 77.0], units="C"),
                default_value=35,
            )
        ],
    )
    mock_mapdl = MagicMock(spec=_MapdlCore)
    material_string = elasticity.write_model(material_id=3, pyansys_session=mock_mapdl)
    print(material_string)
    with open(ELASTICITY_ISOTROPIC_VARIABLE_TEMP_REFERENCE_TEMP, "r") as file:
        data = file.read()
        assert data == material_string


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
    mock_mapdl = MagicMock(spec=_MapdlCore)
    material_string = elasticity.write_model(material_id=1, pyansys_session=mock_mapdl)
    with open(ELASTICITY_ORTHOTROPIC_CONSTANT, "r") as file:
        data = file.read()
        assert data == material_string


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
    mock_mapdl = MagicMock(spec=_MapdlCore)
    material_string = elasticity.write_model(material_id=1, pyansys_session=mock_mapdl)
    with open(ELASTICITY_ORTHOTROPIC_VARIABLE, "r") as file:
        data = file.read()
        assert data == material_string


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
    mock_mapdl = MagicMock(spec=_MapdlCore)
    material_string = elasticity.write_model(material_id=1, pyansys_session=mock_mapdl)
    with open(ELASTICITY_ORTHOTROPIC_VARIABLE_TEMP_A11_A22, "r") as file:
        data = file.read()
        assert data == material_string


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
    mock_mapdl = MagicMock(spec=_MapdlCore)
    material_string = elasticity.write_model(material_id=1, pyansys_session=mock_mapdl)
    print(material_string)
    with open(ELASTICITY_ORTHOTROPIC_VARIABLE_A11_A22, "r") as file:
        data = file.read()
        assert data == material_string


def test_elasticity_anisotropic_constant():
    elasticity = ElasticityAnisotropic(
        column_1=Quantity(
            value=[100000000, 1000000, 2000000, 3000000, 4000000, 5000000], units="Pa"
        ),
        column_2=Quantity(
            value=[7.88860905221012e-31, 150000000, 6000000, 7000000, 8000000, 9000000],
            units="Pa",
        ),
        column_3=Quantity(
            value=[
                7.88860905221012e-31,
                7.88860905221012e-31,
                200000000,
                10000000,
                11000000,
                12000000,
            ],
            units="Pa",
        ),
        column_4=Quantity(
            value=[
                7.88860905221012e-31,
                7.88860905221012e-31,
                7.88860905221012e-31,
                50000000,
                13000000,
                14000000,
            ],
            units="Pa",
        ),
        column_5=Quantity(
            value=[
                7.88860905221012e-31,
                7.88860905221012e-31,
                7.88860905221012e-31,
                7.88860905221012e-31,
                60000000,
                15000000,
            ],
            units="Pa",
        ),
        column_6=Quantity(
            value=[
                7.88860905221012e-31,
                7.88860905221012e-31,
                7.88860905221012e-31,
                7.88860905221012e-31,
                7.88860905221012e-31,
                70000000,
            ],
            units="Pa",
        ),
    )

    mock_mapdl = MagicMock(spec=_MapdlCore)
    material_string = elasticity.write_model(material_id=1, pyansys_session=mock_mapdl)
    with open(ELASTICITY_ANISOTROPIC_CONSTANT, "r") as file:
        data = file.read()
        assert data == material_string


elasticity = ElasticityIsotropic(
    youngs_modulus=Quantity(value=[1000000], units="Pa"),
    poissons_ratio=Quantity(value=[0.3], units=""),
    independent_parameters=[
        IndependentParameter(
            name="Temperature",
            values=Quantity(value=[7.88860905221012e-31], units="C"),
            default_value=22.0,
        )
    ],
)
mock_mapdl = MagicMock(spec=_MapdlCore)
material_string = elasticity.write_model(material_id=2, pyansys_session=mock_mapdl)
with open(ELASTICITY_ISOTROPIC_CONSTANT, "r") as file:
    data = file.read()
    print(material_string)
