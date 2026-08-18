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

from ansys.materials.manager.models import (
    Density,
    ElasticityIsotropic,
    IndependentParameter,
    TabularQuantity,
)


def _tq(values, temps, unit="Pa", temp_unit="C"):
    """Build a TabularQuantity with a single temperature independent parameter."""
    return TabularQuantity(
        values=Quantity(values, unit),
        independent_parameters=[
            IndependentParameter(name="Temperature", values=Quantity(temps, temp_unit))
        ],
    )


class TestFlattenParameterGridsIntersect:
    def test_overlapping_grids_returns_common_points(self):
        """E on [20, 100, 200], ν on [100, 200, 300] → common grid is [100, 200]."""
        model = ElasticityIsotropic(
            youngs_modulus=_tq([200e9, 190e9, 180e9], [20.0, 100.0, 200.0]),
            poissons_ratio=_tq([0.30, 0.31, 0.32], [100.0, 200.0, 300.0], unit=""),
        )
        result = model.flatten_parameter_grids()

        assert isinstance(result.youngs_modulus, Quantity)
        assert isinstance(result.poissons_ratio, Quantity)
        assert list(result.youngs_modulus.value) == pytest.approx([190e9, 180e9])
        assert list(result.poissons_ratio.value) == pytest.approx([0.30, 0.31])
        assert len(result.independent_parameters) == 1
        assert list(result.independent_parameters[0].values.value) == pytest.approx([100.0, 200.0])

    def test_identical_grids_all_points_preserved(self):
        """When both grids are identical, all points are preserved."""
        model = ElasticityIsotropic(
            youngs_modulus=_tq([200e9, 190e9], [20.0, 100.0]),
            poissons_ratio=_tq([0.30, 0.31], [20.0, 100.0], unit=""),
        )
        result = model.flatten_parameter_grids()

        assert isinstance(result.youngs_modulus, Quantity)
        assert list(result.youngs_modulus.value) == pytest.approx([200e9, 190e9])
        assert list(result.poissons_ratio.value) == pytest.approx([0.30, 0.31])
        assert list(result.independent_parameters[0].values.value) == pytest.approx([20.0, 100.0])

    def test_reversed_grid_ordering_produces_correct_pairing(self):
        """Values must be aligned to the first field's canonical ordering.

        E is at [100, 200] °C; ν is at [200, 100] °C (reversed).  After flattening both
        should be in [100, 200] order and each value must correspond to its correct temperature.
        E(100)=190e9, E(200)=180e9; ν(200)=0.31, ν(100)=0.30.
        """
        model = ElasticityIsotropic(
            youngs_modulus=_tq([190e9, 180e9], [100.0, 200.0]),
            poissons_ratio=_tq([0.31, 0.30], [200.0, 100.0], unit=""),
        )
        result = model.flatten_parameter_grids()

        assert list(result.independent_parameters[0].values.value) == pytest.approx([100.0, 200.0])
        assert list(result.youngs_modulus.value) == pytest.approx([190e9, 180e9])
        # ν(100)=0.30 must appear first, ν(200)=0.31 second
        assert list(result.poissons_ratio.value) == pytest.approx([0.30, 0.31])

    def test_disjoint_grids_raises(self):
        """When grids share no common points, raise ValueError.

        E is defined at temperatures [20, 100, 200] °C; ν is defined at [300, 400, 500] °C.
        The two ranges do not overlap at all, so no common grid point exists.
        """
        model = ElasticityIsotropic(
            youngs_modulus=_tq([200e9, 195e9, 190e9], [20.0, 100.0, 200.0]),
            poissons_ratio=_tq([0.28, 0.29, 0.30], [300.0, 400.0, 500.0], unit=""),
        )
        with pytest.raises(ValueError, match="completely disjoint grids"):
            model.flatten_parameter_grids()

    def test_returns_new_instance_original_unchanged(self):
        """flatten_parameter_grids must not mutate the original model."""
        model = ElasticityIsotropic(
            youngs_modulus=_tq([200e9, 190e9, 180e9], [20.0, 100.0, 200.0]),
            poissons_ratio=_tq([0.30, 0.31, 0.32], [100.0, 200.0, 300.0], unit=""),
        )
        result = model.flatten_parameter_grids()

        assert result is not model
        assert isinstance(model.youngs_modulus, TabularQuantity)
        assert len(model.youngs_modulus.value) == 3
        assert len(model.poissons_ratio.value) == 3


class TestFlattenParameterGridsEdgeCases:
    def test_single_tabular_field_is_demoted(self):
        """Even a single TabularQuantity field is demoted to Quantity + independent_parameters."""
        density_tq = _tq([7800.0, 7750.0], [20.0, 100.0], unit="kg m^-3")
        model = Density(density=density_tq)
        result = model.flatten_parameter_grids()

        assert result is not model
        assert isinstance(result.density, Quantity)
        assert list(result.density.value) == pytest.approx([7800.0, 7750.0])
        assert len(result.independent_parameters) == 1
        assert list(result.independent_parameters[0].values.value) == pytest.approx([20.0, 100.0])

    def test_flattens_all_ips_by_default(self):
        """flatten_parameter_grids with no args should align on all IPs."""
        model = ElasticityIsotropic(
            youngs_modulus=_tq([200e9, 190e9, 180e9], [20.0, 100.0, 200.0]),
            poissons_ratio=_tq([0.30, 0.31, 0.32], [100.0, 200.0, 300.0], unit=""),
        )
        result = model.flatten_parameter_grids()

        assert list(result.youngs_modulus.value) == pytest.approx([190e9, 180e9])
        assert list(result.poissons_ratio.value) == pytest.approx([0.30, 0.31])

    def test_mismatched_ip_names_raises(self):
        """Mismatched IP names across fields should raise ValueError."""
        pressure_ip = IndependentParameter(name="Pressure", values=Quantity([1.0, 2.0], "Pa"))
        model = ElasticityIsotropic(
            youngs_modulus=TabularQuantity(
                values=Quantity([200e9, 190e9], "Pa"),
                independent_parameters=[
                    IndependentParameter(name="Temperature", values=Quantity([20.0, 100.0], "C"))
                ],
            ),
            poissons_ratio=TabularQuantity(
                values=Quantity([0.30, 0.31], ""),
                independent_parameters=[pressure_ip],
            ),
        )
        with pytest.raises(ValueError, match="same independent parameter names"):
            model.flatten_parameter_grids()


class TestTabularQuantityScalarValues:
    def test_scalar_quantity_values_does_not_raise(self):
        """TabularQuantity with a scalar Quantity (float value) should not raise on construction."""
        tq = TabularQuantity(
            values=Quantity(7800.0, "kg m^-3"),
            independent_parameters=[],
        )
        assert tq.values.value == pytest.approx(7800.0)

    def test_scalar_quantity_length_mismatch_raises(self):
        """Scalar Quantity with a non-matching IP should still raise."""
        with pytest.raises(ValueError, match="2 values but dependent quantity has 1"):
            # scalar dependent (n=1) vs IP with 2 values → mismatch
            TabularQuantity(
                values=Quantity(7800.0, "kg m^-3"),
                independent_parameters=[
                    IndependentParameter(name="Temperature", values=Quantity([20.0, 100.0], "C"))
                ],
            )
