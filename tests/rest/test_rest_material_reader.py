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

import warnings

import pytest

from ansys.materials.manager._models._material_models.density import Density
from ansys.materials.manager._models._material_models.specific_heat import SpecificHeat
from ansys.materials.manager._models._material_models.thermal_conductivity_isotropic import (
    ThermalConductivityIsotropic,
)
from ansys.materials.manager.parsers._common import ModelInfo
from ansys.materials.manager.parsers.rest._rest_model_map import MATERIAL_MODEL_MAP, MODEL_ID_MAP
from ansys.materials.manager.parsers.rest.rest_material_reader import RestMaterialReader


def _minimal_json(name: str = "Steel", material_id: str = "mat-1", models=None) -> dict:
    """Return a minimal JSON structure matching the Granta MI REST schema."""
    return {
        "materials": [
            {
                "materialName": name,
                "materialId": material_id,
                "models": models or [],
            }
        ]
    }


def _density_model_section(density_value: float) -> dict:
    """Return a model section dict for Density matching the Granta MI REST schema."""
    return {
        "modelName": "Density",
        "modelId": "density",
        "properties": [
            {
                "name": "Density",
                "symbol": "rho",
                "unit": "kg/m^3",
                "numericValue": density_value,
            }
        ],
    }


@pytest.fixture(autouse=True)
def _clean_model_maps():
    """Ensure both maps are empty before each test (avoids cross-test pollution)."""
    orig_material = dict(MATERIAL_MODEL_MAP)
    orig_id = dict(MODEL_ID_MAP)
    MATERIAL_MODEL_MAP.clear()
    MODEL_ID_MAP.clear()
    yield
    MATERIAL_MODEL_MAP.clear()
    MATERIAL_MODEL_MAP.update(orig_material)
    MODEL_ID_MAP.clear()
    MODEL_ID_MAP.update(orig_id)


def test_convert_materials_empty_response():
    """convert_materials should return an empty dict when there are no materials."""
    reader = RestMaterialReader({"materials": []})
    assert reader.convert_materials() == {}


def test_convert_materials_reads_material_name():
    """convert_materials should read 'materialName' from the Granta MI schema."""
    raw = _minimal_json(name="Aluminium")
    result = RestMaterialReader(raw).convert_materials()
    assert "Aluminium" in result


def test_convert_materials_reads_material_id():
    """convert_materials should read 'materialId' from the Granta MI schema."""
    raw = _minimal_json(name="Copper", material_id="cu-42")
    result = RestMaterialReader(raw).convert_materials()
    assert result["Copper"].mat_id == "cu-42"


def test_convert_materials_multiple_materials():
    """All materials in the response should be deserialized."""
    raw = {
        "materials": [
            {"materialName": "Mat A", "materialId": "mat-a", "models": []},
            {"materialName": "Mat B", "materialId": "mat-b", "models": []},
        ]
    }
    result = RestMaterialReader(raw).convert_materials()
    assert set(result.keys()) == {"Mat A", "Mat B"}


def test_visit_material_model_dispatches_on_model_id():
    """_iter_model_sections should dispatch on 'modelId' via MODEL_ID_MAP."""
    MODEL_ID_MAP["density"] = Density
    MATERIAL_MODEL_MAP[Density] = ModelInfo(
        labels=["Density"],
        attributes=["density"],
    )
    raw = _minimal_json(models=[_density_model_section(7850.0)])
    result = RestMaterialReader(raw).convert_materials()

    density_model = result["Steel"].get_model_by_name("Density")
    assert density_model is not None
    assert density_model.density.value[0] == pytest.approx(7850.0)
    assert density_model.density.unit == "kg m^-3"


def test_visit_material_model_reads_properties_array():
    """Labels should be matched against the 'name' field in the 'properties' array."""
    MODEL_ID_MAP["density"] = Density
    MATERIAL_MODEL_MAP[Density] = ModelInfo(
        labels=["Density"],
        attributes=["density"],
    )
    raw = _minimal_json(models=[_density_model_section(2700.0)])
    result = RestMaterialReader(raw).convert_materials()
    assert result["Steel"].get_model_by_name("Density").density.value[0] == pytest.approx(2700.0)


