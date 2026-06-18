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
from ansys.materials.manager._models._material_models.compressive_strength import (
    CompressiveStrengthUltimate,
)
from ansys.materials.manager._models._material_models.density import Density
from ansys.materials.manager._models._material_models.elasticity_isotropic import (
    ElasticityIsotropic,
)
from ansys.materials.manager._models._material_models.electrical_resistivity_isotropic import (
    ElectricalResistivityIsotropic,
)
from ansys.materials.manager._models._material_models.specific_heat import SpecificHeat
from ansys.materials.manager._models._material_models.tensile_elongation import TensileElongation
from ansys.materials.manager._models._material_models.tensile_strength import (
    TensileStrengthUltimate,
    TensileStrengthYield,
)
from ansys.materials.manager._models._material_models.thermal_conductivity_isotropic import (
    ThermalConductivityIsotropic,
)
from ansys.materials.manager.parsers._common import ModelInfo
from ansys.materials.manager.parsers.rest._rest_reader import get_tabular_property

MODEL_ID_MAP: dict[str, type] = {}
"""Maps Granta MI ``modelId`` strings to ``MaterialModel`` subclasses in this package."""

MATERIAL_MODEL_MAP: dict = {}
"""Maps ``MaterialModel`` subclasses to :class:`ModelInfo` field descriptors."""

MODEL_ID_INFO_MAP: dict[str, ModelInfo] = {}
"""
Per-model-ID :class:`ModelInfo` overrides.

When a Granta MI ``modelId`` maps to the same ``MaterialModel`` class as another ID (e.g.
``"density"`` and ``"density.with.temp"`` both map to :class:`~.Density`), entries here
take precedence over :data:`MATERIAL_MODEL_MAP` for the specific ID.  This allows tabular
variants to carry their own ``method_read`` without replacing the scalar-variant mapping.
"""


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

# ---------------------------------------------------------------------------
# Tabular (temperature-dependent) model variants
# ---------------------------------------------------------------------------
# These share the same MaterialModel class as their scalar counterparts but
# require a method_read that parses the "columns" array format.  They are
# registered in MODEL_ID_INFO_MAP so the per-ID ModelInfo takes precedence
# over MATERIAL_MODEL_MAP during reading.


def _tabular_reader(*attr_label_pairs: tuple[str, str]):
    """Create a tabular model reader from one or more ``(attribute, label)`` pairs.

    Parameters
    ----------
    *attr_label_pairs : tuple[str, str]
        Each pair maps a model attribute name to its Granta MI property label.

    Returns
    -------
    Callable
        A reader function compatible with :class:`~ModelInfo`'s ``method_read``.
    """
    attributes = tuple(a for a, _ in attr_label_pairs)
    labels = tuple(label for _, label in attr_label_pairs)

    def _read(model_data: dict):
        return (attributes, tuple(get_tabular_property(model_data, label) for label in labels))

    return _read


MODEL_ID_MAP["density.with.temp"] = Density
MODEL_ID_INFO_MAP["density.with.temp"] = ModelInfo(
    method_read=_tabular_reader(("density", "Density"))
)

MODEL_ID_MAP["elasticity.isotropic.with.temp"] = ElasticityIsotropic
MODEL_ID_INFO_MAP["elasticity.isotropic.with.temp"] = ModelInfo(
    method_read=_tabular_reader(
        ("youngs_modulus", "Tensile modulus"),
        ("poissons_ratio", "Poisson's ratio"),
    )
)

MODEL_ID_MAP["tensile.strength.ultimate.with.temp"] = TensileStrengthUltimate
MODEL_ID_INFO_MAP["tensile.strength.ultimate.with.temp"] = ModelInfo(
    method_read=_tabular_reader(("tensile_strength_ultimate", "Tensile strength, ultimate"))
)

MODEL_ID_MAP["tensile.strength.yield.with.temp"] = TensileStrengthYield
MODEL_ID_INFO_MAP["tensile.strength.yield.with.temp"] = ModelInfo(
    method_read=_tabular_reader(("tensile_strength_yield", "Tensile strength, yield"))
)

MODEL_ID_MAP["tensile.strength.ultimate"] = TensileStrengthUltimate
MATERIAL_MODEL_MAP[TensileStrengthUltimate] = ModelInfo(
    labels=["Tensile strength, ultimate"],
    attributes=["tensile_strength_ultimate"],
)

MODEL_ID_MAP["tensile.strength.yield"] = TensileStrengthYield
MATERIAL_MODEL_MAP[TensileStrengthYield] = ModelInfo(
    labels=["Tensile strength, yield"],
    attributes=["tensile_strength_yield"],
)

MODEL_ID_MAP["specific.heat.capacity.with.temp"] = SpecificHeat
MODEL_ID_INFO_MAP["specific.heat.capacity.with.temp"] = ModelInfo(
    method_read=_tabular_reader(("specific_heat", "Specific heat capacity"))
)

MODEL_ID_MAP["thermal.conductivity.with.temp"] = ThermalConductivityIsotropic
MODEL_ID_INFO_MAP["thermal.conductivity.with.temp"] = ModelInfo(
    method_read=_tabular_reader(("thermal_conductivity", "Thermal conductivity"))
)

MODEL_ID_MAP["thermal.expansion.coefficient.with.temp"] = CoefficientofThermalExpansionIsotropic
MODEL_ID_INFO_MAP["thermal.expansion.coefficient.with.temp"] = ModelInfo(
    method_read=_tabular_reader(
        ("coefficient_of_thermal_expansion", "Thermal expansion coefficient")
    )
)


MODEL_ID_MAP["compressive.strength.ultimate"] = CompressiveStrengthUltimate
MATERIAL_MODEL_MAP[CompressiveStrengthUltimate] = ModelInfo(
    labels=["Compressive strength, ultimate"],
    attributes=["compressive_strength_ultimate"],
)

MODEL_ID_MAP["compressive.strength.ultimate.with.temp"] = CompressiveStrengthUltimate
MODEL_ID_INFO_MAP["compressive.strength.ultimate.with.temp"] = ModelInfo(
    method_read=_tabular_reader(("compressive_strength_ultimate", "Compressive strength, ultimate"))
)

MODEL_ID_MAP["tensile.elongation"] = TensileElongation
MATERIAL_MODEL_MAP[TensileElongation] = ModelInfo(
    labels=["Tensile elongation"],
    attributes=["tensile_elongation"],
)

MODEL_ID_MAP["tensile.elongation.with.temp"] = TensileElongation
MODEL_ID_INFO_MAP["tensile.elongation.with.temp"] = ModelInfo(
    method_read=_tabular_reader(("tensile_elongation", "Tensile elongation"))
)

MODEL_ID_MAP["electrical.resistivity"] = ElectricalResistivityIsotropic
MATERIAL_MODEL_MAP[ElectricalResistivityIsotropic] = ModelInfo(
    labels=["Electrical resistivity"],
    attributes=["electrical_resistivity"],
)

MODEL_ID_MAP["electrical.resistivity.with.temp"] = ElectricalResistivityIsotropic
MODEL_ID_INFO_MAP["electrical.resistivity.with.temp"] = ModelInfo(
    method_read=_tabular_reader(("electrical_resistivity", "Electrical resistivity"))
)
