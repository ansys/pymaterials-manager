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

from ansys.dyna.core.lib.keyword_base import KeywordBase

from ansys.materials.manager._models._material_models.elasticity_anisotropic import (
    ElasticityAnisotropic,
)
from ansys.materials.manager._models.material import Material
from ansys.materials.manager.util.ls_dyna.writer_ls_dyna_utils import (
    MAT_CARD_REGISTRY,
    get_anisotropic_attributes_values,
    get_attributes_values,
)
from ansys.materials.manager.util.writer import register_writer


@register_writer("Deck")
class WriterLsDyna:
    """Class containing the methods for writing into a LS-Dyna session."""

    def write_material(self, material: Material, material_id: int, **kwargs) -> list[KeywordBase]:
        """Write material in the lsdyna deck."""
        models = material.models
        instanciated_models = []
        instanciated_models_name = []
        available = {model.__class__.__name__: model for model in models}
        class_to_instance = {type(obj): obj for obj in available.values()}
        model_classes = set(class_to_instance.keys())
        for required_classes_key, target_cls in MAT_CARD_REGISTRY.items():
            if (target_cls.keyword + target_cls.subkeyword).lower() in instanciated_models_name:
                continue
            required_classes = set(required_classes_key)
            if required_classes.issubset(model_classes):
                args = {}
                for required_cls in required_classes_key:
                    instance = class_to_instance.get(required_cls)
                    if instance is None:
                        break
                    if isinstance(instance, ElasticityAnisotropic):
                        args.update(get_anisotropic_attributes_values(instance))
                    else:
                        args.update(get_attributes_values(instance))
                material_class = target_cls(mid=material_id)

                for key, value in args.items():
                    setattr(material_class, key, value[0] if isinstance(value, Sequence) else value)
                instanciated_models.append(material_class)
                instanciated_models_name.append(material_class.__class__)
        return instanciated_models
