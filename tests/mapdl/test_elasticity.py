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
from ansys.materials.manager._models._material_models import ElasticityIsotropic
from ansys.materials.manager._models._material_models.elasticity_orthotropic import (
    ElasticityOrthotropic,
)

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
ELASTICITY_ISOTROPIC_CONSTANT = os.path.join(
    DIR_PATH, "..", "data", "mapdl_elasticity_isotropic_constant.cdb"
)
ELASTICITY_ISOTROPIC_VARIABLE_TEMP = os.path.join(
    DIR_PATH, "..", "data", "mapdl_elasticity_isotropic_variable.cdb"
)
ELASTICITY_ORTHOTROPIC_CONSTANT = os.path.join(
    DIR_PATH, "..", "data", "mapdl_elasticity_orthotropic_constant.cdb"
)
ELASTICITY_ORTHOTROPIC_VARIABLE = os.path.join(
    DIR_PATH, "..", "data", "mapdl_elasticity_orthotropic_variable.cdb"
)
# def test_elasticity_isotropic_constant():
elasticity = ElasticityIsotropic(
    youngs_modulus=Quantity(value=[1000000], units="Pa"),
    poissons_ratio=Quantity(value=[0.3], unit=""),
)
mock_mapdl = MagicMock(spec=_MapdlCore)
material_string = elasticity.write_model(material_id=2, pyansys_session=mock_mapdl)
with open(ELASTICITY_ISOTROPIC_CONSTANT, "r") as file:
    data = file.read()
    assert data == material_string

# def test_elasticity_isotropic_variable():
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

# def test_elasticity_orthotropic_constant():
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

# def test_elasticity_orthotropic_variable():
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
