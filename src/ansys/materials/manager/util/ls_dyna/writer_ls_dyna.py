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

from ansys.dyna.core import keywords as kwd
from ansys.dyna.core.lib.keyword_base import KeywordBase

from ansys.materials.manager._models._common.material_model import MaterialModel  # noqa: E501
from ansys.materials.manager._models._material_models.density import Density
from ansys.materials.manager._models._material_models.elasticity_isotropic import (  # noqa: E501
    ElasticityIsotropic,
)
from ansys.materials.manager._models.material import Material
from ansys.materials.manager.util.common_writer import register_writer


def normalize_key(classes: tuple[type]) -> tuple[type]:
    """Normalize the mat card registry key."""
    return tuple(sorted(classes, key=lambda cls: cls.__name__))


# most complete needs to go before
MAT_CARD_REGISTRY = {
    normalize_key((Density, ElasticityIsotropic)): kwd.Mat001,
    normalize_key((ElasticityIsotropic,)): kwd.Mat001,
}


def get_attributes_values(model: MaterialModel) -> dict:
    """Get the attribute to the dyna model and values."""
    labels = [
        field.lsdyna_name
        for field in model.__class__.model_fields.values()
        if hasattr(field, "lsdyna_name") and field.lsdyna_name
    ]
    dependant_parameter_names = [
        model_name
        for model_name, field in model.__class__.model_fields.items()
        if hasattr(field, "lsdyna_name") and field.lsdyna_name
    ]
    dict_model = model.model_dump()
    dependent_parameters = []
    for name in dependant_parameter_names:
        value = dict_model[name]["value"]
        dependent_parameters.append(value.tolist())
    return dict(zip(labels, dependent_parameters))


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
                    args.update(get_attributes_values(instance))
                material_class = target_cls(mid=material_id)
                for key, value in args.items():
                    setattr(material_class, key, value[0])
                instanciated_models.append(material_class)
                instanciated_models_name.append(material_class.__class__.__name__.lower())
        return instanciated_models
