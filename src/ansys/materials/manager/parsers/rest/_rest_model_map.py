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

from ansys.materials.manager._models._material_models.cofficient_of_thermal_expansion_isotropic import (  # noqa: E501
    CoefficientofThermalExpansionIsotropic,
)
from ansys.materials.manager._models._material_models.density import Density
from ansys.materials.manager._models._material_models.elasticity_isotropic import (
    ElasticityIsotropic,
)
from ansys.materials.manager._models._material_models.specific_heat import SpecificHeat
from ansys.materials.manager._models._material_models.thermal_conductivity_isotropic import (
    ThermalConductivityIsotropic,
)
from ansys.materials.manager.parsers._common import ModelInfo

MODEL_ID_MAP: dict[str, type] = {}
"""Maps Granta MI ``modelId`` strings to ``MaterialModel`` subclasses in this package."""

MATERIAL_MODEL_MAP: dict = {}
"""Maps ``MaterialModel`` subclasses to :class:`ModelInfo` field descriptors."""


MODEL_ID_MAP["density"] = Density
MATERIAL_MODEL_MAP[Density] = ModelInfo(
    labels=["Density"],
    attributes=["density"],
)

MODEL_ID_MAP["specific.heat.capacity"] = SpecificHeat
MATERIAL_MODEL_MAP[SpecificHeat] = ModelInfo(
    labels=["Specific heat capacity"],
    attributes=["specific_heat"],
)

MODEL_ID_MAP["thermal.conductivity"] = ThermalConductivityIsotropic
MATERIAL_MODEL_MAP[ThermalConductivityIsotropic] = ModelInfo(
    labels=["Thermal conductivity"],
    attributes=["thermal_conductivity"],
)

MODEL_ID_MAP["elasticity.isotropic"] = ElasticityIsotropic
MATERIAL_MODEL_MAP[ElasticityIsotropic] = ModelInfo(
    labels=["Tensile modulus", "Poisson's ratio"],
    attributes=["youngs_modulus", "poissons_ratio"],
)

MODEL_ID_MAP["thermal.expansion.coefficient"] = CoefficientofThermalExpansionIsotropic
MATERIAL_MODEL_MAP[CoefficientofThermalExpansionIsotropic] = ModelInfo(
    labels=["Thermal expansion coefficient"],
    attributes=["coefficient_of_thermal_expansion"],
)
