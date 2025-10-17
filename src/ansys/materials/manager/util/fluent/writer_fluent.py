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

from typing import Sequence

from ansys.materials.manager._models._common.material_model import MaterialModel
from ansys.materials.manager._models.material import Material
from ansys.materials.manager.util.writer import register_writer


@register_writer("Solver")
class WriterFluent:
    """Class containing the methods for writing into a fluent session."""

    def _write_material_model(self, model: MaterialModel):
        label = [
            field.fluent_name
            for field in model.__class__.model_fields.values()
            if hasattr(field, "fluent_name") and field.fluent_name
        ]
        dependant_parameter_names = [
            model_name
            for model_name, field in model.__class__.model_fields.items()
            if hasattr(field, "fluent_name") and field.fluent_name
        ]
        dict_model = model.model_dump()
        dependent_parameters = []
        for name in dependant_parameter_names:
            value = dict_model[name]["value"]
            dependent_parameters.append(value.tolist() if isinstance(value, Sequence) else value)
        return {label[0]: {"option": "constant", "value": dependent_parameters[0]}}

    def write_material(self, material: Material, material_id: int, **kwargs) -> str:
        """Write the material into Fluent."""
        material_model = {}
        for model in material.models:
            model.validate_model()
            material_model.update(self._write_material_model(model))
        return material_model
