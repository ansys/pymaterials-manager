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

from ansys.materials.manager._models._common import _MapdlCore
from ansys.materials.manager._models._common.independent_parameter import IndependentParameter
from ansys.materials.manager._models._material_models.thermal_conductivity_isotropic import (
    ThermalConductivityIsotropic,
)
from ansys.materials.manager._models._material_models.thermal_conductivity_orthotropic import (
    ThermalConductivityOrthotropic,
)

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
THERMAL_CONDUCTIVITY_ISOTROPIC_CONSTANT = os.path.join(
    DIR_PATH, "..", "data", "mapdl_thermal_conductivity_isotropic_constant.cdb"
)
THERMAL_CONDUCTIVITY_ISOTROPIC_CONSTANT_REFERENCE_TEMPERATURE = os.path.join(
    DIR_PATH, "..", "data", "mapdl_thermal_conductivity_isotropic_constant_ref_temp.cdb"
)
THERMAL_CONDUCTIVITY_ISOTROPIC_VARIABLE_TEMP = os.path.join(
    DIR_PATH, "..", "data", "mapdl_thermal_conductivity_isotropic_variable_temp.cdb"
)
THERMAL_CONDUCTIVITY_ORTHOTROPIC_CONSTANT = os.path.join(
    DIR_PATH, "..", "data", "mapdl_thermal_conductivity_orthotropic_constant.cdb"
)
THERMAL_CONDUCTIVITY_ORTHOTROPIC_CONSTANT_REFERENCE_TEMPERATURE = os.path.join(
    DIR_PATH, "..", "data", "mapdl_thermal_conductivity_orthotropic_constant_ref_temp.cdb"
)
THERMAL_CONDUCTIVITY_ORTHOTROPIC_VARIABLE_TEMP = os.path.join(
    DIR_PATH, "..", "data", "mapdl_thermal_conductivity_orthotropic_variable_temp.cdb"
)
THERMAL_CONDUCTIVITY_ORTHOTROPIC_VARIABLE_A11_A22 = os.path.join(
    DIR_PATH, "..", "data", "mapdl_thermal_conductivity_orthotropic_variable_a11_a22.cdb"
)


def test_thermal_conductivity_isotropic_constant():
    thermal_conductivity = ThermalConductivityIsotropic(
        thermal_conductivity=Quantity(value=[10.0], units="W m^-1 C^-1")
    )
    mock_mapdl = MagicMock(spec=_MapdlCore)
    material_string = thermal_conductivity.write_model(material_id=2, pyansys_session=mock_mapdl)
    with open(THERMAL_CONDUCTIVITY_ISOTROPIC_CONSTANT, "r") as file:
        data = file.read()
        assert data == material_string


def test_thermal_conductivity_isotropic_constant_temperature():
    thermal_conductivity = ThermalConductivityIsotropic(
        thermal_conductivity=Quantity(value=[10.0], units="W m^-1 C^-1"),
        independent_parameters=[
            IndependentParameter(
                name="Temperature",
                values=Quantity(value=[7.88860905221012e-31], units="C"),
                default_value=22.0,
            )
        ],
    )
    mock_mapdl = MagicMock(spec=_MapdlCore)
    material_string = thermal_conductivity.write_model(material_id=3, pyansys_session=mock_mapdl)
    with open(THERMAL_CONDUCTIVITY_ISOTROPIC_CONSTANT_REFERENCE_TEMPERATURE, "r") as file:
        data = file.read()
        assert data == material_string


def test_thermal_conductivity_isotropic_variable():
    thermal_conductivity = ThermalConductivityIsotropic(
        thermal_conductivity=Quantity(value=[10.0, 20.0, 30.0], units="W m^-1 C^-1"),
        independent_parameters=[
            IndependentParameter(
                name="Temperature",
                values=Quantity(value=[12.0, 22.0, 45.0], units="C"),
                default_value=22.0,
            )
        ],
    )

    mock_mapdl = MagicMock(spec=_MapdlCore)
    material_string = thermal_conductivity.write_model(material_id=1, pyansys_session=mock_mapdl)
    with open(THERMAL_CONDUCTIVITY_ISOTROPIC_VARIABLE_TEMP, "r") as file:
        data = file.read()
        assert data == material_string


