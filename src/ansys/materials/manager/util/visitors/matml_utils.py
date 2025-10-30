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

from ansys.units import Quantity

from ansys.materials.manager._models._material_models.elasticity_anisotropic import (
    ElasticityAnisotropic,
)


def map_anisotropic_elasticity(
    material_model: ElasticityAnisotropic,
) -> tuple[list[str], list[Quantity]]:
    """
    Map anisotropic elasticity model to dependent values for MATML.

    Returns the quantity columns of the stiffness matrix.

    Parameters
    ----------
    material_model : ElasticityAnisotropic
        The anisotropic elasticity material model.

    Returns
    -------
    list[Quantity]
        The six columns of the stiffness matrix as quantities.
    """
    quantities = []
    n_single_values = len(material_model.c_11.value) if material_model.c_11 else 0
    values_column_1 = []
    values_column_2 = []
    values_column_3 = []
    values_column_4 = []
    values_column_5 = []
    values_column_6 = []
    for i in range(n_single_values):
        values_column_1 += [
            material_model.c_11.value[i],
            material_model.c_12.value[i],
            material_model.c_13.value[i],
            material_model.c_14.value[i],
            material_model.c_15.value[i],
            material_model.c_16.value[i],
        ]
        values_column_2 += [
            material_model.c_12.value[i],
            material_model.c_22.value[i],
            material_model.c_23.value[i],
            material_model.c_24.value[i],
            material_model.c_25.value[i],
            material_model.c_26.value[i],
        ]
        values_column_3 += [
            material_model.c_13.value[i],
            material_model.c_23.value[i],
            material_model.c_33.value[i],
            material_model.c_34.value[i],
            material_model.c_35.value[i],
            material_model.c_36.value[i],
        ]
        values_column_4 += [
            material_model.c_14.value[i],
            material_model.c_24.value[i],
            material_model.c_34.value[i],
            material_model.c_44.value[i],
            material_model.c_45.value[i],
            material_model.c_46.value[i],
        ]
        values_column_5 += [
            material_model.c_15.value[i],
            material_model.c_25.value[i],
            material_model.c_35.value[i],
            material_model.c_45.value[i],
            material_model.c_55.value[i],
            material_model.c_56.value[i],
        ]
        values_column_6 += [
            material_model.c_16.value[i],
            material_model.c_26.value[i],
            material_model.c_36.value[i],
            material_model.c_46.value[i],
            material_model.c_56.value[i],
            material_model.c_66.value[i],
        ]

    quantities.append(Quantity(value=values_column_1, units=material_model.c_11.unit))
    quantities.append(Quantity(value=values_column_2, units=material_model.c_12.unit))
    quantities.append(Quantity(value=values_column_3, units=material_model.c_13.unit))
    quantities.append(Quantity(value=values_column_4, units=material_model.c_14.unit))
    quantities.append(Quantity(value=values_column_5, units=material_model.c_15.unit))
    quantities.append(Quantity(value=values_column_6, units=material_model.c_16.unit))
    labels = [
        "D[*,1]",
        "D[*,2]",
        "D[*,3]",
        "D[*,4]",
        "D[*,5]",
        "D[*,6]",
    ]
    return labels, quantities
