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

"""Shared fixtures for integration visitor tests."""

from functools import singledispatchmethod

from ansys.units import Quantity
import pytest

from ansys.materials.manager.integrations._common import ModelInfo
from ansys.materials.manager.integrations.base_visitor import BaseVisitor
from ansys.materials.manager.integrations.material_model_writer_visitor import (
    UnsupportedMaterialModelError,
)
from ansys.materials.manager.models import Density, ElasticityIsotropic, Material, MaterialModel


class RecordingVisitor(BaseVisitor):
    """Minimal visitor that records (type, material_name) pairs for dispatch tests."""

    def __init__(self, materials: list[Material], model_map: dict | None = None):
        if model_map is None:
            model_map = {Density: ModelInfo()}
        super().__init__(materials, model_map=model_map)
        self.recorded: list[tuple[type, str]] = []

    @singledispatchmethod
    def visit(self, model: MaterialModel, *, material_name: str) -> None:
        raise UnsupportedMaterialModelError(
            f"{type(self).__name__} has no visit handler for {model.__class__.__name__}"
        )

    @visit.register(MaterialModel)
    def _visit_model(self, model: MaterialModel, *, material_name: str) -> None:
        self.recorded.append((type(model), material_name))

    @visit.register(ElasticityIsotropic)
    def _visit_elasticity(self, model: ElasticityIsotropic, *, material_name: str) -> None:
        self.recorded.append((ElasticityIsotropic, material_name))


@pytest.fixture
def material_with():
    """Factory fixture for building materials with a single model."""

    def _factory(model: MaterialModel, name: str = "test", material_id: int = 1) -> Material:
        return Material(name=name, material_id=material_id, models=[model])

    return _factory


@pytest.fixture
def minimal_model_factory():
    """Build minimal valid instances for map-coverage smoke tests."""

    def _factory(model_cls: type[MaterialModel]) -> MaterialModel | None:
        if model_cls is Density:
            return Density(density=Quantity(value=[1.0], units="kg m^-3"))
        if model_cls is ElasticityIsotropic:
            return ElasticityIsotropic(
                youngs_modulus=Quantity(value=[2.0e11], units="Pa"),
                poissons_ratio=Quantity(value=[0.3], units=""),
            )
        return None

    return _factory
