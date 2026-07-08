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

import pytest

from ansys.materials.manager.integrations import RestMaterialReader
from ansys.materials.manager.integrations._common import ModelInfo
from ansys.materials.manager.integrations.rest._rest_model_map import (
    MATERIAL_MODEL_MAP,
    MODEL_ID_INFO_MAP,
    MODEL_ID_MAP,
    _tabular_reader,
)
from ansys.materials.manager.models import (
    CoefficientofThermalExpansionIsotropic,
    Density,
    ElasticityIsotropic,
    SpecificHeat,
    TabularQuantity,
    TensileStrengthUltimate,
    TensileStrengthYield,
    ThermalConductivityIsotropic,
)

from .static_test_data import BROAD_COVERAGE_PAYLOAD, MIXED_TEMPERATURE_GRIDS_PAYLOAD


def _register_all_tabular_models():
    """Register all scalar and tabular model mappings used by integration tests."""
    MODEL_ID_MAP["density"] = Density
    MATERIAL_MODEL_MAP[Density] = ModelInfo(labels=["Density"], attributes=["density"])
    MODEL_ID_MAP["density.with.temp"] = Density
    MODEL_ID_INFO_MAP["density.with.temp"] = ModelInfo(
        method_read=_tabular_reader(("density", "Density"))
    )

    MODEL_ID_MAP["elasticity.isotropic"] = ElasticityIsotropic
    MATERIAL_MODEL_MAP[ElasticityIsotropic] = ModelInfo(
        labels=["Tensile modulus", "Poisson's ratio"],
        attributes=["youngs_modulus", "poissons_ratio"],
    )
    MODEL_ID_MAP["elasticity.isotropic.with.temp"] = ElasticityIsotropic
    MODEL_ID_INFO_MAP["elasticity.isotropic.with.temp"] = ModelInfo(
        method_read=_tabular_reader(
            ("youngs_modulus", "Tensile modulus"),
            ("poissons_ratio", "Poisson's ratio"),
        )
    )

    MODEL_ID_MAP["specific.heat.capacity"] = SpecificHeat
    MATERIAL_MODEL_MAP[SpecificHeat] = ModelInfo(
        labels=["Specific heat capacity"], attributes=["specific_heat"]
    )
    MODEL_ID_MAP["specific.heat.capacity.with.temp"] = SpecificHeat
    MODEL_ID_INFO_MAP["specific.heat.capacity.with.temp"] = ModelInfo(
        method_read=_tabular_reader(("specific_heat", "Specific heat capacity"))
    )

    MODEL_ID_MAP["tensile.strength.ultimate.with.temp"] = TensileStrengthUltimate
    MODEL_ID_INFO_MAP["tensile.strength.ultimate.with.temp"] = ModelInfo(
        method_read=_tabular_reader(("tensile_strength_ultimate", "Tensile strength, ultimate"))
    )
    MATERIAL_MODEL_MAP[TensileStrengthUltimate] = ModelInfo(
        labels=["Tensile strength, ultimate"], attributes=["tensile_strength_ultimate"]
    )

    MODEL_ID_MAP["tensile.strength.yield.with.temp"] = TensileStrengthYield
    MODEL_ID_INFO_MAP["tensile.strength.yield.with.temp"] = ModelInfo(
        method_read=_tabular_reader(("tensile_strength_yield", "Tensile strength, yield"))
    )
    MATERIAL_MODEL_MAP[TensileStrengthYield] = ModelInfo(
        labels=["Tensile strength, yield"], attributes=["tensile_strength_yield"]
    )

    MODEL_ID_MAP["thermal.conductivity"] = ThermalConductivityIsotropic
    MATERIAL_MODEL_MAP[ThermalConductivityIsotropic] = ModelInfo(
        labels=["Thermal conductivity"], attributes=["thermal_conductivity"]
    )
    MODEL_ID_MAP["thermal.conductivity.with.temp"] = ThermalConductivityIsotropic
    MODEL_ID_INFO_MAP["thermal.conductivity.with.temp"] = ModelInfo(
        method_read=_tabular_reader(("thermal_conductivity", "Thermal conductivity"))
    )

    MODEL_ID_MAP["thermal.expansion.coefficient"] = CoefficientofThermalExpansionIsotropic
    MATERIAL_MODEL_MAP[CoefficientofThermalExpansionIsotropic] = ModelInfo(
        labels=["Thermal expansion coefficient"],
        attributes=["coefficient_of_thermal_expansion"],
    )
    MODEL_ID_MAP["thermal.expansion.coefficient.with.temp"] = CoefficientofThermalExpansionIsotropic
    MODEL_ID_INFO_MAP["thermal.expansion.coefficient.with.temp"] = ModelInfo(
        method_read=_tabular_reader(
            ("coefficient_of_thermal_expansion", "Thermal expansion coefficient")
        )
    )


