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

from ansys.materials.manager._models._common.model_qualifier import ModelQualifier
from ansys.materials.manager._models._common.user_parameter import UserParameter
from ansys.materials.manager._models._material_models.elasticity_anisotropic import (
    ElasticityAnisotropic,
)
from ansys.materials.manager._models._material_models.hill_yield_criterion import HillYieldCriterion
from ansys.materials.manager._models._material_models.isotropic_hardening import IsotropicHardening
from ansys.materials.manager.parsers._common import get_creep_flag
from ansys.materials.manager.parsers.matml._matml_parser import get_data_and_unit


def map_from_anisotropic_elasticity(
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


def map_to_anisotropic_elasticity(property_set: dict) -> tuple[list[str], list[Quantity]]:
    """
    Map anisotropic elasticity model from dependent values for MATML.

    Returns the attribute names and quantities for the stiffness matrix.

    Parameters
    ----------
    property_set : dict
        The anisotropic elasticity property set.

    Returns
    -------
    tuple[list[str], list[Quantity]]
        The attribute names and quantities for the six columns of the stiffness matrix.
    """
    labels = [
        "D[*,1]",
        "D[*,2]",
        "D[*,3]",
        "D[*,4]",
        "D[*,5]",
        "D[*,6]",
    ]
    attributes = []
    quantities = []
    for j in range(6):
        label = labels[j]
        column_values = property_set.parameters.get(label)
        values, units = get_data_and_unit(column_values)
        for i in range(6):
            if j >= i:
                attribute_name = f"c_{i+1}{j+1}"
                attributes.append(attribute_name)
                quantities.append(Quantity(value=[values[i]], units=units))
    return attributes, quantities


def map_from_hill_yield_criterion(
    material_model: HillYieldCriterion,
) -> tuple[list[str], list[Quantity]]:
    """
    Map Hill yield criterion model to dependent values for MATML.

    Parameters
    ----------
    material_model : HillYieldCriterion
        The Hill yield criterion material model.
    Returns
    -------
    list[Quantity]
        The list of yield stress ratio values.
    """
    idx = get_creep_flag(material_model.model_qualifiers)
    labels = [
        [
            "Yield stress ratio in X direction",
            "Yield stress ratio in Y direction",
            "Yield stress ratio in Z direction",
            "Yield stress ratio in XY direction",
            "Yield stress ratio in YZ direction",
            "Yield stress ratio in XZ direction",
        ],
        [
            "Yield stress ratio in X direction for plasticity",
            "Yield stress ratio in Y direction for plasticity",
            "Yield stress ratio in Z direction for plasticity",
            "Yield stress ratio in XY direction for plasticity",
            "Yield stress ratio in YZ direction for plasticity",
            "Yield stress ratio in XZ direction for plasticity",
            "Yield stress ratio in X direction for creep",
            "Yield stress ratio in Y direction for creep",
            "Yield stress ratio in Z direction for creep",
            "Yield stress ratio in XY direction for creep",
            "Yield stress ratio in YZ direction for creep",
            "Yield stress ratio in XZ direction for creep",
        ],
    ]
    yield_attributes = [
        material_model.yield_stress_ratio_x,
        material_model.yield_stress_ratio_y,
        material_model.yield_stress_ratio_z,
        material_model.yield_stress_ratio_xy,
        material_model.yield_stress_ratio_yz,
        material_model.yield_stress_ratio_xz,
    ]
    creep_attributes = [
        material_model.creep_stress_ratio_x,
        material_model.creep_stress_ratio_y,
        material_model.creep_stress_ratio_z,
        material_model.creep_stress_ratio_xy,
        material_model.creep_stress_ratio_yz,
        material_model.creep_stress_ratio_xz,
    ]
    attributes = [yield_attributes, yield_attributes + creep_attributes]
    return labels[idx], attributes[idx]


def map_to_hill_yield_criterion(property_set: dict) -> tuple[list[str], list[Quantity]]:
    """
    Map Hill yield criterion model to dependent values for MATML.

    Parameters
    ----------
    property_set : dict
        The Hill yield criterion property set.

    Returns
    -------
    tuple[list[str], list[Quantity]]
        The labels and quantities for the yield stress ratios.
    """
    qualifiers = [
        ModelQualifier(name=key, value=value) for key, value in property_set.qualifiers.items()
    ]
    idx = get_creep_flag(qualifiers)
    labels = [
        {
            "Yield stress ratio in X direction": "yield_stress_ratio_x",
            "Yield stress ratio in Y direction": "yield_stress_ratio_y",
            "Yield stress ratio in Z direction": "yield_stress_ratio_z",
            "Yield stress ratio in XY direction": "yield_stress_ratio_xy",
            "Yield stress ratio in YZ direction": "yield_stress_ratio_yz",
            "Yield stress ratio in XZ direction": "yield_stress_ratio_xz",
        },
        {
            "Yield stress ratio in X direction for plasticity": "yield_stress_ratio_x",
            "Yield stress ratio in Y direction for plasticity": "yield_stress_ratio_y",
            "Yield stress ratio in Z direction for plasticity": "yield_stress_ratio_z",
            "Yield stress ratio in XY direction for plasticity": "yield_stress_ratio_xy",
            "Yield stress ratio in YZ direction for plasticity": "yield_stress_ratio_yz",
            "Yield stress ratio in XZ direction for plasticity": "yield_stress_ratio_xz",
            "Yield stress ratio in X direction for creep": "creep_stress_ratio_x",
            "Yield stress ratio in Y direction for creep": "creep_stress_ratio_y",
            "Yield stress ratio in Z direction for creep": "creep_stress_ratio_z",
            "Yield stress ratio in XY direction for creep": "creep_stress_ratio_xy",
            "Yield stress ratio in YZ direction for creep": "creep_stress_ratio_yz",
            "Yield stress ratio in XZ direction for creep": "creep_stress_ratio_xz",
        },
    ]
    quantities = []
    for label in labels[idx].keys():
        values = property_set.parameters.get(label, None)
        if values:
            values, units = get_data_and_unit(values)
            quantities.append(Quantity(value=values, units=units))

    return list(labels[idx].values()), quantities


def map_to_model_coefficients(property_set: dict) -> tuple[list[str], list[Quantity]]:
    """
    Map model coefficients to dependent values for MATML.

    Parameters
    ----------
    property_set : dict
        The model coefficients property set.

    Returns
    -------
    tuple[list[str], list[Quantity]]
        The labels and quantities for the model coefficients.
    """
    user_parameters = []
    for parameter_name, parameter_value in property_set.parameters.items():
        if "UserMat Constant" in parameter_value.qualifiers.keys():
            user_mat_constant = parameter_value.qualifiers["UserMat Constant"]
            data, units = get_data_and_unit(parameter_value)
            quantity = Quantity(value=data, units=units)
            user_parameters.append(
                UserParameter(
                    name=parameter_name, values=quantity, user_mat_constant=user_mat_constant
                )
            )
    return ["user_parameters"], [user_parameters]


def map_from_isotropic_hardening(
    isotropic_hardening: IsotropicHardening,
) -> tuple[list[str], list[Quantity]]:
    """
    Map isotropic hardening model parameters to MATML.

    Parameters
    ----------
    isotropic_hardening : IsotropicHardening
        The isotropic hardening material model.

    Returns
    -------
    tuple[list[str], list[Quantity]]
        The labels and quantities for the isotropic hardening model.
    """
    is_multilinear = False
    is_bilinear = False
    for qualifier in isotropic_hardening.model_qualifiers:
        if qualifier.name == "Definition" and qualifier.value == "Multilinear":
            is_multilinear = True
        elif qualifier.name == "Definition" and qualifier.value == "Bilinear":
            is_bilinear = True
    if is_multilinear:
        return ["Stress"], [isotropic_hardening.stress]
    if is_bilinear:
        return ["Yield Strength", "Tangent Modulus"], [
            isotropic_hardening.yield_strength,
            isotropic_hardening.tangent_modulus,
        ]


def map_to_isotropic_hardening(property_set: dict) -> tuple[list[str], list[Quantity]]:
    """
    Map isotropic hardening model parameters from MATML.

    Parameters
    ----------
    property_set : dict
        The isotropic hardening property set.

    Returns
    -------
    tuple[list[str], list[Quantity]]
        The labels and quantities for the isotropic hardening model.
    """
    qualifiers = [
        ModelQualifier(name=key, value=value) for key, value in property_set.qualifiers.items()
    ]

    is_multilinear = False
    is_bilinear = False
    for qualifier in qualifiers:
        if qualifier.name == "Definition" and qualifier.value == "Multilinear":
            is_multilinear = True
        elif qualifier.name == "Definition" and qualifier.value == "Bilinear":
            is_bilinear = True
    labels = []
    quantities = []
    if is_multilinear:
        labels.append("stress")
        values = property_set.parameters.get("Stress")
        data, units = get_data_and_unit(values)
        quantities.append(Quantity(value=data, units=units))
    if is_bilinear:
        labels += ["yield_strength", "tangent_modulus"]
        values_yield_strength = property_set.parameters.get("Yield Strength")
        data_yield_strength, units_yield_strength = get_data_and_unit(values_yield_strength)
        quantities.append(Quantity(value=data_yield_strength, units=units_yield_strength))
        values_tangent_modulus = property_set.parameters.get("Tangent Modulus")
        data_tangent_modulus, units_tangent_modulus = get_data_and_unit(values_tangent_modulus)
        quantities.append(Quantity(value=data_tangent_modulus, units=units_tangent_modulus))
    return labels, quantities
