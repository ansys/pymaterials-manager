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

import sys

from ansys.materials.manager._models._common.material_model import MaterialModel
from ansys.materials.manager._models.material import Material

MATERIAL_MODEL_MAP = {}


class BaseVisitor:
    """Base visitor."""

    def __init__(self, materials: list[Material]):
        """Initialize the base visitor."""
        self._materials = materials
        self._material_repr: dict = {material.name: [] for material in materials}

    def get_material_id(self, material_name) -> int:
        """Get the material id."""
        return [material.mat_id for material in self._materials if material.name == material_name][
            0
        ]

    def is_supported(self, material_model: MaterialModel) -> bool:
        """Check if the material model is supported."""
        module = sys.modules[self.__module__]
        mapping = getattr(module, "MATERIAL_MODEL_MAP")
        if material_model.__class__ in mapping.keys():
            return True
        else:
            return False

    def visit_materials(self):
        """Visit materials."""
        for mat_id, material in enumerate(self._materials, start=1):
            if material.mat_id == None:
                material.mat_id = mat_id
            for material_model in material.models:
                if not self.is_supported(material_model):
                    print("Material model not supported")
                    continue
                self._material_repr[material.name].append(self.visit_material_model(material_model))
                if hasattr(self, "_material_models_per_material"):
                    self._material_models_per_material[material.name].append(
                        material_model.__class__
                    )