def test_visit_material_model_with_method_read():
    """visit_material_model should call method_read when provided."""

    def _read_density(data: dict):
        from ansys.materials.manager.parsers.rest._rest_reader import get_property_with_unit

        value, _unit = get_property_with_unit(data, "Density")
        return ["density"], [value * 2]  # arbitrary transform to prove method_read is called

    MODEL_ID_MAP["density"] = Density
    MATERIAL_MODEL_MAP[Density] = ModelInfo(method_read=_read_density)
    raw = _minimal_json(models=[_density_model_section(1000.0)])
    result = RestMaterialReader(raw).convert_materials()

    density_model = result["Steel"].get_model_by_name("Density")
    assert density_model is not None
    assert density_model.density == pytest.approx(2000.0)  # raw float from method_read


def test_metadata_only_model_ids_are_skipped_silently():
    raw = _minimal_json(
        models=[
            {"modelId": "classification", "modelName": "Classification", "properties": []},
            {"modelId": "description", "modelName": "Description", "properties": []},
            {"modelId": "rendering", "modelName": "Rendering", "properties": []},
        ]
    )
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        result = RestMaterialReader(raw).convert_materials()

    assert len(result["Steel"].models) == 0
    assert len(caught) == 0, f"Unexpected warnings: {[str(w.message) for w in caught]}"


def test_unknown_model_id_emits_logger_warning(caplog):
    import logging

    raw = _minimal_json(
        models=[{"modelId": "b.h.curve", "modelName": "B-H curve", "properties": []}]
    )
    with caplog.at_level(
        logging.WARNING, logger="ansys.materials.manager.parsers.rest.rest_material_reader"
    ):
        RestMaterialReader(raw).convert_materials()

    assert any("b.h.curve" in record.message for record in caplog.records)
    warning_records = [r for r in caplog.records if r.levelno == logging.WARNING]
    assert len(warning_records) == 1


def test_unknown_model_id_does_not_raise():
    raw = _minimal_json(
        models=[{"modelId": "some.future.model", "modelName": "Future Model", "properties": []}]
    )
    result = RestMaterialReader(raw).convert_materials()
    assert "Steel" in result
    assert len(result["Steel"].models) == 0


def test_visit_material_model_warns_when_class_not_in_material_model_map():
    """visit_material_model should warn when the class has no entry in MATERIAL_MODEL_MAP."""
    reader = RestMaterialReader({})
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        result = reader.visit_material_model(Density, {"properties": []})

    assert result is None
    assert any("Density" in str(w.message) for w in caught)


def test_iter_materials_missing_key_yields_nothing():
    """If 'materials' is absent, iteration should yield nothing."""
    result = RestMaterialReader({"data": []}).convert_materials()
    assert result == {}


def test_value_wrapped_response_is_unwrapped():
    """The reader should unwrap the Granta MI 'value' envelope before iterating."""
    import json

    inner = {"materials": [{"materialName": "Steel", "materialId": "s-1", "models": []}]}
    wrapped = {"value": json.dumps(inner), "id": 1}

    result = RestMaterialReader(wrapped).convert_materials()

    assert "Steel" in result
    assert result["Steel"].mat_id == "s-1"


