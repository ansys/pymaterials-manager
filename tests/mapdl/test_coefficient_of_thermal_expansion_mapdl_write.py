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
from ansys.materials.manager._models._common.model_qualifier import ModelQualifier
from ansys.materials.manager._models._material_models.cofficient_of_thermal_expansion_isotropic import (  # noqa: E501
    CoefficientofThermalExpansionIsotropic,
)
from ansys.materials.manager._models._material_models.cofficient_of_thermal_expansion_orthotropic import (  # noqa: E501
    CoefficientofThermalExpansionOrthotropic,
)

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
COEFFICIENT_OF_THERMAL_EXPANSION_SECANT_ISOTROPIC_CONSTANT = os.path.join(
    DIR_PATH, "..", "data", "mapdl_coefficient_of_thermal_expansion_isotropic_secant_constant.cdb"
)
COEFFICIENT_OF_THERMAL_EXPANSION_SECANT_ISOTROPIC_CONSTANT_REF_TEMP = os.path.join(
    DIR_PATH,
    "..",
    "data",
    "mapdl_coefficient_of_thermal_expansion_isotropic_secant_constant_ref_temp.cdb",
)
COEFFICIENT_OF_THERMAL_EXPANSION_SECANT_ISOTROPIC_VARIABLE = os.path.join(
    DIR_PATH, "..", "data", "mapdl_coefficient_of_thermal_expansion_isotropic_secant_variable.cdb"
)
COEFFICIENT_OF_THERMAL_EXPANSION_SECANT_ISOTROPIC_VARIABLE_A11_A22 = os.path.join(
    DIR_PATH,
    "..",
    "data",
    "mapdl_coefficient_of_thermal_expansion_isotropic_secant_variable_a11_a22.cdb",
)
COEFFICIENT_OF_THERMAL_EXPANSION_SECANT_ORTHOTROPIC_CONSTANT = os.path.join(
    DIR_PATH, "..", "data", "mapdl_coefficient_of_thermal_expansion_orthotropic_secant_constant.cdb"
)
COEFFICIENT_OF_THERMAL_EXPANSION_SECANT_ORTHOTROPIC_CONSTANT_REF_TEMP = os.path.join(
    DIR_PATH,
    "..",
    "data",
    "mapdl_coefficient_of_thermal_expansion_orthotropic_secant_constant_ref_temp.cdb",
)
COEFFICIENT_OF_THERMAL_EXPANSION_SECANT_ORTHOTROPIC_VARIABLE = os.path.join(
    DIR_PATH, "..", "data", "mapdl_coefficient_of_thermal_expansion_orthotropic_secant_variable.cdb"
)
COEFFICIENT_OF_THERMAL_EXPANSION_SECANT_ORTHOTROPIC_VARIABLE_A11_A22 = os.path.join(
    DIR_PATH,
    "..",
    "data",
    "mapdl_coefficient_of_thermal_expansion_orthotropic_secant_variable_a11_a22.cdb",
)


def test_coefficient_of_thermal_expansion_coefficient_isotropic_secant_constant():
    thermal_conductivity = CoefficientofThermalExpansionIsotropic(
        model_qualifiers=[ModelQualifier(name="Definition", value="Secant")],
        coefficient_of_thermal_expansion=Quantity(value=[1.0], units="C^-1"),
    )
    mock_mapdl = MagicMock(spec=_MapdlCore)
    material_string = thermal_conductivity.write_model(material_id=1, pyansys_session=mock_mapdl)
    with open(COEFFICIENT_OF_THERMAL_EXPANSION_SECANT_ISOTROPIC_CONSTANT, "r") as file:
        data = file.read()
        assert data == material_string


def test_coefficient_of_thermal_expansion_coefficient_isotropic_secant_ref_temperature():
    thermal_conductivity = CoefficientofThermalExpansionIsotropic(
        model_qualifiers=[ModelQualifier(name="Definition", value="Secant")],
        coefficient_of_thermal_expansion=Quantity(value=[1.0], units="C^-1"),
    )

    mock_mapdl = MagicMock(spec=_MapdlCore)
    material_string = thermal_conductivity.write_model(
        material_id=2, pyansys_session=mock_mapdl, reference_temperature=22.0
    )
    with open(COEFFICIENT_OF_THERMAL_EXPANSION_SECANT_ISOTROPIC_CONSTANT_REF_TEMP, "r") as file:
        data = file.read()
        assert data == material_string


def test_coefficient_of_thermal_expansion_coefficient_isotropic_secant_variable():
    thermal_conductivity = CoefficientofThermalExpansionIsotropic(
        model_qualifiers=[ModelQualifier(name="Definition", value="Secant")],
        coefficient_of_thermal_expansion=Quantity(value=[1.0, 1.1, 1.2], units="C^-1"),
        independent_parameters=[
            IndependentParameter(
                name="Temperature",
                values=Quantity(value=[18.0, 22.0, 24.0], units="C"),
                default_value=22.0,
            )
        ],
    )

    mock_mapdl = MagicMock(spec=_MapdlCore)
    material_string = thermal_conductivity.write_model(
        material_id=3, pyansys_session=mock_mapdl, reference_temperature=22.0
    )
    with open(COEFFICIENT_OF_THERMAL_EXPANSION_SECANT_ISOTROPIC_VARIABLE, "r") as file:
        data = file.read()
        assert data == material_string


