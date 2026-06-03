# Copyright (C) 2022 - 2026 ANSYS, Inc. and/or its affiliates.
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

from ansys.mapdl.core import Mapdl
import pytest

from ansys.materials.manager.material_manager import MaterialManager

DIR_PATH = Path(__file__).resolve().parent
ELASTICITY_MATML = DIR_PATH.joinpath("..", "data", "matml_unittest_elasticity.xml")

pytestmark = pytest.mark.mapdl_integration


@pytest.fixture(scope="module")
def mapdl():
    mapdl = Mapdl(ip="127.0.0.1", port="50052", local=False)
    mapdl.prep7()
    yield mapdl
    mapdl.mpdele("all", "all")


def test_read_matml_write_apdl(mapdl):
    material_manager = MaterialManager()
    material_manager.read_from_matml(ELASTICITY_MATML)
    material = material_manager.get_material("Isotropic Test Material")
    isotropic_elasticity = material.models[0]
    assert isotropic_elasticity.name == "Elasticity"
    assert isotropic_elasticity.model_qualifiers[0].name == "Behavior"
    assert isotropic_elasticity.model_qualifiers[0].value == "Isotropic"
    assert isotropic_elasticity.model_qualifiers[1].name == "Derive from"
    assert isotropic_elasticity.model_qualifiers[1].value == "Young's Modulus and Poisson's Ratio"
    assert isotropic_elasticity.model_qualifiers[2].name == "Field Variable Compatible"
    assert isotropic_elasticity.model_qualifiers[2].value == "Temperature"
    assert isotropic_elasticity.interpolation_options.algorithm_type == "Linear Multivariate"
    assert isotropic_elasticity.interpolation_options.cached == True
    assert isotropic_elasticity.interpolation_options.normalized == True
    assert isotropic_elasticity.independent_parameters[0].name == "Temperature"
    assert isotropic_elasticity.independent_parameters[0].values.value == [7.88860905221012e-31]
    assert isotropic_elasticity.independent_parameters[0].values.unit == "C"
    assert isotropic_elasticity.independent_parameters[0].upper_limit == 1.18329135783152e-30
    assert isotropic_elasticity.independent_parameters[0].lower_limit == 3.94430452610506e-31
    assert isotropic_elasticity.independent_parameters[0].default_value == 22.0
    assert isotropic_elasticity.youngs_modulus.value == [1000000.0]
    assert isotropic_elasticity.youngs_modulus.unit == "Pa"
    assert isotropic_elasticity.poissons_ratio.value == [0.3]
    assert isotropic_elasticity.poissons_ratio.unit == ""
    material_manager.read_from_mapdl_session(mapdl)
    material = material_manager.get_material("MATERIAL NUMBER 1")
    # TODO: Fix test after updating Mapdl read function
    # isotropic_elasticity = material.models[0]
    # assert isotropic_elasticity.name == "Elasticity"
    # assert isotropic_elasticity.model_qualifiers[0].name == "Behavior"
    # assert isotropic_elasticity.model_qualifiers[0].value == "Isotropic"
