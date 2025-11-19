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

from ansys.materials.manager._models._material_models.neo_hookean import NeoHookean
from ansys.materials.manager._models.material import Material
from ansys.materials.manager.parsers.mapdl.mapdl_writer import MapdlWriter

DIR_PATH = Path(__file__).resolve().parent
NEO_HOOKEAN_CONSTANT = DIR_PATH.joinpath("..", "data", "mapdl_neo_hookean_constant.cdb")
neo_hookean = NeoHookean(
    initial_shear_modulus=Quantity(value=[27104.0], units="Pa"),
    incompressibility_modulus=Quantity(value=[1e-05], units="Pa^-1"),
)
material = Material(
    name="Neo Hookean constant",
    models=[neo_hookean],
    material_id=1,
)

writer = MapdlWriter(materials=[material])
material_string = writer.write()
with open(NEO_HOOKEAN_CONSTANT, "r") as file:
    data = file.read()
assert data == material_string[0]

neo_hookean = NeoHookean(
    initial_shear_modulus=Quantity(value=[27104.0, 2700.0, 2600.0], units="Pa"),
    incompressibility_modulus=Quantity(value=[1e-05, 2e-05, 3e-05], units="Pa^-1"),
)
material = Material(
    name="Neo Hookean variable",
    models=[neo_hookean],
    material_id=2,
)
writer = MapdlWriter(materials=[material])
material_string = writer.write()
print(material_string)
