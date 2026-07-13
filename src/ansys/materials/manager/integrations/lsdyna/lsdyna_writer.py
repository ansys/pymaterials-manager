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

# Build writing registry
from typing import Sequence

import numpy as np
from functools import singledispatchmethod

from ..base_visitor import BaseVisitor
from ...models import (
    Density,
    ElasticityAnisotropic,
    ElasticityIsotropic,
    ElasticityOrthotropic,
    Material,
    MaterialModel,
)
from ...models._common import _DynaDeck, _DynaKeywordBase
from .._common import get_model_attributes, normalize_key
from ..material_model_writer_visitor import UnsupportedMaterialModelError
from ._ls_dyna_model_map import MATERIAL_MODEL_MAP

_MATERIAL_CARD_MAP = None


def _get_material_card_map():
    """Return the LS-DYNA material card registry, loading dyna-core on first use."""
    global _MATERIAL_CARD_MAP
    if _MATERIAL_CARD_MAP is None:
        from ansys.dyna.core import keywords as kwd

        _MATERIAL_CARD_MAP = {
            normalize_key((Density, ElasticityIsotropic)): kwd.Mat001,
            normalize_key((ElasticityIsotropic,)): kwd.Mat001,
            normalize_key((Density, ElasticityOrthotropic)): kwd.Mat002,
            normalize_key((ElasticityOrthotropic,)): kwd.Mat002,
            normalize_key((Density, ElasticityAnisotropic)): kwd.Mat002Anis,
            normalize_key((ElasticityAnisotropic,)): kwd.Mat002Anis,
        }
    return _MATERIAL_CARD_MAP


class LsDynaWriter(BaseVisitor):
    """Write materials to LS-DYNA keyword cards via the visitor pattern."""

    _material_models_per_material: dict

    def __init__(self, materials: list[Material]):
        """Initialize the ls dyna writer."""
        super().__init__(materials=materials, model_map=MATERIAL_MODEL_MAP)
        self._material_models_per_material: dict = {material.name: [] for material in materials}
        self.visit_materials()

    @singledispatchmethod
    def visit(self, material_model: MaterialModel, *, material_name: str) -> None:
        """Dispatch LS-DYNA parameter collection by model type."""
        raise UnsupportedMaterialModelError(
            f"{type(self).__name__} has no visit handler for {material_model.__class__.__name__}"
        )

    @visit.register(MaterialModel)
    def _visit_material_model(self, material_model: MaterialModel, *, material_name: str) -> None:
        """Collect per-model parameters for LS-DYNA card composition."""
        model = self._populate_dependent_parameters(material_model)
        self._material_repr[material_name].append(model)
        self._material_models_per_material[material_name].append(material_model.__class__)

    def _to_material_models(self) -> list[_DynaKeywordBase]:
        """Bring to material models."""
        material_card_map = _get_material_card_map()
        instantiated_materials = []
        for material_name, models in self._material_models_per_material.items():
            nrm_key = normalize_key(tuple(models))
            target_cls = material_card_map.get(nrm_key, None)
            if target_cls is None:
                continue
            cls_attributes = get_model_attributes(target_cls)
            mid = self.get_material_id(material_name)
            material_cls = target_cls(mid=mid)
            for model in self._material_repr[material_name]:
                for key in model.keys():
                    if key in cls_attributes:
                        value = model[key].value
                        if isinstance(value, (np.ndarray, Sequence)):
                            value = float(value[0])
                        setattr(material_cls, key, value)
            instantiated_materials.append(material_cls)
        return instantiated_materials

    def write(self, deck: _DynaDeck | None = None) -> list[_DynaKeywordBase] | None:
        """
        Write models to deck.

        Parameters
        ----------
        deck : Deck | None
            Deck to write to. If None, return the material keywords.

        Returns
        -------
        list[KeywordBase] | None
            List of material keywords if deck is None, else None.
        """
        mat_kwds = self._to_material_models()
        if deck:
            deck.extend(mat_kwds)
        else:
            return mat_kwds
