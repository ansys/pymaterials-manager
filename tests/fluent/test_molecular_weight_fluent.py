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

from ansys.materials.manager._models._common._base import _FluentCore
from ansys.materials.manager._models._material_models.molecular_weight import MolecularWeight


def test_molecular_weight_write_fluent():
    mock_fluent = MagicMock(spec=_FluentCore)
    density = MolecularWeight(molecular_weight=Quantity(value=28.966, units="kg kmol^-1"))
    model = density.write_model(1, mock_fluent)
    mock_fluent.settings.setup.materials.fluid["air"] = model
    mock_fluent.settings.setup.materials.fluid.__setitem__.assert_called_once()
    args = mock_fluent.settings.setup.materials.fluid.__setitem__.call_args
    assert args[0][0] == "air"
    assert args[0][1] == {"molecular_weight": {"option": "constant", "value": 28.966}}
