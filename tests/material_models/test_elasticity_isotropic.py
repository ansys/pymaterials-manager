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

from ansys.materials.manager._models import (
    ElasticityIsotropic,
)
from ansys.materials.manager._models._common._packages import SupportedPackage
from ansys.materials.manager._models._common.independent_parameter import IndependentParameter


def test_elasticity_isotropic():
    youngs_modulus = [210e9]
    poissons_ratio = [0.3]
    temperature = IndependentParameter(
        name="Temperature", values=[300.0], default_value=293.15, units="K"
    )

    isotropic_elasticity = ElasticityIsotropic(
        youngs_modulus=youngs_modulus,
        poissons_ratio=poissons_ratio,
        independent_parameters=[temperature],
    )

    assert isotropic_elasticity.youngs_modulus == youngs_modulus
    assert isotropic_elasticity.poissons_ratio == poissons_ratio
    assert isotropic_elasticity.independent_parameters == [temperature]
    assert isotropic_elasticity.supported_packages == [SupportedPackage.MAPDL]
    assert isinstance(isotropic_elasticity, ElasticityIsotropic)


def test_elasticity_isotropic_invalid_parameters():
    youngs_modulus = [210e9]
    poissons_ratio = []

    isotropic_elasticity = ElasticityIsotropic(
        youngs_modulus=youngs_modulus, poissons_ratio=poissons_ratio
    )

    is_ok, failures = isotropic_elasticity.validate_model()
    assert not is_ok
    assert failures[0] == "Poisson's ratio value is not defined."

    youngs_modulus = []
    poissons_ratio = [0.3]
    isotropic_elasticity = ElasticityIsotropic(
        youngs_modulus=youngs_modulus, poissons_ratio=poissons_ratio
    )

    is_ok, failures = isotropic_elasticity.validate_model()
    assert not is_ok
    assert failures[0] == "Young's modulus value is not defined."
