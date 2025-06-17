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

from ansys.materials.manager._models._common._base import _BaseModel
from ansys.materials.manager._models._common._exceptions import ModelValidationException
from ansys.materials.manager._models._common.constant import Constant
from ansys.materials.manager._models._common.piecewise_linear import PiecewiseLinear
from ansys.materials.manager._models._common.polynomial import Polynomial
from ansys.materials.manager._models._mapdl.anisotropic_elasticity import (
    AnisotropicElasticity,
    ElasticityMode,
)
from ansys.materials.manager._models._material_models.cofficient_of_thermal_expansion_isotropic import (
    CoefficientofThermalExpansionIsotropic,
)
from ansys.materials.manager._models._material_models.cofficient_of_thermal_expansion_orthotropic import (
    CoefficientofThermalExpansionOrthotropic,
)
from ansys.materials.manager._models._material_models.color import (
    Color,
)
from ansys.materials.manager._models._material_models.density import Density
from ansys.materials.manager._models._material_models.elasticity_anisotropic import (
    ElasticityAnisotropic,
)
from ansys.materials.manager._models._material_models.elasticity_isotropic import (
    ElasticityIsotropic,
)
from ansys.materials.manager._models._material_models.elasticity_orthotropic import (
    ElasticityOrthotropic,
)
from ansys.materials.manager._models._material_models.fabric_fiber_angle import (
    FabricFiberAngle,
)
from ansys.materials.manager._models._material_models.fiber_angle import (
    FiberAngle,
)
from ansys.materials.manager._models._material_models.hill_yield_criterion import (
    HillYieldCriterion,
)
from ansys.materials.manager._models._material_models.isotropic_hardening import (
    IsotropicHardening,
)
from ansys.materials.manager._models._material_models.isotropic_hardening_voce_law import (
    IsotropicHardeningVoceLaw,
)
from ansys.materials.manager._models._material_models.kinematic_hardening import (
    KinematicHardening,
)
from ansys.materials.manager._models._material_models.larc03_04_constants import (
    LaRc0304Constants,
)
from ansys.materials.manager._models._material_models.ply_type import (
    PlyType,
)
from ansys.materials.manager._models._material_models.puck_constants import (
    PuckConstants,
)
from ansys.materials.manager._models._material_models.puck_constants_additional import (
    AdditionalPuckConstants,
)
from ansys.materials.manager._models._material_models.specific_heat import (
    SpecificHeat,
)
from ansys.materials.manager._models._material_models.speed_of_sound import (
    SpeedofSound,
)
from ansys.materials.manager._models._material_models.strain_hardening import (
    StrainHardening,
)
from ansys.materials.manager._models._material_models.strain_limits_isotropic import (
    StrainLimitsIsotropic,
)
from ansys.materials.manager._models._material_models.strain_limits_orthotropic import (
    StrainLimitsOrthotropic,
)
from ansys.materials.manager._models._material_models.stress_limits_orthotropic import (
    StressLimitsOrthotropic,
)
from ansys.materials.manager._models._material_models.thermal_conductivity_isotropic import (
    ThermalConductivityIsotropic,
)
from ansys.materials.manager._models._material_models.thermal_conductivity_orthotropic import (
    ThermalConductivityOrthotropic,
)
from ansys.materials.manager._models._material_models.tsai_wu_constants import (
    TsaiWuConstants,
)
from ansys.materials.manager._models._material_models.usermat import (
    ModelCoefficients,
)
from ansys.materials.manager._models._material_models.zero_thermal_strain_reference_temperature_isotropic import (
    ZeroThermalStrainReferenceTemperatureIsotropic,
)
from ansys.materials.manager._models._material_models.zero_thermal_strain_reference_temperature_orthotropic import (
    ZeroThermalStrainReferenceTemperatureOrthotropic,
)
