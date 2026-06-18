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
