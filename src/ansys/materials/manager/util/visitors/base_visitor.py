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

from abc import abstractmethod
import sys

from ansys.materials.manager._models._common.material_model import MaterialModel
from ansys.materials.manager._models.material import Material

MATERIAL_MODEL_MAP = {}


class BaseVisitor:
    """Base visitor. All visitors should inherit from this class."""

    def __init__(self, materials: list[Material]):
        """Initialize the base visitor."""
        self._materials: list[Material] = materials
        self._material_repr: dict = {material.name: [] for material in materials}

    def get_material_id(self, material_name) -> int:
        """
        Get the material id given the material name.

        Parameters
        ----------
        material_name : str
            Name of the material.

        Returns
        -------
        int
            Material id.
        """
        return [material.mat_id for material in self._materials if material.name == material_name][
            0
        ]

    def is_supported(self, material_model: MaterialModel) -> bool:
        """
        Check if the material model is supported.

        Parameters
        ----------
        material_model : MaterialModel
            Material model to check.

        Returns
        -------
        bool
            True if the material model is supported, False otherwise.
        """
        module = sys.modules[self.__module__]
        mapping = getattr(module, "MATERIAL_MODEL_MAP")
        if material_model.__class__ in mapping.keys():
            return True
        else:
            return False

    @abstractmethod
    def visit_material_model(self, material_name: str, material_model: MaterialModel):
        """Abstract implementation of the visit material model."""
        raise NotImplementedError()

    def visit_materials(self):
        """Visit materials."""
        for material in self._materials:
            for material_model in material.models:
                if not self.is_supported(material_model):
                    print(
                        f"Material model: {material_model.__class__.__name__} not supported by {self.__class__.__name__}"  # noqa: E501
                    )
                    continue
                self.visit_material_model(material.name, material_model)