def test_coefficient_of_thermal_expansion_coefficient_isotropic_secant_variable_a11_a22():
    thermal_conductivity = CoefficientofThermalExpansionIsotropic(
        model_qualifiers=[ModelQualifier(name="Definition", value="Secant")],
        coefficient_of_thermal_expansion=Quantity(
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
                0.32,
                0.12,
                0.22,
                0.32,
            ],
            units="C^-1",
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
    material_string = thermal_conductivity.write_model(material_id=4, pyansys_session=mock_mapdl)
    with open(COEFFICIENT_OF_THERMAL_EXPANSION_SECANT_ISOTROPIC_VARIABLE_A11_A22, "r") as file:
        data = file.read()
        assert data == material_string


def test_coefficient_of_thermal_expansion_coefficient_orthotropic_secant_constant():
    thermal_conductivity = CoefficientofThermalExpansionOrthotropic(
        model_qualifiers=[ModelQualifier(name="Definition", value="Secant")],
        coefficient_of_thermal_expansion_x=Quantity(value=[1.0], units="C^-1"),
        coefficient_of_thermal_expansion_y=Quantity(value=[2.0], units="C^-1"),
        coefficient_of_thermal_expansion_z=Quantity(value=[3.0], units="C^-1"),
    )
    mock_mapdl = MagicMock(spec=_MapdlCore)
    material_string = thermal_conductivity.write_model(material_id=5, pyansys_session=mock_mapdl)
    with open(COEFFICIENT_OF_THERMAL_EXPANSION_SECANT_ORTHOTROPIC_CONSTANT, "r") as file:
        data = file.read()
        assert data == material_string


def test_coefficient_of_thermal_expansion_coefficient_orthotropic_secant_constant_ref_temp():
    thermal_conductivity = CoefficientofThermalExpansionOrthotropic(
        model_qualifiers=[ModelQualifier(name="Definition", value="Secant")],
        coefficient_of_thermal_expansion_x=Quantity(value=[1.0], units="C^-1"),
        coefficient_of_thermal_expansion_y=Quantity(value=[2.0], units="C^-1"),
        coefficient_of_thermal_expansion_z=Quantity(value=[3.0], units="C^-1"),
    )
    mock_mapdl = MagicMock(spec=_MapdlCore)
    material_string = thermal_conductivity.write_model(
        material_id=6, pyansys_session=mock_mapdl, reference_temperature=22.0
    )
    with open(COEFFICIENT_OF_THERMAL_EXPANSION_SECANT_ORTHOTROPIC_CONSTANT_REF_TEMP, "r") as file:
        data = file.read()
        assert data == material_string


def test_coefficient_of_thermal_expansion_coefficient_orthotropic_secant_variable():
    thermal_conductivity = CoefficientofThermalExpansionOrthotropic(
        model_qualifiers=[ModelQualifier(name="Definition", value="Secant")],
        coefficient_of_thermal_expansion_x=Quantity(value=[1.0, 1.1, 1.2], units="C^-1"),
        coefficient_of_thermal_expansion_y=Quantity(value=[2.0, 2.1, 2.2], units="C^-1"),
        coefficient_of_thermal_expansion_z=Quantity(value=[3.0, 3.1, 3.2], units="C^-1"),
        independent_parameters=[
            IndependentParameter(
                name="Temperature",
                values=Quantity(value=[15.0, 22.0, 30.0], units="C"),
                default_value=22.0,
            )
        ],
    )
    mock_mapdl = MagicMock(spec=_MapdlCore)
    material_string = thermal_conductivity.write_model(
        material_id=7, pyansys_session=mock_mapdl, reference_temperature=22.0
    )
    with open(COEFFICIENT_OF_THERMAL_EXPANSION_SECANT_ORTHOTROPIC_VARIABLE, "r") as file:
        data = file.read()
        assert data == material_string


def test_coefficient_of_thermal_expansion_coefficient_orthotropic_secant_variable_a11_a22():
    thermal_conductivity = CoefficientofThermalExpansionOrthotropic(
        model_qualifiers=[ModelQualifier(name="Definition", value="Secant")],
        coefficient_of_thermal_expansion_x=Quantity(
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
                0.32,
                0.12,
                0.22,
                0.32,
            ],
            units="C^-1",
        ),
        coefficient_of_thermal_expansion_y=Quantity(
            value=[
                0.13,
                0.23,
                0.33,
                0.13,
                0.23,
                0.33,
                0.13,
                0.23,
                0.33,
                0.13,
                0.23,
                0.33,
                0.13,
                0.23,
                0.33,
                0.13,
                0.23,
                0.33,
            ],
            units="C^-1",
        ),
        coefficient_of_thermal_expansion_z=Quantity(
            value=[
                0.14,
                0.24,
                0.34,
                0.14,
                0.24,
                0.34,
                0.14,
                0.24,
                0.34,
                0.14,
                0.24,
                0.34,
                0.14,
                0.24,
                0.34,
                0.14,
                0.24,
                0.34,
            ],
            units="C^-1",
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
    with open(COEFFICIENT_OF_THERMAL_EXPANSION_SECANT_ORTHOTROPIC_VARIABLE_A11_A22, "r") as file:
        data = file.read()
        assert data == material_string
