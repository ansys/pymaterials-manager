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

import json

import pytest

from ansys.materials.manager.integrations import RestMaterialReader
from ansys.materials.manager.integrations.rest._rest_model_map import (
    MATERIAL_MODEL_MAP,
    MODEL_ID_MAP,
)
from ansys.materials.manager.models import (
    CoefficientofThermalExpansionIsotropic,
    Density,
    ElasticityIsotropic,
    ElectricalResistivityIsotropic,
    SpecificHeat,
    ThermalConductivityIsotropic,
)

_Z_99_INNER = {
    "materials": [
        {
            "materialName": "Synthetic Alloy Z-99",
            "materialId": "deadbeef-cafe-4321-abcd-000011112222",
            "databaseKey": "MOCK_DATA_SET",
            "models": [
                {
                    "modelName": "Classification",
                    "modelId": "classification",
                    "constraints": [],
                    "properties": [{"name": "Material class", "stringValue": "Metal"}],
                },
                {
                    "modelName": "Density",
                    "modelId": "density",
                    "constraints": [],
                    "properties": [
                        {
                            "name": "Density",
                            "symbol": "rho",
                            "unit": "kg/m^3",
                            "numericValue": 4500.0,
                        }
                    ],
                },
                {
                    "modelName": "Elasticity, isotropic",
                    "modelId": "elasticity.isotropic",
                    "constraints": [],
                    "properties": [
                        {
                            "name": "Tensile modulus",
                            "symbol": "E",
                            "unit": "Pa",
                            "numericValue": 150000000000.0,
                        },
                        {
                            "name": "Poisson's ratio",
                            "symbol": "v",
                            "numericValue": 0.33,
                        },
                    ],
                },
                {
                    "modelName": "Thermal conductivity",
                    "modelId": "thermal.conductivity",
                    "constraints": [],
                    "properties": [
                        {
                            "name": "Thermal conductivity",
                            "symbol": "k",
                            "unit": "W/m.\u00b0C",
                            "numericValue": 38.5,
                        }
                    ],
                },
                {
                    "modelName": "Thermal expansion coefficient",
                    "modelId": "thermal.expansion.coefficient",
                    "constraints": [],
                    "properties": [
                        {
                            "name": "Thermal expansion coefficient",
                            "symbol": "CTE",
                            "unit": "strain/\u00b0C",
                            "numericValue": 8e-6,
                        }
                    ],
                },
                {
                    "modelName": "Simple failure",
                    "modelId": "simple.failure",
                    "constraints": [],
                    "properties": [
                        {
                            "name": "Tensile strength, yield",
                            "symbol": "YS",
                            "unit": "Pa",
                            "numericValue": 250000000.0,
                        }
                    ],
                },
            ],
        }
    ]
}

# Actual wire format from the server: materials JSON is a string inside "value"
_Z_99_PAYLOAD = {"value": json.dumps(_Z_99_INNER), "id": 1}


class TestModelIdMapDefaults:
    """Verify MODEL_ID_MAP is populated with the expected classes at import time."""

    def test_density_registered(self):
        assert MODEL_ID_MAP.get("density") is Density

    def test_specific_heat_registered(self):
        assert MODEL_ID_MAP.get("specific.heat.capacity") is SpecificHeat

    def test_thermal_conductivity_registered(self):
        assert MODEL_ID_MAP.get("thermal.conductivity") is ThermalConductivityIsotropic

    def test_elasticity_isotropic_registered(self):
        assert MODEL_ID_MAP.get("elasticity.isotropic") is ElasticityIsotropic

    def test_cte_isotropic_registered(self):
        assert (
            MODEL_ID_MAP.get("thermal.expansion.coefficient")
            is CoefficientofThermalExpansionIsotropic
        )

    def test_electrical_resistivity_registered(self):
        assert MODEL_ID_MAP.get("electrical.resistivity") is ElectricalResistivityIsotropic

    def test_electrical_resistivity_with_temp_registered(self):
        assert (
            MODEL_ID_MAP.get("electrical.resistivity.with.temp") is ElectricalResistivityIsotropic
        )


