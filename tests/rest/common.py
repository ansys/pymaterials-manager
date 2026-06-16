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

"""Shared helpers for the REST reader test suite."""

import json as _json


def minimal_json(name: str = "Steel", material_id: str = "mat-1", models=None) -> dict:
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


def density_model_section(density_value: float) -> dict:
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


SYNTHETIC_PAYLOAD = {
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


_TEMPS_3 = [20.0, 100.0, 200.0]


def _col(name, unit, values, is_free):
    col = {"name": name, "isFreeParameter": is_free, "numericValues": values}
    if unit:
        col["unit"] = unit
    return col


def _temp_col(temps):
    return _col("Temperature", "\u00b0C", temps, True)


def _tabular_section(model_id, prop_name, dep_unit, dep_values, temps=None):
    """Build a single-property tabular model section."""
    if temps is None:
        temps = _TEMPS_3
    return {
        "modelId": model_id,
        "constraints": [],
        "properties": [
            {
                "name": prop_name,
                "columns": [
                    _col(prop_name, dep_unit, dep_values, False),
                    _temp_col(temps),
                ],
            }
        ],
    }


def tabular_density_section(temps, densities):
    return _tabular_section("density.with.temp", "Density", "kg/m^3", densities, temps)


def tabular_elasticity_section(temps, e_vals, v_vals):
    return {
        "modelId": "elasticity.isotropic.with.temp",
        "properties": [
            {
                "name": "Tensile modulus",
                "columns": [
                    _col("Tensile modulus", "Pa", e_vals, False),
                    _temp_col(temps),
                ],
            },
            {
                "name": "Poisson's ratio",
                "columns": [
                    _col("Poisson's ratio", None, v_vals, False),
                    _temp_col(temps),
                ],
            },
        ],
    }


# Payload focused on mismatched E/ν temperature grids being accepted.
MIXED_TEMPERATURE_GRIDS_PAYLOAD = {
    "value": _json.dumps(
        {
            "materials": [
                {
                    "materialName": "Synthetic Alloy A",
                    "materialId": "00000000-0000-0000-0000-000000000001",
                    "models": [
                        {
                            "modelId": "classification",
                            "constraints": [],
                            "properties": [{"name": "Material state", "stringValue": "Solid"}],
                        },
                        {
                            "modelId": "density",
                            "constraints": [],
                            "properties": [
                                {"name": "Density", "unit": "kg/m^3", "numericValue": 4430.0}
                            ],
                        },
                        _tabular_section(
                            "density.with.temp",
                            "Density",
                            "kg/m^3",
                            [4454.0, 4450.0, 4445.0],
                            [-260.0, -250.0, -240.0],
                        ),
                        {
                            "modelId": "elasticity.isotropic.with.temp",
                            "constraints": [],
                            "properties": [
                                {
                                    "name": "Tensile modulus",
                                    "columns": [
                                        _col("Tensile modulus", "Pa", [1.18e11, 1.17e11], False),
                                        _temp_col([-240.0, -230.0]),
                                    ],
                                },
                                {
                                    "name": "Poisson's ratio",
                                    "columns": [
                                        _col("Poisson's ratio", None, [0.34, 0.34], False),
                                        _temp_col([20.0, 30.0]),
                                    ],
                                },
                            ],
                        },
                        _tabular_section(
                            "tensile.strength.ultimate.with.temp",
                            "Tensile strength, ultimate",
                            "Pa",
                            [9.84e8],
                            [20.0],
                        ),
                        _tabular_section(
                            "tensile.strength.yield.with.temp",
                            "Tensile strength, yield",
                            "Pa",
                            [9.66e8],
                            [20.0],
                        ),
                    ],
                }
            ]
        }
    ),
    "id": 1,
}

# Payload with broad model type coverage: scalar + tabular for all common models,
# plus an unregistered model and a metadata-only model for warning/skip behavior.
BROAD_COVERAGE_PAYLOAD = {
    "value": _json.dumps(
        {
            "materials": [
                {
                    "materialName": "Synthetic Carbon Steel",
                    "materialId": "00000000-0000-0000-0000-000000000002",
                    "models": [
                        {
                            "modelId": "classification",
                            "constraints": [],
                            "properties": [{"name": "Material state", "stringValue": "Solid"}],
                        },
                        {
                            "modelId": "density",
                            "constraints": [],
                            "properties": [
                                {"name": "Density", "unit": "kg/m^3", "numericValue": 7860.0}
                            ],
                        },
                        _tabular_section(
                            "density.with.temp", "Density", "kg/m^3", [7860.0, 7840.0, 7800.0]
                        ),
                        {
                            "modelId": "elasticity.isotropic",
                            "constraints": [],
                            "properties": [
                                {"name": "Tensile modulus", "unit": "Pa", "numericValue": 210e9},
                                {"name": "Poisson's ratio", "numericValue": 0.29},
                            ],
                        },
                        {
                            "modelId": "elasticity.isotropic.with.temp",
                            "constraints": [],
                            "properties": [
                                {
                                    "name": "Tensile modulus",
                                    "columns": [
                                        _col("Tensile modulus", "Pa", [210e9, 205e9, 198e9], False),
                                        _temp_col(_TEMPS_3),
                                    ],
                                },
                                {
                                    "name": "Poisson's ratio",
                                    "columns": [
                                        _col("Poisson's ratio", None, [0.290, 0.291, 0.292], False),
                                        _temp_col(_TEMPS_3),
                                    ],
                                },
                            ],
                        },
                        {
                            "modelId": "multilinear.hardening",
                            "constraints": [],
                            "properties": [],
                        },
                        {
                            "modelId": "specific.heat.capacity",
                            "constraints": [],
                            "properties": [
                                {
                                    "name": "Specific heat capacity",
                                    "unit": "J/kg.\u00b0C",
                                    "numericValue": 460.0,
                                }
                            ],
                        },
                        _tabular_section(
                            "specific.heat.capacity.with.temp",
                            "Specific heat capacity",
                            "J/kg.\u00b0C",
                            [460.0, 480.0, 510.0],
                        ),
                        _tabular_section(
                            "tensile.strength.ultimate.with.temp",
                            "Tensile strength, ultimate",
                            "Pa",
                            [500e6, 480e6, 450e6],
                        ),
                        _tabular_section(
                            "tensile.strength.yield.with.temp",
                            "Tensile strength, yield",
                            "Pa",
                            [350e6, 330e6, 300e6],
                        ),
                        {
                            "modelId": "thermal.conductivity",
                            "constraints": [],
                            "properties": [
                                {
                                    "name": "Thermal conductivity",
                                    "unit": "W/m.\u00b0C",
                                    "numericValue": 50.0,
                                }
                            ],
                        },
                        _tabular_section(
                            "thermal.conductivity.with.temp",
                            "Thermal conductivity",
                            "W/m.\u00b0C",
                            [50.0, 48.0, 44.0],
                        ),
                        {
                            "modelId": "thermal.expansion.coefficient",
                            "constraints": [],
                            "properties": [
                                {
                                    "name": "Thermal expansion coefficient",
                                    "unit": "strain/\u00b0C",
                                    "numericValue": 12e-6,
                                }
                            ],
                        },
                        _tabular_section(
                            "thermal.expansion.coefficient.with.temp",
                            "Thermal expansion coefficient",
                            "strain/\u00b0C",
                            [11e-6, 12e-6, 13e-6],
                        ),
                    ],
                }
            ]
        }
    ),
    "id": 1,
}
