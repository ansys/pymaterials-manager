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

from ansys.materials.manager._models._common.material_model import MaterialModel
from ansys.materials.manager._models._material_models import ElasticityAnisotropic


def get_value(model: MaterialModel, attr_name: str) -> float:
    """
    Safe extract scalar value from material property.

    Parameters
    ----------
    model : MaterialModel
        The material model instance.
    attr_name : str
        The attribute name to extract the value from.

    Returns
    -------
    float
        The extracted scalar value.

    """
    value = getattr(model, attr_name).value
    return value[0] if hasattr(value, "__len__") and len(value) > 0 else value


def map_anisotropic_elasticity(
    material_model: ElasticityAnisotropic,
) -> tuple[list[str], list[list[float]]]:
    """Map anisotropic elasticity model to dependent values for MAPDL.

    Returns the 21 unique elements of the symmetric stiffness matrix
    in column-wise lower triangular order.

    Parameters
    ----------
    material_model : ElasticityAnisotropic
        The anisotropic elasticity material model.
    Returns
    -------
    list[float]
        The list of 21 unique stiffness matrix elements.
    """
    return ["lower_triangular"], [
        [
            get_value(material_model, "c_11"),
            get_value(material_model, "c_12"),
            get_value(material_model, "c_13"),
            get_value(material_model, "c_14"),
            get_value(material_model, "c_15"),
            get_value(material_model, "c_16"),
            get_value(material_model, "c_22"),
            get_value(material_model, "c_23"),
            get_value(material_model, "c_24"),
            get_value(material_model, "c_25"),
            get_value(material_model, "c_26"),
            get_value(material_model, "c_33"),
            get_value(material_model, "c_34"),
            get_value(material_model, "c_35"),
            get_value(material_model, "c_36"),
            get_value(material_model, "c_44"),
            get_value(material_model, "c_45"),
            get_value(material_model, "c_46"),
            get_value(material_model, "c_55"),
            get_value(material_model, "c_56"),
            get_value(material_model, "c_66"),
        ]
    ]
