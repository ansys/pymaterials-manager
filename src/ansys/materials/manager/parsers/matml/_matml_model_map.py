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

from ansys.materials.manager._models._material_models.cofficient_of_thermal_expansion_isotropic import (  # noqa: E501
    CoefficientofThermalExpansionIsotropic,
)
from ansys.materials.manager._models._material_models.cofficient_of_thermal_expansion_orthotropic import (  # noqa: E501
    CoefficientofThermalExpansionOrthotropic,
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
from ansys.materials.manager._models._material_models.fabric_fiber_angle import FabricFiberAngle
from ansys.materials.manager._models._material_models.fiber_angle import FiberAngle
from ansys.materials.manager._models._material_models.hill_yield_criterion import HillYieldCriterion
from ansys.materials.manager._models._material_models.isotropic_hardening import IsotropicHardening
from ansys.materials.manager._models._material_models.isotropic_hardening_voce_law import (
    IsotropicHardeningVoceLaw,
)
from ansys.materials.manager._models._material_models.kinematic_hardening import KinematicHardening
from ansys.materials.manager._models._material_models.larc03_04_constants import LaRc0304Constants
from ansys.materials.manager._models._material_models.molecular_weight import MolecularWeight
from ansys.materials.manager._models._material_models.ply_type import PlyType
from ansys.materials.manager._models._material_models.puck_constants import PuckConstants
from ansys.materials.manager._models._material_models.puck_constants_additional import (
    AdditionalPuckConstants,
)
from ansys.materials.manager._models._material_models.specific_heat import SpecificHeat
from ansys.materials.manager._models._material_models.speed_of_sound import SpeedofSound
from ansys.materials.manager._models._material_models.strain_hardening import StrainHardening
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
from ansys.materials.manager._models._material_models.tsai_wu_constants import TsaiWuConstants
from ansys.materials.manager._models._material_models.usermat import ModelCoefficients
from ansys.materials.manager._models._material_models.viscosity import Viscosity
from ansys.materials.manager._models._material_models.zero_thermal_strain_reference_temperature_isotropic import (  # noqa: E501
    ZeroThermalStrainReferenceTemperatureIsotropic,
)
from ansys.materials.manager._models._material_models.zero_thermal_strain_reference_temperature_orthotropic import (  # noqa: E501
    ZeroThermalStrainReferenceTemperatureOrthotropic,
)
from ansys.materials.manager.parsers._common import ModelInfo
from ansys.materials.manager.parsers.matml._matml_utils import (
    map_from_anisotropic_elasticity,
    map_from_hill_yield_criterion,
    map_to_anisotropic_elasticity,
    map_to_hill_yield_criterion,
    map_to_model_coefficients,
)

MATERIAL_MODEL_MAP = {
    CoefficientofThermalExpansionIsotropic: ModelInfo(
        labels=["Coefficient of Thermal Expansion"],
        attributes=["coefficient_of_thermal_expansion"],
    ),
    CoefficientofThermalExpansionOrthotropic: ModelInfo(
        labels=[
            "Coefficient of Thermal Expansion X direction",
            "Coefficient of Thermal Expansion Y direction",
            "Coefficient of Thermal Expansion Z direction",
        ],
        attributes=[
            "coefficient_of_thermal_expansion_x",
            "coefficient_of_thermal_expansion_y",
            "coefficient_of_thermal_expansion_z",
        ],
    ),
    Density: ModelInfo(labels=["Density"], attributes=["density"]),
    ElasticityIsotropic: ModelInfo(
        labels=["Young's Modulus", "Poisson's Ratio"],
        attributes=["youngs_modulus", "poissons_ratio"],
    ),
    ElasticityOrthotropic: ModelInfo(
        labels=[
            "Young's Modulus X direction",
            "Young's Modulus Y direction",
            "Young's Modulus Z direction",
            "Shear Modulus XY",
            "Shear Modulus YZ",
            "Shear Modulus XZ",
            "Poisson's Ratio XY",
            "Poisson's Ratio YZ",
            "Poisson's Ratio XZ",
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
    ElasticityAnisotropic: ModelInfo(
        method_write=map_from_anisotropic_elasticity,
        method_read=map_to_anisotropic_elasticity,
    ),
    FabricFiberAngle: ModelInfo(
        labels=["Fabric Fiber Angle"],
        attributes=["fabric_fiber_angle"],
    ),
    FiberAngle: ModelInfo(),
    HillYieldCriterion: ModelInfo(
        method_write=map_from_hill_yield_criterion,
        method_read=map_to_hill_yield_criterion,
    ),
    IsotropicHardeningVoceLaw: ModelInfo(
        labels=[
            "Initial Yield Stress",
            "Linear Coefficient",
            "Exponential Coefficient",
            "Exponential Saturation Parameter",
        ],
        attributes=[
            "initial_yield_stress",
            "linear_coefficient",
            "exponential_coefficient",
            "exponential_saturation_parameter",
        ],
    ),
    IsotropicHardening: ModelInfo(
        labels=["Stress"],
        attributes=["stress"],
    ),
    KinematicHardening: ModelInfo(
        labels=[
            "Yield Stress",
            "Material Constant γ1",
            "Material Constant C1",
            "Material Constant γ2",
            "Material Constant C2",
            "Material Constant γ3",
            "Material Constant C3",
            "Material Constant γ4",
            "Material Constant C4",
            "Material Constant γ5",
            "Material Constant C5",
        ],
        attributes=[
            "yield_stress",
            "material_constant_gamma_1",
            "material_constant_c_1",
            "material_constant_gamma_2",
            "material_constant_c_2",
            "material_constant_gamma_3",
            "material_constant_c_3",
            "material_constant_gamma_4",
            "material_constant_c_4",
            "material_constant_gamma_5",
            "material_constant_c_5",
        ],
    ),
    LaRc0304Constants: ModelInfo(
        labels=[
            "Fracture Toughness Ratio",
            "Longitudinal Friction Coefficient",
            "Transverse Friction Coefficient",
            "Fracture Angle Under Compression",
        ],
        attributes=[
            "fracture_toughness_ratio",
            "longitudinal_friction_coefficient",
            "transverse_friction_coefficient",
            "fracture_angle_under_compression",
        ],
    ),
    ModelCoefficients: ModelInfo(
        method_read=map_to_model_coefficients,
    ),
    MolecularWeight: ModelInfo(
        labels=["Molecular Weight"],
        attributes=["molecular_weight"],
    ),
    PlyType: ModelInfo(),
    PuckConstants: ModelInfo(
        labels=[
            "Compressive Inclination XZ",
            "Compressive Inclination YZ",
            "Tensile Inclination XZ",
            "Tensile Inclination YZ",
        ],
        attributes=[
            "compressive_inclination_xz",
            "compressive_inclination_yz",
            "tensile_inclination_xz",
            "tensile_inclination_yz",
        ],
    ),
    AdditionalPuckConstants: ModelInfo(
        labels=[
            "Interface Weakening Factor",
            "Degradation Parameter s",
            "Degradation Parameter M",
        ],
        attributes=[
            "interface_weakening_factor",
            "degradation_parameter_s",
            "degradation_parameter_m",
        ],
    ),
    SpecificHeat: ModelInfo(
        labels=["Specific Heat"],
        attributes=["specific_heat"],
    ),
    SpeedofSound: ModelInfo(
        labels=["Speed of Sound"],
        attributes=["speed_of_sound"],
    ),
    StrainHardening: ModelInfo(
        labels=["Creep Constant 1", "Creep Constant 2", "Creep Constant 3", "Creep Constant 4"],
        attributes=["creep_constant_1", "creep_constant_2", "creep_constant_3", "creep_constant_4"],
    ),
    StrainLimitsIsotropic: ModelInfo(
        labels=["Von Mises "],
        attributes=["von_mises"],
    ),
    StrainLimitsOrthotropic: ModelInfo(
        labels=[
            "Tensile X direction",
            "Tensile Y direction",
            "Tensile Z direction",
            "Compressive X direction",
            "Compressive Y direction",
            "Compressive Z direction",
            "Shear XY",
            "Shear XZ",
            "Shear YZ",
        ],
        attributes=[
            "tensile_x_direction",
            "tensile_y_direction",
            "tensile_z_direction",
            "compressive_x_direction",
            "compressive_y_direction",
            "compressive_z_direction",
            "shear_xy",
            "shear_xz",
            "shear_yz",
        ],
    ),
    StressLimitsOrthotropic: ModelInfo(
        labels=[
            "Tensile X direction",
            "Tensile Y direction",
            "Tensile Z direction",
            "Compressive X direction",
            "Compressive Y direction",
            "Compressive Z direction",
            "Shear XY",
            "Shear YZ",
            "Shear XZ",
        ],
        attributes=[
            "tensile_x_direction",
            "tensile_y_direction",
            "tensile_z_direction",
            "compressive_x_direction",
            "compressive_y_direction",
            "compressive_z_direction",
            "shear_xy",
            "shear_yz",
            "shear_xz",
        ],
    ),
    ThermalConductivityIsotropic: ModelInfo(
        labels=["Thermal Conductivity"],
        attributes=["thermal_conductivity"],
    ),
    ThermalConductivityOrthotropic: ModelInfo(
        labels=[
            "Thermal Conductivity X direction",
            "Thermal Conductivity Y direction",
            "Thermal Conductivity Z direction",
        ],
        attributes=[
            "thermal_conductivity_x",
            "thermal_conductivity_y",
            "thermal_conductivity_z",
        ],
    ),
    TsaiWuConstants: ModelInfo(
        labels=[
            "Coupling Coefficient XY",
            "Coupling Coefficient XZ",
            "Coupling Coefficient YZ",
        ],
        attributes=[
            "coupling_coefficient_xy",
            "coupling_coefficient_xz",
            "coupling_coefficient_yz",
        ],
    ),
    Viscosity: ModelInfo(
        labels=["Viscosity"],
        attributes=["viscosity"],
    ),
    ZeroThermalStrainReferenceTemperatureIsotropic: ModelInfo(
        labels=["Zero-Thermal-Strain Reference Temperature"],
        attributes=["zero_thermal_strain_reference_temperature"],
    ),
    ZeroThermalStrainReferenceTemperatureOrthotropic: ModelInfo(
        labels=["Zero-Thermal-Strain Reference Temperature"],
        attributes=["zero_thermal_strain_reference_temperature"],
    ),
}
