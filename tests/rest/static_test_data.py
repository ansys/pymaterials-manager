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

SYNTHETIC_VALUE_SECTION = {
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

# Payload focused on mismatched E/ν temperature grids being accepted.
MIXED_TEMPERATURE_GRIDS_PAYLOAD = {
    "value": r"""
    {
        "materials": [
            {
                "materialName": "Synthetic Alloy A",
                "materialId": "00000000-0000-0000-0000-000000000001",
                "models": [
                    {
                        "modelId": "classification",
                        "constraints": [],
                        "properties": [
                            {
                                "name": "Material state",
                                "stringValue": "Solid"
                            }
                        ]
                    },
                    {
                        "modelId": "density",
                        "constraints": [],
                        "properties": [
                            {
                                "name": "Density",
                                "unit": "kg/m^3",
                                "numericValue": 4430.0
                            }
                        ]
                    },
                    {
                        "modelId": "density.with.temp",
                        "constraints": [],
                        "properties": [
                            {
                                "name": "Density",
                                "columns": [
                                    {
                                        "name": "Density",
                                        "isFreeParameter": false,
                                        "numericValues": [
                                            4454.0,
                                            4450.0,
                                            4445.0
                                        ],
                                        "unit": "kg/m^3"
                                    },
                                    {
                                        "name": "Temperature",
                                        "isFreeParameter": true,
                                        "numericValues": [
                                            -260.0,
                                            -250.0,
                                            -240.0
                                        ],
                                        "unit": "\u00b0C"
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "modelId": "elasticity.isotropic.with.temp",
                        "constraints": [],
                        "properties": [
                            {
                                "name": "Tensile modulus",
                                "columns": [
                                    {
                                        "name": "Tensile modulus",
                                        "isFreeParameter": false,
                                        "numericValues": [
                                            118000000000.0,
                                            117000000000.0
                                        ],
                                        "unit": "Pa"
                                    },
                                    {
                                        "name": "Temperature",
                                        "isFreeParameter": true,
                                        "numericValues": [
                                            -240.0,
                                            -230.0
                                        ],
                                        "unit": "\u00b0C"
                                    }
                                ]
                            },
                            {
                                "name": "Poisson's ratio",
                                "columns": [
                                    {
                                        "name": "Poisson's ratio",
                                        "isFreeParameter": false,
                                        "numericValues": [
                                            0.34,
                                            0.34
                                        ]
                                    },
                                    {
                                        "name": "Temperature",
                                        "isFreeParameter": true,
                                        "numericValues": [
                                            20.0,
                                            30.0
                                        ],
                                        "unit": "\u00b0C"
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "modelId": "tensile.strength.ultimate.with.temp",
                        "constraints": [],
                        "properties": [
                            {
                                "name": "Tensile strength, ultimate",
                                "columns": [
                                    {
                                        "name": "Tensile strength, ultimate",
                                        "isFreeParameter": false,
                                        "numericValues": [
                                            984000000.0
                                        ],
                                        "unit": "Pa"
                                    },
                                    {
                                        "name": "Temperature",
                                        "isFreeParameter": true,
                                        "numericValues": [
                                            20.0
                                        ],
                                        "unit": "\u00b0C"
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "modelId": "tensile.strength.yield.with.temp",
                        "constraints": [],
                        "properties": [
                            {
                                "name": "Tensile strength, yield",
                                "columns": [
                                    {
                                        "name": "Tensile strength, yield",
                                        "isFreeParameter": false,
                                        "numericValues": [
                                            966000000.0
                                        ],
                                        "unit": "Pa"
                                    },
                                    {
                                        "name": "Temperature",
                                        "isFreeParameter": true,
                                        "numericValues": [
                                            20.0
                                        ],
                                        "unit": "\u00b0C"
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
    }
    """,
    "id": 1,
}

# Payload with broad model type coverage: scalar + tabular for all common models,
# plus an unregistered model and a metadata-only model for warning/skip behavior.

BROAD_COVERAGE_PAYLOAD = {
    "value": r"""
    {
        "materials": [
            {
                "materialName": "Synthetic Carbon Steel",
                "materialId": "00000000-0000-0000-0000-000000000002",
                "models": [
                    {
                        "modelId": "classification",
                        "constraints": [],
                        "properties": [
                            {
                                "name": "Material state",
                                "stringValue": "Solid"
                            }
                        ]
                    },
                    {
                        "modelId": "density",
                        "constraints": [],
                        "properties": [
                            {
                                "name": "Density",
                                "unit": "kg/m^3",
                                "numericValue": 7860.0
                            }
                        ]
                    },
                    {
                        "modelId": "density.with.temp",
                        "constraints": [],
                        "properties": [
                            {
                                "name": "Density",
                                "columns": [
                                    {
                                        "name": "Density",
                                        "isFreeParameter": false,
                                        "numericValues": [
                                            7860.0,
                                            7840.0,
                                            7800.0
                                        ],
                                        "unit": "kg/m^3"
                                    },
                                    {
                                        "name": "Temperature",
                                        "isFreeParameter": true,
                                        "numericValues": [
                                            20.0,
                                            100.0,
                                            200.0
                                        ],
                                        "unit": "\u00b0C"
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "modelId": "elasticity.isotropic",
                        "constraints": [],
                        "properties": [
                            {
                                "name": "Tensile modulus",
                                "unit": "Pa",
                                "numericValue": 210000000000.0
                            },
                            {
                                "name": "Poisson's ratio",
                                "numericValue": 0.29
                            }
                        ]
                    },
                    {
                        "modelId": "elasticity.isotropic.with.temp",
                        "constraints": [],
                        "properties": [
                            {
                                "name": "Tensile modulus",
                                "columns": [
                                    {
                                        "name": "Tensile modulus",
                                        "isFreeParameter": false,
                                        "numericValues": [
                                            210000000000.0,
                                            205000000000.0,
                                            198000000000.0
                                        ],
                                        "unit": "Pa"
                                    },
                                    {
                                        "name": "Temperature",
                                        "isFreeParameter": true,
                                        "numericValues": [
                                            20.0,
                                            100.0,
                                            200.0
                                        ],
                                        "unit": "\u00b0C"
                                    }
                                ]
                            },
                            {
                                "name": "Poisson's ratio",
                                "columns": [
                                    {
                                        "name": "Poisson's ratio",
                                        "isFreeParameter": false,
                                        "numericValues": [
                                            0.29,
                                            0.291,
                                            0.292
                                        ]
                                    },
                                    {
                                        "name": "Temperature",
                                        "isFreeParameter": true,
                                        "numericValues": [
                                            20.0,
                                            100.0,
                                            200.0
                                        ],
                                        "unit": "\u00b0C"
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "modelId": "multilinear.hardening",
                        "constraints": [],
                        "properties": [
                            {
                                "name": "True stress with strain",
                                "columns": [
                                    {
                                        "name": "Stress",
                                        "isFreeParameter": false,
                                        "numericValues": [
                                            204267400.0,
                                            215867000.0,
                                            227161500.0,
                                            238158400.0
                                        ],
                                        "unit": "Pa"
                                    },
                                    {
                                        "name": "Strain",
                                        "isFreeParameter": true,
                                        "numericValues": [
                                            0.0,
                                            0.002,
                                            0.004,
                                            0.006
                                        ],
                                        "unit": "strain"
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "modelId": "specific.heat.capacity",
                        "constraints": [],
                        "properties": [
                            {
                                "name": "Specific heat capacity",
                                "unit": "J/kg.\u00b0C",
                                "numericValue": 460.0
                            }
                        ]
                    },
                    {
                        "modelId": "specific.heat.capacity.with.temp",
                        "constraints": [],
                        "properties": [
                            {
                                "name": "Specific heat capacity",
                                "columns": [
                                    {
                                        "name": "Specific heat capacity",
                                        "isFreeParameter": false,
                                        "numericValues": [
                                            460.0,
                                            480.0,
                                            510.0
                                        ],
                                        "unit": "J/kg.\u00b0C"
                                    },
                                    {
                                        "name": "Temperature",
                                        "isFreeParameter": true,
                                        "numericValues": [
                                            20.0,
                                            100.0,
                                            200.0
                                        ],
                                        "unit": "\u00b0C"
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "modelId": "tensile.strength.ultimate.with.temp",
                        "constraints": [],
                        "properties": [
                            {
                                "name": "Tensile strength, ultimate",
                                "columns": [
                                    {
                                        "name": "Tensile strength, ultimate",
                                        "isFreeParameter": false,
                                        "numericValues": [
                                            500000000.0,
                                            480000000.0,
                                            450000000.0
                                        ],
                                        "unit": "Pa"
                                    },
                                    {
                                        "name": "Temperature",
                                        "isFreeParameter": true,
                                        "numericValues": [
                                            20.0,
                                            100.0,
                                            200.0
                                        ],
                                        "unit": "\u00b0C"
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "modelId": "tensile.strength.yield.with.temp",
                        "constraints": [],
                        "properties": [
                            {
                                "name": "Tensile strength, yield",
                                "columns": [
                                    {
                                        "name": "Tensile strength, yield",
                                        "isFreeParameter": false,
                                        "numericValues": [
                                            350000000.0,
                                            330000000.0,
                                            300000000.0
                                        ],
                                        "unit": "Pa"
                                    },
                                    {
                                        "name": "Temperature",
                                        "isFreeParameter": true,
                                        "numericValues": [
                                            20.0,
                                            100.0,
                                            200.0
                                        ],
                                        "unit": "\u00b0C"
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "modelId": "thermal.conductivity",
                        "constraints": [],
                        "properties": [
                            {
                                "name": "Thermal conductivity",
                                "unit": "W/m.\u00b0C",
                                "numericValue": 50.0
                            }
                        ]
                    },
                    {
                        "modelId": "thermal.conductivity.with.temp",
                        "constraints": [],
                        "properties": [
                            {
                                "name": "Thermal conductivity",
                                "columns": [
                                    {
                                        "name": "Thermal conductivity",
                                        "isFreeParameter": false,
                                        "numericValues": [
                                            50.0,
                                            48.0,
                                            44.0
                                        ],
                                        "unit": "W/m.\u00b0C"
                                    },
                                    {
                                        "name": "Temperature",
                                        "isFreeParameter": true,
                                        "numericValues": [
                                            20.0,
                                            100.0,
                                            200.0
                                        ],
                                        "unit": "\u00b0C"
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "modelId": "thermal.expansion.coefficient",
                        "constraints": [],
                        "properties": [
                            {
                                "name": "Thermal expansion coefficient",
                                "unit": "strain/\u00b0C",
                                "numericValue": 1.2e-05
                            }
                        ]
                    },
                    {
                        "modelId": "thermal.expansion.coefficient.with.temp",
                        "constraints": [],
                        "properties": [
                            {
                                "name": "Thermal expansion coefficient",
                                "columns": [
                                    {
                                        "name": "Thermal expansion coefficient",
                                        "isFreeParameter": false,
                                        "numericValues": [
                                            1.1e-05,
                                            1.2e-05,
                                            1.3e-05
                                        ],
                                        "unit": "strain/\u00b0C"
                                    },
                                    {
                                        "name": "Temperature",
                                        "isFreeParameter": true,
                                        "numericValues": [
                                            20.0,
                                            100.0,
                                            200.0
                                        ],
                                        "unit": "\u00b0C"
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
    }
    """,
    "id": 1,
}
TABULAR_ELASTICITY_WITH_TEMPERATURE_MODEL = {
    "modelId": "elasticity.isotropic.with.temp",
    "properties": [
        {
            "name": "Tensile modulus",
            "columns": [
                {
                    "name": "Tensile modulus",
                    "isFreeParameter": False,
                    "unit": "Pa",
                    "numericValues": [2e11, 1.9e11],
                },
                {
                    "name": "Temperature",
                    "isFreeParameter": True,
                    "unit": "\u00b0C",
                    "numericValues": [20.0, 100.0],
                },
            ],
        },
        {
            "name": "Poisson's ratio",
            "columns": [
                {"name": "Poisson's ratio", "isFreeParameter": False, "numericValues": [0.3, 0.31]},
                {
                    "name": "Temperature",
                    "isFreeParameter": True,
                    "unit": "\u00b0C",
                    "numericValues": [20.0, 100.0],
                },
            ],
        },
    ],
}