class TestMaterialModelMapDefaults:
    """Verify MATERIAL_MODEL_MAP carries correct labels/attributes for each class."""

    def test_density_labels_and_attributes(self):
        info = MATERIAL_MODEL_MAP[Density]
        assert info.labels == ["Density"]
        assert info.attributes == ["density"]

    def test_specific_heat_labels_and_attributes(self):
        info = MATERIAL_MODEL_MAP[SpecificHeat]
        assert info.labels == ["Specific heat capacity"]
        assert info.attributes == ["specific_heat"]

    def test_thermal_conductivity_labels_and_attributes(self):
        info = MATERIAL_MODEL_MAP[ThermalConductivityIsotropic]
        assert info.labels == ["Thermal conductivity"]
        assert info.attributes == ["thermal_conductivity"]

    def test_elasticity_isotropic_labels_and_attributes(self):
        info = MATERIAL_MODEL_MAP[ElasticityIsotropic]
        assert info.labels == ["Tensile modulus", "Poisson's ratio"]
        assert info.attributes == ["youngs_modulus", "poissons_ratio"]

    def test_cte_isotropic_labels_and_attributes(self):
        info = MATERIAL_MODEL_MAP[CoefficientofThermalExpansionIsotropic]
        assert info.labels == ["Thermal expansion coefficient"]
        assert info.attributes == ["coefficient_of_thermal_expansion"]

    def test_electrical_resistivity_labels_and_attributes(self):
        info = MATERIAL_MODEL_MAP[ElectricalResistivityIsotropic]
        assert info.labels == ["Electrical resistivity"]
        assert info.attributes == ["electrical_resistivity"]


class TestEndToEndWithDefaultMaps:
    """Verify the real Granta MI payload is correctly deserialized using default maps."""

    @pytest.fixture(autouse=True)
    def _result(self):
        self.result = RestMaterialReader(_Z_99_PAYLOAD).convert_materials()
        self.mat = self.result["Synthetic Alloy Z-99"]

    def test_value_envelope_unwrapped(self):
        """Reader should unwrap the {'value': '...', 'id': 1} envelope automatically."""
        assert "Synthetic Alloy Z-99" in self.result

    def test_material_id(self):
        assert self.mat.mat_id == "deadbeef-cafe-4321-abcd-000011112222"

    def test_density_model_instantiated(self):
        assert isinstance(self.mat.get_model_by_name("Density"), Density)

    def test_density_value(self):
        assert self.mat.get_model_by_name("Density").density.value[0] == pytest.approx(4500.0)

    def test_density_unit(self):
        assert self.mat.get_model_by_name("Density").density.unit == "kg m^-3"

    def test_elasticity_model_instantiated(self):
        assert isinstance(self.mat.get_model_by_name("Elasticity"), ElasticityIsotropic)

    def test_youngs_modulus_value(self):
        model = self.mat.get_model_by_name("Elasticity")
        assert model.youngs_modulus.value[0] == pytest.approx(150000000000.0)

    def test_youngs_modulus_unit(self):
        assert self.mat.get_model_by_name("Elasticity").youngs_modulus.unit == "Pa"

    def test_poissons_ratio_value(self):
        model = self.mat.get_model_by_name("Elasticity")
        assert model.poissons_ratio.value[0] == pytest.approx(0.33)

    def test_poissons_ratio_dimensionless(self):
        assert self.mat.get_model_by_name("Elasticity").poissons_ratio.unit == ""

    def test_thermal_conductivity_model_instantiated(self):
        assert isinstance(
            self.mat.get_model_by_name("Thermal Conductivity"), ThermalConductivityIsotropic
        )

    def test_thermal_conductivity_value(self):
        model = self.mat.get_model_by_name("Thermal Conductivity")
        assert model.thermal_conductivity.value[0] == pytest.approx(38.5)

    def test_thermal_conductivity_unit(self):
        model = self.mat.get_model_by_name("Thermal Conductivity")
        assert model.thermal_conductivity.unit == "W m^-1 K^-1"

    def test_cte_model_instantiated(self):
        assert isinstance(
            self.mat.get_model_by_name("Coefficient of Thermal Expansion"),
            CoefficientofThermalExpansionIsotropic,
        )

    def test_cte_value(self):
        model = self.mat.get_model_by_name("Coefficient of Thermal Expansion")
        assert model.coefficient_of_thermal_expansion.value[0] == pytest.approx(8e-6)

    def test_cte_unit(self):
        model = self.mat.get_model_by_name("Coefficient of Thermal Expansion")
        assert model.coefficient_of_thermal_expansion.unit == "K^-1"

    def test_unregistered_models_not_present(self):
        """classification and simple.failure should not appear — no mapping registered."""
        model_names = {m.name for m in self.mat.models}
        assert "Classification" not in model_names
        assert "Simple failure" not in model_names

    def test_exactly_four_models_parsed(self):
        """density + elasticity + thermal.conductivity + CTE = 4 registered models."""
        assert len(self.mat.models) == 4
