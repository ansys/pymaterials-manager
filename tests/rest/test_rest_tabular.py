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
import pytest

from ansys.materials.manager.integrations import RestMaterialReader
from ansys.materials.manager.integrations._common import ModelInfo
from ansys.materials.manager.integrations.rest._rest_model_map import (
    MATERIAL_MODEL_MAP,
    MODEL_ID_INFO_MAP,
    MODEL_ID_MAP,
    _tabular_reader,
)
from ansys.materials.manager.integrations.rest._rest_reader import (
    get_dimensionality,
    get_tabular_property,
)
from ansys.materials.manager.models import (
    Density,
    IsotropicHardening,
    TabularQuantity,
    TensileStrengthUltimate,
    TensileStrengthYield,
)

from .common import (
    minimal_json,
    multilinear_hardening_section,
    tabular_density_section,
)
from .static_test_data import BROAD_COVERAGE_PAYLOAD, TABULAR_ELASTICITY_WITH_TEMPERATURE_MODEL


class TestTabularReader:
    def test_get_dimensionality_scalar(self):
        """Scalar model sections (no columns) have dimensionality 0."""
        section = {"properties": [{"name": "Density", "numericValue": 7800.0}]}
        assert get_dimensionality(section) == 0

    def test_get_dimensionality_tabular(self):
        """Tabular model sections count isFreeParameter columns."""
        section = tabular_density_section([20.0, 100.0], [7800.0, 7750.0])
        assert get_dimensionality(section) == 1

    def test_get_tabular_property_returns_quantity_and_ind_param(self):
        section = tabular_density_section([20.0, 100.0], [7800.0, 7750.0])
        tabular_quantity = get_tabular_property(section, "Density")

        assert tabular_quantity is not None
        assert isinstance(tabular_quantity, TabularQuantity)
        assert list(tabular_quantity.value) == pytest.approx([7800.0, 7750.0])
        assert tabular_quantity.unit == "kg m^-3"
        assert len(tabular_quantity.independent_parameters) == 1
        assert tabular_quantity.independent_parameters[0].name == "Temperature"
        assert list(tabular_quantity.independent_parameters[0].values.value) == pytest.approx(
            [20.0, 100.0]
        )
        assert tabular_quantity.independent_parameters[0].values.unit == "C"

    def test_get_tabular_property_missing_returns_none(self):
        section = {"properties": []}
        tabular_quantity = get_tabular_property(section, "Density")
        assert tabular_quantity is None

    def test_read_density_with_temp(self):
        section = tabular_density_section([20.0, 100.0], [7800.0, 7750.0])
        attrs, values = _tabular_reader(("density", "Density"))(section)
        attr_map = dict(zip(attrs, values))

        density_tq = attr_map["density"]
        assert isinstance(density_tq, TabularQuantity)
        assert list(density_tq.value) == pytest.approx([7800.0, 7750.0])
        assert density_tq.independent_parameters[0].name == "Temperature"

    def test_read_elasticity_isotropic_with_temp(self):
        section = TABULAR_ELASTICITY_WITH_TEMPERATURE_MODEL
        attrs, values = _tabular_reader(
            ("youngs_modulus", "Tensile modulus"),
            ("poissons_ratio", "Poisson's ratio"),
        )(section)
        attr_map = dict(zip(attrs, values))

        assert isinstance(attr_map["youngs_modulus"], TabularQuantity)
        assert isinstance(attr_map["poissons_ratio"], TabularQuantity)
        assert list(attr_map["youngs_modulus"].value) == pytest.approx([2e11, 1.9e11])
        assert list(attr_map["poissons_ratio"].value) == pytest.approx([0.3, 0.31])
        assert attr_map["youngs_modulus"].independent_parameters[0].name == "Temperature"

    def test_read_tensile_strength_ultimate_with_temp(self):
        section = {
            "modelId": "tensile.strength.ultimate.with.temp",
            "properties": [
                {
                    "name": "Tensile strength, ultimate",
                    "columns": [
                        {
                            "name": "Tensile strength, ultimate",
                            "unit": "Pa",
                            "isFreeParameter": False,
                            "numericValues": [1e9],
                        },
                        {
                            "name": "Temperature",
                            "unit": "\u00b0C",
                            "isFreeParameter": True,
                            "numericValues": [20.0],
                        },
                    ],
                }
            ],
        }
        attrs, values = _tabular_reader(
            ("tensile_strength_ultimate", "Tensile strength, ultimate")
        )(section)
        attr_map = dict(zip(attrs, values))
        assert isinstance(attr_map["tensile_strength_ultimate"], TabularQuantity)
        assert list(attr_map["tensile_strength_ultimate"].value) == pytest.approx([1e9])

    def test_read_tensile_strength_yield_with_temp(self):
        section = {
            "modelId": "tensile.strength.yield.with.temp",
            "properties": [
                {
                    "name": "Tensile strength, yield",
                    "columns": [
                        {
                            "name": "Tensile strength, yield",
                            "unit": "Pa",
                            "isFreeParameter": False,
                            "numericValues": [9e8],
                        },
                        {
                            "name": "Temperature",
                            "unit": "\u00b0C",
                            "isFreeParameter": True,
                            "numericValues": [20.0],
                        },
                    ],
                }
            ],
        }
        attrs, values = _tabular_reader(("tensile_strength_yield", "Tensile strength, yield"))(
            section
        )
        attr_map = dict(zip(attrs, values))
        assert isinstance(attr_map["tensile_strength_yield"], TabularQuantity)
        assert list(attr_map["tensile_strength_yield"].value) == pytest.approx([9e8])

    def test_read_specific_heat_with_temp(self):
        section = {
            "modelId": "specific.heat.capacity.with.temp",
            "properties": [
                {
                    "name": "Specific heat capacity",
                    "columns": [
                        {
                            "name": "Specific heat capacity",
                            "unit": "J/kg.\u00b0C",
                            "isFreeParameter": False,
                            "numericValues": [500.0, 520.0],
                        },
                        {
                            "name": "Temperature",
                            "unit": "\u00b0C",
                            "isFreeParameter": True,
                            "numericValues": [20.0, 100.0],
                        },
                    ],
                }
            ],
        }
        attrs, values = _tabular_reader(("specific_heat", "Specific heat capacity"))(section)
        attr_map = dict(zip(attrs, values))
        assert isinstance(attr_map["specific_heat"], TabularQuantity)
        assert list(attr_map["specific_heat"].value) == pytest.approx([500.0, 520.0])
        assert attr_map["specific_heat"].unit == "J kg^-1 K^-1"
        assert attr_map["specific_heat"].independent_parameters[0].name == "Temperature"

    def test_read_thermal_conductivity_with_temp(self):
        section = {
            "modelId": "thermal.conductivity.with.temp",
            "properties": [
                {
                    "name": "Thermal conductivity",
                    "columns": [
                        {
                            "name": "Thermal conductivity",
                            "unit": "W/m.\u00b0C",
                            "isFreeParameter": False,
                            "numericValues": [15.0, 18.0],
                        },
                        {
                            "name": "Temperature",
                            "unit": "\u00b0C",
                            "isFreeParameter": True,
                            "numericValues": [20.0, 100.0],
                        },
                    ],
                }
            ],
        }
        attrs, values = _tabular_reader(("thermal_conductivity", "Thermal conductivity"))(section)
        attr_map = dict(zip(attrs, values))
        assert isinstance(attr_map["thermal_conductivity"], TabularQuantity)
        assert list(attr_map["thermal_conductivity"].value) == pytest.approx([15.0, 18.0])
        assert attr_map["thermal_conductivity"].unit == "W m^-1 K^-1"
        assert attr_map["thermal_conductivity"].independent_parameters[0].name == "Temperature"

    def test_read_thermal_expansion_coefficient_with_temp(self):
        section = {
            "modelId": "thermal.expansion.coefficient.with.temp",
            "properties": [
                {
                    "name": "Thermal expansion coefficient",
                    "columns": [
                        {
                            "name": "Thermal expansion coefficient",
                            "unit": "strain/\u00b0C",
                            "isFreeParameter": False,
                            "numericValues": [1.2e-5, 1.3e-5],
                        },
                        {
                            "name": "Temperature",
                            "unit": "\u00b0C",
                            "isFreeParameter": True,
                            "numericValues": [20.0, 100.0],
                        },
                    ],
                }
            ],
        }
        attrs, values = _tabular_reader(
            ("coefficient_of_thermal_expansion", "Thermal expansion coefficient")
        )(section)
        attr_map = dict(zip(attrs, values))
        assert isinstance(attr_map["coefficient_of_thermal_expansion"], TabularQuantity)
        assert list(attr_map["coefficient_of_thermal_expansion"].value) == pytest.approx(
            [1.2e-5, 1.3e-5]
        )
        assert attr_map["coefficient_of_thermal_expansion"].unit == "K^-1"
        assert (
            attr_map["coefficient_of_thermal_expansion"].independent_parameters[0].name
            == "Temperature"
        )

    def test_read_electrical_resistivity_with_temp(self):
        section = {
            "modelId": "electrical.resistivity.with.temp",
            "properties": [
                {
                    "name": "Electrical resistivity",
                    "columns": [
                        {
                            "name": "Electrical resistivity",
                            "unit": "ohm.m",
                            "isFreeParameter": False,
                            "numericValues": [1.7e-8, 2.1e-8],
                        },
                        {
                            "name": "Temperature",
                            "unit": "\u00b0C",
                            "isFreeParameter": True,
                            "numericValues": [20.0, 100.0],
                        },
                    ],
                }
            ],
        }
        attrs, values = _tabular_reader(("electrical_resistivity", "Electrical resistivity"))(
            section
        )
        attr_map = dict(zip(attrs, values))
        assert isinstance(attr_map["electrical_resistivity"], TabularQuantity)
        assert list(attr_map["electrical_resistivity"].value) == pytest.approx([1.7e-8, 2.1e-8])
        assert attr_map["electrical_resistivity"].unit == "ohm m"
        assert attr_map["electrical_resistivity"].independent_parameters[0].name == "Temperature"


