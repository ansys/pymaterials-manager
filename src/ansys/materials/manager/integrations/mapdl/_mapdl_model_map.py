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

from ...models import (
    CoefficientofThermalExpansionIsotropic,
    CoefficientofThermalExpansionOrthotropic,
    Density,
    ElasticityAnisotropic,
    ElasticityIsotropic,
    ElasticityOrthotropic,
    HillYieldCriterion,
    IsotropicHardening,
    ThermalConductivityIsotropic,
    ThermalConductivityOrthotropic,
)
from .._common import ModelInfo
from ._mapdl_utils import (
    map_coefficient_of_thermal_expansion_isotropic,
    map_coefficient_of_thermal_expansion_orthotropic,
    map_from_anisotropic_elasticity,
    map_from_hill_yield_criterion,
)

MATERIAL_MODEL_MAP = {
    CoefficientofThermalExpansionIsotropic: ModelInfo(
        method_write=map_coefficient_of_thermal_expansion_isotropic,
    ),
    CoefficientofThermalExpansionOrthotropic: ModelInfo(
        method_write=map_coefficient_of_thermal_expansion_orthotropic
    ),
    Density: ModelInfo(labels=["DENS"], attributes=["density"]),
    ElasticityIsotropic: ModelInfo(
        labels=["EX", "PRXY"], attributes=["youngs_modulus", "poissons_ratio"]
    ),
    ElasticityOrthotropic: ModelInfo(
        labels=[
            "EX",
            "EY",
            "EZ",
            "GXY",
            "GYZ",
            "GXZ",
            "PRXY",
            "PRYZ",
            "PRXZ",
        ],
        attributes=[
            "youngs_modulus_x",
            "youngs_modulus_y",
            "youngs_modulus_z",
            "shear_modulus_xy",
            "shear_modulus_yz",
            "shear_modulus_xz",
            "poissons_ratio_xy",
            "poissons_ratio_yz",
            "poissons_ratio_xz",
        ],
    ),
    ElasticityAnisotropic: ModelInfo(method_write=map_from_anisotropic_elasticity),
    HillYieldCriterion: ModelInfo(
        method_write=map_from_hill_yield_criterion,
    ),
    IsotropicHardening: ModelInfo(
        attributes=["stress"],
    ),
    ThermalConductivityIsotropic: ModelInfo(
        labels=["KXX"],
        attributes=["thermal_conductivity"],
    ),
    ThermalConductivityOrthotropic: ModelInfo(
        labels=[
            "KXX",
            "KYY",
            "KZZ",
        ],
        attributes=[
            "thermal_conductivity_x",
            "thermal_conductivity_y",
            "thermal_conductivity_z",
        ],
    ),
}