def test_thermal_conductivity_orthotropic_constant():
    thermal_conductivity = ThermalConductivityOrthotropic(
        thermal_conductivity_x=Quantity(value=[10.0], units="W m^-1 C^-1"),
        thermal_conductivity_y=Quantity(value=[20.0], units="W m^-1 C^-1"),
        thermal_conductivity_z=Quantity(value=[30.0], units="W m^-1 C^-1"),
    )

    mock_mapdl = MagicMock(spec=_MapdlCore)
    material_string = thermal_conductivity.write_model(material_id=4, pyansys_session=mock_mapdl)
    with open(THERMAL_CONDUCTIVITY_ORTHOTROPIC_CONSTANT, "r") as file:
        data = file.read()
        assert data == material_string


def test_thermal_conductivity_orthotropic_constant_reference_temperature():
    thermal_conductivity = ThermalConductivityOrthotropic(
        thermal_conductivity_x=Quantity(value=[10.0], units="W m^-1 C^-1"),
        thermal_conductivity_y=Quantity(value=[20.0], units="W m^-1 C^-1"),
        thermal_conductivity_z=Quantity(value=[30.0], units="W m^-1 C^-1"),
        independent_parameters=[
            IndependentParameter(
                name="Temperature",
                values=Quantity(value=[7.88860905221012e-31], units="C"),
                default_value=22.0,
            )
        ],
    )

    mock_mapdl = MagicMock(spec=_MapdlCore)
    material_string = thermal_conductivity.write_model(material_id=5, pyansys_session=mock_mapdl)
    with open(THERMAL_CONDUCTIVITY_ORTHOTROPIC_CONSTANT_REFERENCE_TEMPERATURE, "r") as file:
        data = file.read()
        assert data == material_string


def test_thermal_conductivity_orthotropic_variable_temperature():
    thermal_conductivity = ThermalConductivityOrthotropic(
        thermal_conductivity_x=Quantity(value=[10.0, 11.0, 12.0], units="W m^-1 C^-1"),
        thermal_conductivity_y=Quantity(value=[20.0, 21.0, 22.0], units="W m^-1 C^-1"),
        thermal_conductivity_z=Quantity(value=[30.0, 31.0, 32.0], units="W m^-1 C^-1"),
        independent_parameters=[
            IndependentParameter(
                name="Temperature",
                values=Quantity(value=[12.0, 21.0, 31], units="C"),
                default_value=22.0,
            )
        ],
    )

    mock_mapdl = MagicMock(spec=_MapdlCore)
    material_string = thermal_conductivity.write_model(material_id=6, pyansys_session=mock_mapdl)
    with open(THERMAL_CONDUCTIVITY_ORTHOTROPIC_VARIABLE_TEMP, "r") as file:
        data = file.read()
        assert data == material_string


def test_thermal_conductivity_orthotropic_variable_a11_a22():
    thermal_conductivity = ThermalConductivityOrthotropic(
        thermal_conductivity_x=Quantity(
            value=[
                10.0,
                20.0,
                30.0,
                10.0,
                20.0,
                30.0,
                10.0,
                20.0,
                30.0,
                10.0,
                20.0,
                30.0,
                10.0,
                20.0,
                30.0,
                10.0,
                20.0,
                30.0,
            ],
            units="W m^-1 C^-1",
        ),
        thermal_conductivity_y=Quantity(
            value=[
                11.0,
                21.0,
                31.0,
                11.0,
                21.0,
                31.0,
                11.0,
                21.0,
                31.0,
                11.0,
                21.0,
                31.0,
                11.0,
                21.0,
                31.0,
                11.0,
                21.0,
                31.0,
            ],
            units="W m^-1 C^-1",
        ),
        thermal_conductivity_z=Quantity(
            value=[
                12.0,
                22.0,
                32.0,
                12.0,
                22.0,
                32.0,
                12.0,
                22.0,
                32.0,
                12.0,
                22.0,
                32.0,
                12.0,
                22.0,
                32.0,
                12.0,
                22.0,
                32.0,
            ],
            units="W m^-1 C^-1",
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
        ],
    )

    mock_mapdl = MagicMock(spec=_MapdlCore)
    material_string = thermal_conductivity.write_model(material_id=7, pyansys_session=mock_mapdl)
    with open(THERMAL_CONDUCTIVITY_ORTHOTROPIC_VARIABLE_A11_A22, "r") as file:
        data = file.read()
        assert data == material_string