class TestDimensionalityPreference:
    pytestmark = pytest.mark.usefixtures("_clean_model_maps")

    def test_tensile_strength_ultimate_scalar(self):
        """Scalar tensile.strength.ultimate should populate UTS as a Quantity."""
        MODEL_ID_MAP["tensile.strength.ultimate"] = TensileStrengthUltimate
        MATERIAL_MODEL_MAP[TensileStrengthUltimate] = ModelInfo(
            labels=["Tensile strength, ultimate"], attributes=["tensile_strength_ultimate"]
        )

        raw = minimal_json(
            models=[
                {
                    "modelId": "tensile.strength.ultimate",
                    "properties": [
                        {"name": "Tensile strength, ultimate", "unit": "Pa", "numericValue": 480e6}
                    ],
                }
            ]
        )

        result = RestMaterialReader(raw).convert_materials()
        model = result["Steel"].get_model_by_name("Tensile Strength, Ultimate")
        assert model is not None
        assert not isinstance(model.tensile_strength_ultimate, TabularQuantity)
        assert model.tensile_strength_ultimate.value[0] == pytest.approx(480e6)
        assert model.tensile_strength_ultimate.unit == "Pa"

    def test_tensile_strength_yield_scalar(self):
        """Scalar tensile.strength.yield should populate tensile_strength_yield as a Quantity."""
        MODEL_ID_MAP["tensile.strength.yield"] = TensileStrengthYield
        MATERIAL_MODEL_MAP[TensileStrengthYield] = ModelInfo(
            labels=["Tensile strength, yield"], attributes=["tensile_strength_yield"]
        )

        raw = minimal_json(
            models=[
                {
                    "modelId": "tensile.strength.yield",
                    "properties": [
                        {"name": "Tensile strength, yield", "unit": "Pa", "numericValue": 310e6}
                    ],
                }
            ]
        )

        result = RestMaterialReader(raw).convert_materials()
        model = result["Steel"].get_model_by_name("Tensile Strength, Yield")
        assert model is not None
        assert not isinstance(model.tensile_strength_yield, TabularQuantity)
        assert model.tensile_strength_yield.value[0] == pytest.approx(310e6)
        assert model.tensile_strength_yield.unit == "Pa"

    def test_dimensionality_prefers_tabular_over_scalar(self, caplog):
        """When both scalar and tabular sections exist, tabular (higher dim) is selected."""
        import logging

        MODEL_ID_MAP["density"] = Density
        MATERIAL_MODEL_MAP[Density] = ModelInfo(labels=["Density"], attributes=["density"])
        MODEL_ID_MAP["density.with.temp"] = Density
        MODEL_ID_INFO_MAP["density.with.temp"] = ModelInfo(
            method_read=_tabular_reader(("density", "Density"))
        )

        raw = minimal_json(
            models=[
                {
                    "modelId": "density",
                    "properties": [{"name": "Density", "unit": "kg/m^3", "numericValue": 7800.0}],
                },
                tabular_density_section([20.0, 100.0], [7810.0, 7760.0]),
            ]
        )

        with caplog.at_level(
            logging.DEBUG, logger="ansys.materials.manager.integrations.rest.rest_material_reader"
        ):
            result = RestMaterialReader(raw).convert_materials()

        density_model = result["Steel"].get_model_by_name("Density")
        assert density_model is not None
        assert isinstance(density_model.density, TabularQuantity)
        assert len(density_model.density.value) == 2
        assert density_model.independent_parameters is None
        assert density_model.density.independent_parameters[0].name == "Temperature"
        assert any(
            "density.with.temp" in r.message for r in caplog.records if r.levelno == logging.DEBUG
        )

    def test_dimensionality_tie_skips_and_warns(self, caplog):
        """Two model sections with equal dimensionality for the same class should both be skipped"""
        import logging

        MODEL_ID_MAP["density"] = Density
        MATERIAL_MODEL_MAP[Density] = ModelInfo(labels=["Density"], attributes=["density"])
        MODEL_ID_MAP["density.clone"] = Density

        raw = minimal_json(
            models=[
                {
                    "modelId": "density",
                    "properties": [{"name": "Density", "unit": "kg/m^3", "numericValue": 7800.0}],
                },
                {
                    "modelId": "density.clone",
                    "properties": [{"name": "Density", "unit": "kg/m^3", "numericValue": 7900.0}],
                },
            ]
        )

        with caplog.at_level(
            logging.WARNING, logger="ansys.materials.manager.integrations.rest.rest_material_reader"
        ):
            result = RestMaterialReader(raw).convert_materials()

        assert result["Steel"].get_model_by_name("Density") is None
        assert any(
            "equal dimensionality" in r.message
            for r in caplog.records
            if r.levelno == logging.WARNING
        )

    def test_tabular_unknown_unit_skips_and_warns(self, caplog):
        """A tabular property with an unknown unit should be skipped with a warning."""
        import logging

        MODEL_ID_MAP["density.with.temp"] = Density
        MODEL_ID_INFO_MAP["density.with.temp"] = ModelInfo(
            method_read=_tabular_reader(("density", "Density"))
        )

        raw = minimal_json(
            models=[
                {
                    "modelId": "density.with.temp",
                    "properties": [
                        {
                            "name": "Density",
                            "columns": [
                                {
                                    "name": "Density",
                                    "unit": "furlong/fortnight^3",
                                    "isFreeParameter": False,
                                    "numericValues": [1.0],
                                },
                                {
                                    "name": "Temperature",
                                    "unit": "\u00b0C",
                                    "isFreeParameter": True,
                                    "numericValues": [20.0],
                                },
                            ],
                        }
                    ],
                }
            ]
        )

        with caplog.at_level(logging.WARNING):
            result = RestMaterialReader(raw).convert_materials()

        assert "Steel" in result
        assert any(
            "unit" in r.message.lower() for r in caplog.records if r.levelno == logging.WARNING
        )


