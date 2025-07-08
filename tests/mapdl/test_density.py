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

from unittest.mock import MagicMock

from ansys.units import Quantity

from ansys.materials.manager._models._common._base import _MapdlCore
from ansys.materials.manager._models._common.independent_parameter import IndependentParameter
from ansys.materials.manager._models._material_models.density import Density

# def test_write_constant_density_apdl():
density = Density(
    density=Quantity(value=[1.34], units="kg m^-3"),
)
mock_mapdl = MagicMock(spec=_MapdlCore)
material_string = density.write_model(material_id=1, pyansys_session=mock_mapdl)
print(material_string)
# assert material_string == "MP, DENS, 1, 1.34"

density = Density(
    density=Quantity(value=[1.34, 2.5], units="kg m^-3"),
    independent_parameters=[
        IndependentParameter(name="Temperature", values=Quantity(value=[22, 30], units="C"))
    ],
)
mock_mapdl = MagicMock(spec=_MapdlCore)
material_string = density.write_model(material_id=1, pyansys_session=mock_mapdl)
print(material_string)