_SYNTHETIC_PAYLOAD = {
    "materials": [
        {
            "materialName": "Test Alloy X-7",
            "materialId": "c0ffee00-0000-4242-beef-123456789abc",
            "databaseKey": "TEST_DB_001",
            "databaseName": "Test Database",
            "tableName": "Test Table",
            "unitSystem": "SI (Consistent)",
            "absoluteUnits": False,
            "exportDateTime": "2000-01-01T00:00:00Z",
            "traceabilityNotes": "Synthetic test data — not from a real server",
            "models": [
                {
                    "modelName": "Classification",
                    "modelId": "classification",
                    "constraints": [],
                    "properties": [
                        {"name": "Material class", "stringValue": "Metal"},
                        {"name": "Material family", "stringValue": "Metal (non-ferrous)"},
                        {"name": "Material sub-class", "stringValue": "Test alloy"},
                        {"name": "Material form", "stringValue": "Bulk material"},
                        {"name": "Material state", "stringValue": "Solid"},
                    ],
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
                            "numericValue": 3210.5,
                        }
                    ],
                },
                {
                    "modelName": "Description",
                    "modelId": "description",
                    "constraints": [],
                    "properties": [
                        {
                            "name": "Description",
                            "stringValue": "Synthetic test alloy for unit tests",
                        }
                    ],
                },
                {
                    "modelName": "Rendering",
                    "modelId": "rendering",
                    "constraints": [],
                    "properties": [
                        {"name": "Red", "symbol": "R", "numericValue": 64},
                        {"name": "Green", "symbol": "G", "numericValue": 128},
                        {"name": "Blue", "symbol": "B", "numericValue": 255},
                        {"name": "Opacity", "numericValue": 1},
                        {"name": "Metallic finish", "boolValue": False},
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
                            "numericValue": 310000000.0,
                        },
                        {
                            "name": "Tensile strength, ultimate",
                            "symbol": "UTS",
                            "unit": "Pa",
                            "numericValue": 480000000.0,
                        },
                        {
                            "name": "Tensile elongation",
                            "symbol": "e",
                            "unit": "strain",
                            "numericValue": 0.15,
                        },
                    ],
                },
                {
                    "modelName": "Specific heat capacity",
                    "modelId": "specific.heat.capacity",
                    "constraints": [],
                    "properties": [
                        {
                            "name": "Specific heat capacity",
                            "symbol": "Cp",
                            "unit": "J/kg.\u00b0C",
                            "numericValue": 875.0,
                        }
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
                            "numericValue": 42.0,
                        }
                    ],
                },
            ],
        }
    ]
}


def test_real_payload_parses_material_name_and_id():
    """The reader should extract material name and ID from the Granta MI payload."""
    result = RestMaterialReader(_SYNTHETIC_PAYLOAD).convert_materials()

    assert "Test Alloy X-7" in result
    assert result["Test Alloy X-7"].mat_id == "c0ffee00-0000-4242-beef-123456789abc"


def test_real_payload_skips_unregistered_models_with_warning(caplog):
    import logging

    with caplog.at_level(
        logging.WARNING,
        logger="ansys.materials.manager.parsers.rest.rest_material_reader",
    ):
        result = RestMaterialReader(_SYNTHETIC_PAYLOAD).convert_materials()

    assert "Test Alloy X-7" in result
    assert result["Test Alloy X-7"].models == []

    warned_ids = {r.message.split("'")[1] for r in caplog.records if r.levelno == logging.WARNING}
    # Physics models with no mapping should have warned
    assert "density" in warned_ids
    # Metadata-only models must NOT have warned
    assert "classification" not in warned_ids
    assert "description" not in warned_ids
    assert "rendering" not in warned_ids


def test_real_payload_density_model():
    """Density should be parsed from the payload when the mapping is registered."""
    MODEL_ID_MAP["density"] = Density
    MATERIAL_MODEL_MAP[Density] = ModelInfo(labels=["Density"], attributes=["density"])

    result = RestMaterialReader(_SYNTHETIC_PAYLOAD).convert_materials()
    density_model = result["Test Alloy X-7"].get_model_by_name("Density")

    assert density_model is not None
    assert density_model.density.value[0] == pytest.approx(3210.5)
    assert density_model.density.unit == "kg m^-3"


def test_real_payload_specific_heat_model():
    """SpecificHeat should be parsed from the payload when the mapping is registered."""
    MODEL_ID_MAP["specific.heat.capacity"] = SpecificHeat
    MATERIAL_MODEL_MAP[SpecificHeat] = ModelInfo(
        labels=["Specific heat capacity"], attributes=["specific_heat"]
    )

    result = RestMaterialReader(_SYNTHETIC_PAYLOAD).convert_materials()
    sh_model = result["Test Alloy X-7"].get_model_by_name("Specific Heat")

    assert sh_model is not None
    assert sh_model.specific_heat.value[0] == pytest.approx(875.0)
    assert sh_model.specific_heat.unit == "J kg^-1 K^-1"