class TestMultilinearHardening:
    """Tests for the multilinear.hardening → IsotropicHardening mapping."""

    _STRAINS = [0.0, 0.002, 0.004, 0.006]
    _STRESSES = [204267400.0, 215867000.0, 227161500.0, 238158400.0]

    @pytest.fixture
    def section(self):
        return multilinear_hardening_section(self._STRAINS, self._STRESSES)

    def test_tabular_reader_independent_parameter_map(self, section):
        """independent_parameter_map should rename IPs in the returned TabularQuantity."""
        reader = _tabular_reader(
            ("stress", "True stress with strain"),
            independent_parameter_map={"Strain": "Plastic Strain"},
        )
        attrs, values = reader(section)
        tq = dict(zip(attrs, values))[
            "stress"
        ]  # Mirrors how attributes and values are mapped when creating models
        assert isinstance(tq, TabularQuantity)
        assert tq.independent_parameters[0].name == "Plastic Strain"

    def test_tabular_reader_independent_parameter_map_not_provided_preserves_name(self, section):
        """Without independent_parameter_map the original column name should be preserved."""
        reader = _tabular_reader(("stress", "True stress with strain"))
        attrs, values = reader(section)
        tq = dict(zip(attrs, values))["stress"]
        assert tq.independent_parameters[0].name == "Strain"

    @pytest.fixture
    def model(self, section):
        raw = minimal_json(models=[section])
        result = RestMaterialReader(raw).convert_materials()
        return result["Steel"].get_model_by_name("Isotropic Hardening")

    def test_model_is_populated(self, model):
        """The IsotropicHardening model should be present in the material."""
        assert model is not None
        assert isinstance(model, IsotropicHardening)

    def test_stress_is_quantity(self, model):
        """model.stress should be a plain Quantity, not a TabularQuantity."""
        assert isinstance(model.stress, Quantity)
        assert not isinstance(model.stress, TabularQuantity)

    def test_stress_values(self, model):
        """Stress values should match the payload."""
        assert list(model.stress.value) == pytest.approx(self._STRESSES)

    def test_stress_unit(self, model):
        """Stress unit should be Pa."""
        assert model.stress.unit == "Pa"

    def test_plastic_strain_ip_present(self, model):
        """independent_parameters should contain exactly one IP named 'Plastic Strain'."""
        ip_names = [ip.name for ip in model.independent_parameters]
        assert ip_names == ["Plastic Strain"]

    def test_plastic_strain_values(self, model):
        """Plastic strain values should match the payload."""
        ip = model.independent_parameters[0]
        assert list(ip.values.value) == pytest.approx(self._STRAINS)

    def test_broad_coverage_payload_includes_hardening(self):
        """BROAD_COVERAGE_PAYLOAD should produce an IsotropicHardening model."""
        result = RestMaterialReader(BROAD_COVERAGE_PAYLOAD).convert_materials()
        material = result.get("Synthetic Carbon Steel")
        assert material is not None
        model = material.get_model_by_name("Isotropic Hardening")
        assert model is not None
        assert isinstance(model, IsotropicHardening)
        assert isinstance(model.stress, Quantity)
