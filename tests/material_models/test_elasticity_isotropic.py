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

from ansys.units import Quantity

from ansys.materials.manager._models._common import IndependentParameter
from ansys.materials.manager._models._material_models.elasticity_isotropic import (
    ElasticityIsotropic,
)


def test_elasticity_isotropic():
    youngs_modulus = Quantity(value=[210e9], units="Pa")
    poissons_ratio = Quantity(value=[0.3], units="")
    temperature = IndependentParameter(
        name="Temperature", values=Quantity(value=[100.0], units="C"), default_value=293.15
    )

    isotropic_elasticity = ElasticityIsotropic(
        youngs_modulus=youngs_modulus,
        poissons_ratio=poissons_ratio,
        independent_parameters=[temperature],
    )
    assert isinstance(isotropic_elasticity, ElasticityIsotropic)
    assert isotropic_elasticity.youngs_modulus.value.tolist() == youngs_modulus.value.tolist()
    assert isotropic_elasticity.youngs_modulus.units == youngs_modulus.units
    assert isotropic_elasticity.poissons_ratio.value.tolist() == poissons_ratio.value.tolist()
    assert isotropic_elasticity.independent_parameters[0].values.value == [100]
    assert isotropic_elasticity.independent_parameters[0].values.units == temperature.values.units
