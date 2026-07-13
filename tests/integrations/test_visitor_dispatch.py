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

import logging
import warnings

from ansys.units import Quantity
import pytest

from ansys.materials.manager.integrations._common import ModelInfo
from ansys.materials.manager.integrations.base_visitor import BaseVisitor
from ansys.materials.manager.integrations.material_model_writer_visitor import (
    UnsupportedMaterialModelError,
)
from ansys.materials.manager.models import Density, ElasticityIsotropic, Material, MaterialModel

from .conftest import RecordingVisitor


def test_material_model_accept_delegates_to_visit():
    """MaterialModel.accept should call visitor.visit with material_name."""
    density = Density(density=Quantity(value=[1.0], units="kg m^-3"))
    material = Material(name="steel", models=[density])
    visitor = RecordingVisitor([material], model_map={Density: ModelInfo()})

    density.accept(visitor, material_name="steel")

    assert visitor.recorded == [(Density, "steel")]


def test_material_accept_visits_all_models_in_order():
    """Material.accept should visit each child model."""
    density = Density(density=Quantity(value=[1.0], units="kg m^-3"))
    elasticity = ElasticityIsotropic(
        youngs_modulus=Quantity(value=[2.0e11], units="Pa"),
        poissons_ratio=Quantity(value=[0.3], units=""),
    )
    material = Material(name="alloy", models=[density, elasticity])
    visitor = RecordingVisitor(
        [material],
        model_map={Density: ModelInfo(), ElasticityIsotropic: ModelInfo()},
    )

    material.accept(visitor)

    assert visitor.recorded == [(Density, "alloy"), (ElasticityIsotropic, "alloy")]


def test_singledispatch_picks_specific_handler():
    """visit.register should dispatch by concrete model type."""
    elasticity = ElasticityIsotropic(
        youngs_modulus=Quantity(value=[2.0e11], units="Pa"),
        poissons_ratio=Quantity(value=[0.3], units=""),
    )
    material = Material(name="m", models=[elasticity])
    visitor = RecordingVisitor([material], model_map={ElasticityIsotropic: ModelInfo()})

    elasticity.accept(visitor, material_name="m")

    assert visitor.recorded == [(ElasticityIsotropic, "m")]


def test_unsupported_model_skipped_during_visit_material(caplog):
    """Unsupported models should be skipped with a warning, not raise."""
    density = Density(density=Quantity(value=[1.0], units="kg m^-3"))
    material = Material(name="m", models=[density])
    visitor = RecordingVisitor([material], model_map={})

    with caplog.at_level(logging.WARNING):
        material.accept(visitor)

    assert "Density" in caplog.text
    assert visitor.recorded == []


def test_is_supported_requires_model_map_and_visit_handler():
    """is_supported is False when the map or visit handler is missing."""
    density = Density(density=Quantity(value=[1.0], units="kg m^-3"))
    writer = BaseVisitor([Material(name="m", models=[density])], model_map={Density: ModelInfo()})
    assert writer.is_supported(density) is False

    visitor = RecordingVisitor(
        [Material(name="m", models=[density])],
        model_map={Density: ModelInfo()},
    )
    assert visitor.is_supported(density) is True


def test_visit_material_model_deprecated_shim(capsys):
    """visit_material_model should warn and delegate to accept."""

    class StubWriter(BaseVisitor):
        def visit(self, model: MaterialModel, *, material_name: str) -> None:
            pass

    density = Density(density=Quantity(value=[1.0], units="kg m^-3"))
    material = Material(name="m", models=[density])
    writer = StubWriter([material], model_map={Density: ModelInfo()})

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        writer.visit_material_model("m", density)

    assert any(issubclass(w.category, DeprecationWarning) for w in caught)


def test_base_visitor_visit_raises_without_handler():
    """BaseVisitor.visit should raise when no handler is defined."""
    density = Density(density=Quantity(value=[1.0], units="kg m^-3"))
    writer = BaseVisitor([Material(name="m", models=[density])], model_map={Density: ModelInfo()})

    with pytest.raises(UnsupportedMaterialModelError):
        density.accept(writer, material_name="m")
