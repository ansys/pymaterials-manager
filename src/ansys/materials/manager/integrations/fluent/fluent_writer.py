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

from functools import singledispatchmethod

from ...models import Material, MaterialModel
from ..base_visitor import BaseVisitor
from ..material_model_writer_visitor import UnsupportedMaterialModelError
from ._fluent_model_map import MATERIAL_MODEL_MAP


class FluentWriter(BaseVisitor):
    """Write materials to Fluent solver representation via the visitor pattern."""

    def __init__(self, materials: list[Material]):
        """Initialize the fluent writer."""
        super().__init__(materials=materials, model_map=MATERIAL_MODEL_MAP)
        self.visit_materials()

    def _standard_write(self, material_model: MaterialModel) -> dict:
        """Write standard models."""
        dependent_parameters = self._populate_dependent_parameters(material_model)
        model = {}
        for label in dependent_parameters.keys():
            value = dependent_parameters[label].value[0]
            new_model = {label: {"option": "constant", "value": float(value)}}
            model.update(new_model)
        return model

    @singledispatchmethod
    def visit(self, material_model: MaterialModel, *, material_name: str) -> None:
        """Dispatch Fluent serialization by model type."""
        raise UnsupportedMaterialModelError(
            f"{type(self).__name__} has no visit handler for {material_model.__class__.__name__}"
        )

    @visit.register(MaterialModel)
    def _visit_material_model(self, material_model: MaterialModel, *, material_name: str) -> None:
        """Visit supported Fluent material models."""
        model = self._standard_write(material_model)
        self._material_repr[material_name].append(model)

    def write(self, material_names: list[str] | None = None) -> list[dict]:
        """
        Write fluent representation.

        Parameters
        ----------
        material_names : list[str] | None
            List of material names to write. If None, write all materials.

        Returns
        -------
        list[dict]
            List of material representations.
        """
        if material_names:
            material_to_write = []
            for name in material_names:
                if name in self._material_repr.keys():
                    material_to_write.append(self._material_repr[name])
        else:
            material_to_write = self._material_repr
        return material_to_write