class TestIntegration:
    pytestmark = pytest.mark.usefixtures("_clean_model_maps")

    def test_mixed_temperature_grid_payload_parses(self):
        """Tabular models with mismatched E/ν temperature grids are accepted."""
        _register_all_tabular_models()

        result = RestMaterialReader(MIXED_TEMPERATURE_GRIDS_PAYLOAD).convert_materials()
        mat = result["Synthetic Alloy A"]

        density_model = mat.get_model_by_name("Density")
        assert density_model is not None
        assert isinstance(density_model.density, TabularQuantity)
        assert len(density_model.density.value) == 3
        assert density_model.density.independent_parameters[0].name == "Temperature"

        e_model = mat.get_model_by_name("Elasticity")
        assert e_model is not None
        assert isinstance(e_model.youngs_modulus, TabularQuantity)
        assert isinstance(e_model.poissons_ratio, TabularQuantity)

        uts_model = mat.get_model_by_name("Tensile Strength, Ultimate")
        assert uts_model is not None
        assert isinstance(uts_model.tensile_strength_ultimate, TabularQuantity)
        assert list(uts_model.tensile_strength_ultimate.value) == pytest.approx([9.84e8])

        ys_model = mat.get_model_by_name("Tensile Strength, Yield")
        assert ys_model is not None
        assert isinstance(ys_model.tensile_strength_yield, TabularQuantity)
        assert list(ys_model.tensile_strength_yield.value) == pytest.approx([9.66e8])

    def test_carbon_steel_payload_full_integration(self, caplog):
        """Broad model coverage, dimensionality preference, and warning behavior."""
        import logging

        _register_all_tabular_models()

        with caplog.at_level(
            logging.WARNING,
            logger="ansys.materials.manager.integrations.rest.rest_material_reader",
        ):
            result = RestMaterialReader(BROAD_COVERAGE_PAYLOAD).convert_materials()

        assert "Synthetic Carbon Steel" in result
        mat = result["Synthetic Carbon Steel"]
        assert mat.mat_id == "00000000-0000-0000-0000-000000000002"

        density_model = mat.get_model_by_name("Density")
        assert density_model is not None
        assert isinstance(density_model.density, TabularQuantity)
        assert list(density_model.density.value) == pytest.approx([7860.0, 7840.0, 7800.0])
        assert density_model.density.independent_parameters[0].name == "Temperature"

        e_model = mat.get_model_by_name("Elasticity")
        assert e_model is not None
        assert isinstance(e_model.youngs_modulus, TabularQuantity)
        assert isinstance(e_model.poissons_ratio, TabularQuantity)
        assert list(e_model.youngs_modulus.value) == pytest.approx([210e9, 205e9, 198e9])
        assert list(e_model.poissons_ratio.value) == pytest.approx([0.290, 0.291, 0.292])
        assert len(e_model.youngs_modulus.value) == len(e_model.poissons_ratio.value)

        sh_model = mat.get_model_by_name("Specific Heat")
        assert sh_model is not None
        assert isinstance(sh_model.specific_heat, TabularQuantity)
        assert list(sh_model.specific_heat.value) == pytest.approx([460.0, 480.0, 510.0])

        uts_model = mat.get_model_by_name("Tensile Strength, Ultimate")
        assert uts_model is not None
        assert isinstance(uts_model.tensile_strength_ultimate, TabularQuantity)
        assert list(uts_model.tensile_strength_ultimate.value) == pytest.approx(
            [500e6, 480e6, 450e6]
        )

        ys_model = mat.get_model_by_name("Tensile Strength, Yield")
        assert ys_model is not None
        assert isinstance(ys_model.tensile_strength_yield, TabularQuantity)
        assert list(ys_model.tensile_strength_yield.value) == pytest.approx([350e6, 330e6, 300e6])

        tc_model = mat.get_model_by_name("Thermal Conductivity")
        assert tc_model is not None
        assert isinstance(tc_model.thermal_conductivity, TabularQuantity)
        assert list(tc_model.thermal_conductivity.value) == pytest.approx([50.0, 48.0, 44.0])

        cte_model = mat.get_model_by_name("Coefficient of Thermal Expansion")
        assert cte_model is not None
        assert isinstance(cte_model.coefficient_of_thermal_expansion, TabularQuantity)
        assert list(cte_model.coefficient_of_thermal_expansion.value) == pytest.approx(
            [11e-6, 12e-6, 13e-6]
        )

        warned_ids = {
            r.message.split("'")[1] for r in caplog.records if r.levelno == logging.WARNING
        }
        assert "multilinear.hardening" in warned_ids
        assert "classification" not in warned_ids
