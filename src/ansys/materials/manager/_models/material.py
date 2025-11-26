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

from collections import Counter
from typing import List
import uuid

from ansys.materials.manager._models._common import MaterialModel


class Material:
    """
    Provides a wrapper class for managing a material.

    This class associates a material ID with one or more material models.
    """

    name: str
    models: List[MaterialModel]
    _mat_id: str
    _guid: str

    def __init__(
        self,
        name: str,
        material_id: str | None = None,
        models: list[MaterialModel] = [],
        guid: str | None = None,
    ) -> None:
        """
        Create an instance of a material.

        Optionally specify a material ID, or other properties.

        Parameters
        ----------
        material_name : str
            Name of the material.
        material_id : str | None
            ID to associate with this material.
        models : list[MaterialModel]
            list of material models.
        uuid : str | None
            Unique identifier for the material.
        """
        self.name = name
        self._mat_id = material_id
        if uuid is not None:
            self._guid = guid
        else:
            self._guid = str(uuid.uuid4())  # Generate a new UUID if not provided
        self._models = []
        self._models.extend(models)
        self._check_unique_models()

    @property
    def guid(self) -> str:
        """UUID (transfer ID), which is unique."""
        return self._guid

    @guid.setter
    def guid(self, value: str) -> None:
        self._guid = value

    @property
    def mat_id(self) -> int:
        """The material id."""
        return self._mat_id

    @mat_id.setter
    def mat_id(self, value: int) -> None:
        self._mat_id = value

    @property
    def models(self) -> list[MaterialModel]:
        """Currently assigned material models."""
        # returns a copy to block mutation operations
        return self._models.copy()

    @models.setter
    def models(self, value: list[MaterialModel]) -> None:
        """Set the material models."""
        if not isinstance(value, list):
            raise TypeError("models must be a list of MaterialModel instances.")
        self._models = value
        self._check_unique_models()

    def _check_unique_models(self) -> None:
        material_names = Counter([model.name for model in self.models])
        repeated_models = [item for item, count in material_names.items() if count > 1]
        if len(repeated_models) > 0:
            raise (f"The following material models are repeated: {repeated_models}")
        return

    def append_models(self, value: list[MaterialModel] | MaterialModel) -> None:
        """Append one or more material models to the current material models."""
        if isinstance(value, MaterialModel):
            value = [value]
        self._models.extend(value)
        self._check_unique_models()

    def get_model_by_name(self, model_name: str) -> MaterialModel | None:
        """Get the material model with a given model name."""
        model = None
        for mat_model in self.models:
            if model_name.lower() == mat_model.name.lower():
                model = mat_model
        return model
