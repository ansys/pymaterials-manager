# Copyright (C) 2022 - 2025 ANSYS, Inc. and/or its affiliates.
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

from ansys.dyna.core import Deck
from ansys.dyna.core import keywords as kwd
from ansys.dyna.core.lib.keyword_base import KeywordBase
import numpy as np

from ansys.materials.manager._models._material_models.density import Density
from ansys.materials.manager._models._material_models.elasticity_anisotropic import (
    ElasticityAnisotropic,
)
from ansys.materials.manager._models._material_models.elasticity_isotropic import (
    ElasticityIsotropic,
)
from ansys.materials.manager._models._material_models.elasticity_orthotropic import (
    ElasticityOrthotropic,
)
from ansys.materials.manager._models.material import Material
from ansys.materials.manager.parsers._common import get_model_attributes, normalize_key
from ansys.materials.manager.parsers.base_visitor import BaseVisitor

from ._ls_dyna_model_map import MATERIAL_MODEL_MAP  # noqa: F401

# most complete needs to go before
MATERIAL_CARD_MAP = {
    normalize_key((Density, ElasticityIsotropic)): kwd.Mat001,
    normalize_key((ElasticityIsotropic,)): kwd.Mat001,
    normalize_key((Density, ElasticityOrthotropic)): kwd.Mat002,
    normalize_key((ElasticityOrthotropic,)): kwd.Mat002,
    normalize_key((Density, ElasticityAnisotropic)): kwd.Mat002Anis,
    normalize_key((ElasticityAnisotropic,)): kwd.Mat002Anis,
}


class LsDynaVisitor(BaseVisitor):
    """Ls Dyna visitor."""

    _material_models_per_material: dict

    def __init__(self, materials: list[Material]):
        """Initialize the ls dyna visitor."""
        super().__init__(materials=materials)
        self._material_models_per_material: dict = {material.name: [] for material in materials}
        self.visit_materials()

    def visit_material_model(self, material_name, material_model):
        """Visit material model."""
        if isinstance(
            material_model,
            (Density, ElasticityIsotropic, ElasticityOrthotropic, ElasticityAnisotropic),
        ):
            model = self._populate_dependent_parameters(material_model)
            self._material_repr[material_name].append(model)
            self._material_models_per_material[material_name].append(material_model.__class__)

    def _to_material_models(self) -> list[KeywordBase]:
        """Bring to material models."""
        instantiated_materials = []
        for material_name, models in self._material_models_per_material.items():
            nrm_key = normalize_key(tuple(models))
            target_cls = MATERIAL_CARD_MAP.get(nrm_key, None)
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

    def write(self, deck: Deck | None = None) -> list[KeywordBase] | None:
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
