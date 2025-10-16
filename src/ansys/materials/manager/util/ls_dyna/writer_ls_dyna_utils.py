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
import numpy as np

from ansys.materials.manager._models._common.material_model import MaterialModel  # noqa: E501
from ansys.materials.manager._models._material_models.density import Density
from ansys.materials.manager._models._material_models.elasticity_anisotropic import (
    ElasticityAnisotropic,
)
from ansys.materials.manager._models._material_models.elasticity_isotropic import (  # noqa: E501
    ElasticityIsotropic,
)
from ansys.materials.manager._models._material_models.elasticity_orthotropic import (
    ElasticityOrthotropic,
)


def normalize_key(classes: tuple[type]) -> tuple[type]:
    """Normalize the mat card registry key."""
    return tuple(sorted(classes, key=lambda cls: cls.__name__))


# most complete needs to go before
MAT_CARD_REGISTRY = {
    normalize_key((Density, ElasticityIsotropic)): kwd.Mat001,
    normalize_key((ElasticityIsotropic,)): kwd.Mat001,
    normalize_key((Density, ElasticityOrthotropic)): kwd.Mat002,
    normalize_key((ElasticityOrthotropic,)): kwd.Mat002,
    normalize_key((Density, ElasticityAnisotropic)): kwd.Mat002Anis,
    normalize_key((ElasticityAnisotropic,)): kwd.Mat002Anis,
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


def get_anisotropic_attributes_values(model: ElasticityAnisotropic):
    """Get the attibure to the elasticity anisotropic dyna model."""
    d = np.column_stack(
        (
            model.column_1.value,
            model.column_2.value,
            model.column_3.value,
            model.column_4.value,
            model.column_5.value,
            model.column_6.value,
        )
    ).tolist()
    return {
        "c11": d[0][0],
        "c12": d[0][1],
        "c22": d[1][1],
        "c13": d[0][2],
        "c23": d[1][2],
        "c33": d[2][2],
        "c14": d[0][3],
        "c24": d[1][3],
        "c34": d[2][3],
        "c44": d[3][3],
        "c15": d[0][4],
        "c25": d[1][4],
        "c35": d[2][4],
        "c45": d[3][4],
        "c55": d[4][4],
        "c16": d[0][5],
        "c26": d[1][5],
        "c36": d[2][5],
        "c46": d[3][5],
        "c56": d[4][5],
        "c66": d[5][5],
    }