def test_real_payload_thermal_conductivity_model():
    """ThermalConductivityIsotropic should be parsed from the payload when registered."""
    MODEL_ID_MAP["thermal.conductivity"] = ThermalConductivityIsotropic
    MATERIAL_MODEL_MAP[ThermalConductivityIsotropic] = ModelInfo(
        labels=["Thermal conductivity"], attributes=["thermal_conductivity"]
    )

    result = RestMaterialReader(_SYNTHETIC_PAYLOAD).convert_materials()
    tc_model = result["Test Alloy X-7"].get_model_by_name("Thermal Conductivity")

    assert tc_model is not None
    assert tc_model.thermal_conductivity.value[0] == pytest.approx(42.0)
    assert tc_model.thermal_conductivity.unit == "W m^-1 K^-1"


def test_real_payload_multiple_models_registered():
    """All registered models should be populated in a single convert_materials call."""
    MODEL_ID_MAP["density"] = Density
    MATERIAL_MODEL_MAP[Density] = ModelInfo(labels=["Density"], attributes=["density"])
    MODEL_ID_MAP["specific.heat.capacity"] = SpecificHeat
    MATERIAL_MODEL_MAP[SpecificHeat] = ModelInfo(
        labels=["Specific heat capacity"], attributes=["specific_heat"]
    )
    MODEL_ID_MAP["thermal.conductivity"] = ThermalConductivityIsotropic
    MATERIAL_MODEL_MAP[ThermalConductivityIsotropic] = ModelInfo(
        labels=["Thermal conductivity"], attributes=["thermal_conductivity"]
    )

    result = RestMaterialReader(_SYNTHETIC_PAYLOAD).convert_materials()
    mat = result["Test Alloy X-7"]

    assert mat.get_model_by_name("Density") is not None
    assert mat.get_model_by_name("Specific Heat") is not None
    assert mat.get_model_by_name("Thermal Conductivity") is not None
    # Classification / rendering / description / simple.failure are not registered
    assert len(mat.models) == 3


def test_unknown_unit_skips_property_and_warns(caplog):
    """A property whose unit is not in _GRANTA_MI_UNIT_MAP should be skipped with a warning."""
    import logging

    MODEL_ID_MAP["density"] = Density
    MATERIAL_MODEL_MAP[Density] = ModelInfo(labels=["Density"], attributes=["density"])

    raw = _minimal_json(
        models=[
            {
                "modelName": "Density",
                "modelId": "density",
                "properties": [
                    {
                        "name": "Density",
                        "symbol": "rho",
                        "unit": "furlong/fortnight^3",  # not in _GRANTA_MI_UNIT_MAP
                        "numericValue": 1234.0,
                    }
                ],
            }
        ]
    )

    with caplog.at_level(logging.WARNING):
        result = RestMaterialReader(raw).convert_materials()

    # Material is still returned, but the density attribute is not set
    assert "Steel" in result
    density_model = result["Steel"].get_model_by_name("Density")
    assert density_model is not None
    assert density_model.density is None
    assert any("furlong/fortnight^3" in r.message for r in caplog.records)


def test_malformed_value_envelope_raises_granta_mi_error():
    """A 'value' field containing invalid JSON should raise GrantaMIError with a clear message."""
    from ansys.materials.manager.parsers.rest._exceptions import GrantaMIError

    malformed = {"value": "not valid json {[}", "id": 1}

    with pytest.raises(GrantaMIError, match="malformed"):
        RestMaterialReader(malformed).convert_materials()


def test_missing_material_name_raises_granta_mi_error():
    """A material record missing 'materialName' should raise GrantaMIError."""
    import json

    from ansys.materials.manager.parsers.rest._exceptions import GrantaMIError

    raw = {"value": json.dumps({"materials": [{"models": []}]}), "id": 1}

    with pytest.raises(GrantaMIError, match="missing required field"):
        RestMaterialReader(raw).convert_materials()


def test_missing_material_id_raises_granta_mi_error():
    """A material record missing 'materialId' should raise GrantaMIError."""
    import json

    from ansys.materials.manager.parsers.rest._exceptions import GrantaMIError

    raw = {"value": json.dumps({"materials": [{"materialName": "Steel", "models": []}]}), "id": 1}

    with pytest.raises(GrantaMIError, match="missing required field"):
        RestMaterialReader(raw).convert_materials()
