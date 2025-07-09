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
from ansys.materials.manager._models._material_models import ElasticityIsotropic

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
ELASTICITY_ISOTROPIC_CONSTANT = os.path.join(
    DIR_PATH, "..", "data", "mapdl_elasticity_isotropic_constant.cdb"
)
elasticity = ElasticityIsotropic(
    youngs_modulus=Quantity(value=[1000000], units="Pa"),
    poissons_ratio=Quantity(value=[0.3], unit=""),
)
mock_mapdl = MagicMock(spec=_MapdlCore)
material_string = elasticity.write_model(material_id=2, pyansys_session=mock_mapdl)
with open(ELASTICITY_ISOTROPIC_CONSTANT, "r") as file:
    data = file.read()
    assert data == material_string
