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

from ansys.materials.manager._models._common._base import _MapdlCore
from ansys.materials.manager._models._common.independent_parameter import IndependentParameter
from ansys.materials.manager._models._common.interpolation_options import InterpolationOptions
from ansys.materials.manager._models._material_models import HillYieldCriterion

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
HILL_CONSTANT = os.path.join(DIR_PATH, "..", "data", "mapdl_hill_constant.cdb")
HILL_VARIABLE_TEMP = os.path.join(DIR_PATH, "..", "data", "mapdl_hill_variable_temp.cdb")
HILL_VARIABLE_A11_A22 = os.path.join(DIR_PATH, "..", "data", "mapdl_hill_variable_a11_a22.cdb")


# def test_hill_constant():
hill = HillYieldCriterion(
    yield_stress_ratio_x=Quantity(value=[1.2], units=""),
    yield_stress_ratio_xy=Quantity(value=[0.12], units=""),
    yield_stress_ratio_xz=Quantity(value=[0.23], units=""),
    yield_stress_ratio_y=Quantity(value=[0.8], units=""),
    yield_stress_ratio_yz=Quantity(value=[0.23], units=""),
    yield_stress_ratio_z=Quantity(value=[0.5], units=""),
)

mock_mapdl = MagicMock(spec=_MapdlCore)
material_string = hill.write_model(material_id=2, pyansys_session=mock_mapdl)
with open(HILL_CONSTANT, "r") as file:
    data = file.read()
    assert data == material_string

# def test_hill_variable_temp():
hill = HillYieldCriterion(
    yield_stress_ratio_x=Quantity(value=[1.2, 1.2, 1.4], units=""),
    yield_stress_ratio_y=Quantity(value=[0.8, 0.8, 0.7], units=""),
    yield_stress_ratio_z=Quantity(value=[0.5, 0.5, 0.4], units=""),
    yield_stress_ratio_xy=Quantity(value=[0.12, 0.12, 0.12], units=""),
    yield_stress_ratio_yz=Quantity(value=[0.23, 0.23, 0.23], units=""),
    yield_stress_ratio_xz=Quantity(value=[0.23, 0.23, 0.23], units=""),
    independent_parameters=[
        IndependentParameter(name="Temperature", values=Quantity(value=[34, 78, 245], units="C"))
    ],
)
mock_mapdl = MagicMock(spec=_MapdlCore)
material_string = hill.write_model(material_id=2, pyansys_session=mock_mapdl)
with open(HILL_VARIABLE_TEMP, "r") as file:
    data = file.read()
    assert data == material_string

# def test_hill_variable_a11_a22():
hill = HillYieldCriterion(
    yield_stress_ratio_x=Quantity(
        value=[1, 1.38717930847789, 3.00721990713311, 1.2181891328774, 1, 1.38717930847789, 1],
        units="",
    ),
    yield_stress_ratio_y=Quantity(
        value=[1, 1, 1, 1.2181891328774, 1.38717930847789, 1.38717930847789, 3.00721990713311],
        units="",
    ),
    yield_stress_ratio_z=Quantity(
        value=[3.00721990713311, 1.38717930847789, 1, 1.21818913296279, 1.38717930847789, 1, 1],
        units="",
    ),
    yield_stress_ratio_xy=Quantity(
        value=[
            1.27583858742812,
            1.27583858742812,
            1.27583858742812,
            1.27583858742812,
            1.27583858742812,
            1.27583858742812,
            1.27583858742812,
        ],
        units="",
    ),
    yield_stress_ratio_yz=Quantity(
        value=[
            1.27583858742812,
            1.27583858742812,
            1.27583858742812,
            1.27583858742812,
            1.27583858742812,
            1.27583858742812,
            1.27583858742812,
        ],
        units="",
    ),
    yield_stress_ratio_xz=Quantity(
        value=[
            1.27583858742812,
            1.27583858742812,
            1.27583858742812,
            1.27583858742812,
            1.27583858742812,
            1.27583858742812,
            1.27583858742812,
        ],
        units="",
    ),
    independent_parameters=[
        IndependentParameter(
            name="Orientation Tensor A11",
            values=Quantity(value=[0, 0.5, 1, 0.3333333333, 0, 0.5, 0], units=""),
            upper_limit=1.0,
            lower_limit=0.0,
            default_value=0.0,
        ),
        IndependentParameter(
            name="Orientation Tensor A22",
            values=Quantity(value=[0, 0, 0, 0.3333333333, 0.5, 0.5, 1], units=""),
            upper_limit=1.0,
            lower_limit=0.0,
            default_value=0.0,
        ),
    ],
    interpolation_options=InterpolationOptions(algorithm_type="Linear Multivariate"),
)
mock_mapdl = MagicMock(spec=_MapdlCore)
material_string = hill.write_model(material_id=2, pyansys_session=mock_mapdl)
with open(HILL_VARIABLE_A11_A22, "r") as file:
    data = file.read()
    assert data == material_string
