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

from ansys.materials.manager._models._common.material_model import MaterialModel
from ansys.materials.manager._models._common.model_qualifier import ModelQualifier
from ansys.materials.manager._models._material_models import ElasticityAnisotropic
from ansys.materials.manager._models._material_models.cofficient_of_thermal_expansion_isotropic import (  # noqa: E501
    CoefficientofThermalExpansionIsotropic,
)
from ansys.materials.manager._models._material_models.cofficient_of_thermal_expansion_orthotropic import (  # noqa: E501
    CoefficientofThermalExpansionOrthotropic,
)
from ansys.materials.manager._models._material_models.hill_yield_criterion import HillYieldCriterion
from ansys.materials.manager._models._material_models.isotropic_hardening import IsotropicHardening
from ansys.materials.manager.parsers._common import get_creep_flag


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


def get_thermal_expansion_flag(qualifiers: list[ModelQualifier]) -> int:
    """
    Get thermal expansion flag.

    Parameters
    ----------
    qualifiers : list[ModelQualifier]
        List of model qualifiers.
    Returns
    -------
    int
        Index for label selection.
    """
    for qualifier in qualifiers:
        if qualifier.name == "Definition":
            if qualifier.value == "Instantaneous":
                return 0
        else:
            return 1


def map_coefficient_of_thermal_expansion_isotropic(
    material_model: CoefficientofThermalExpansionIsotropic,
) -> tuple[list[str], Quantity]:
    """
    Map isotropic coefficient of thermal expansion model to dependent values for MAPDL.

    Parameters
    ----------
    material_model : CoefficientofThermalExpansionIsotropic
        The isotropic coefficient of thermal expansion material model.

    Returns
    -------
    list[Quantity]
        The list of coefficient of thermal expansion values.
    """
    idx = get_thermal_expansion_flag(material_model.model_qualifiers)
    labels = [["CTEX"], ["ALPX"]]
    return labels[idx], [material_model.coefficient_of_thermal_expansion]


def map_coefficient_of_thermal_expansion_orthotropic(
    material_model: CoefficientofThermalExpansionOrthotropic,
) -> tuple[list[str], list[Quantity]]:
    """
    Map orthotropic coefficient of thermal expansion model to dependent values for MAPDL.

    Parameters
    ----------
    material_model : CoefficientofThermalExpansionOrthotropic
        The orthotropic coefficient of thermal expansion material model.

    Returns
    -------
    list[Quantity]
        The list of coefficient of thermal expansion values in X, Y, Z directions.
    """
    idx = get_thermal_expansion_flag(material_model.model_qualifiers)
    labels = [
        ["CTEX_X", "CTEX_Y", "CTEX_Z"],
        ["ALPX", "ALPY", "ALPZ"],
    ]
    return labels[idx], [
        material_model.coefficient_of_thermal_expansion_x,
        material_model.coefficient_of_thermal_expansion_y,
        material_model.coefficient_of_thermal_expansion_z,
    ]


def map_from_anisotropic_elasticity(
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


def map_from_hill_yield_criterion(
    material_model: HillYieldCriterion,
) -> tuple[list[str], list[list[float]]]:
    """
    Map Hill yield criterion model to dependent values for MAPDL.

    Parameters
    ----------
    material_model : HillYieldCriterion
        The Hill yield criterion material model.
    Returns
    -------
    tuple[list[str], list[list[float]]]
        The list of labels and the list of yield stress ratio values.
    """
    idx = get_creep_flag(material_model.model_qualifiers)
    yield_stress = [
        material_model.yield_stress_ratio_x.value,
        material_model.yield_stress_ratio_y.value,
        material_model.yield_stress_ratio_z.value,
        material_model.yield_stress_ratio_xy.value,
        material_model.yield_stress_ratio_yz.value,
        material_model.yield_stress_ratio_xz.value,
    ]
    tb_opt = ""

    if idx == 1:
        yield_stress += [
            material_model.creep_stress_ratio_x.value,
            material_model.creep_stress_ratio_y.value,
            material_model.creep_stress_ratio_z.value,
            material_model.creep_stress_ratio_xy.value,
            material_model.creep_stress_ratio_yz.value,
            material_model.creep_stress_ratio_xz.value,
        ]
        tb_opt = "PC"

    return [tb_opt], [yield_stress]


def map_from_isotropic_hardening(
    material_model: IsotropicHardening,
) -> tuple[list[str], list[list[float]]]:
    """
    Map isotropic hardening model to dependent values for MAPDL.

    Parameters
    ----------
    material_model : IsotropicHardening
        The isotropic hardening material model.

    Returns
    -------
    tuple[list[str], list[list[float]]]
        The list of labels and the list of values.
    """
    tb_opt = ""
    for qualifier in material_model.model_qualifiers:
        if qualifier.name == "Definition" and qualifier.value == "Multilinear":
            tb_opt = "MISO"
            break
        elif qualifier.name == "Definition" and qualifier.value == "Bilinear":
            tb_opt = "BISO"
            break
    if tb_opt == "":
        raise ValueError("IsotropicHardening model requires a valid 'Definition' qualifier.")
    elif tb_opt == "BISO":
        values = [
            material_model.yield_strength.value,
            material_model.tangent_modulus.value,
        ]
        return [tb_opt], [values]
    else:
        plastic_strain = [
            ind_param.values.value.tolist()
            for ind_param in material_model.independent_parameters
            if ind_param.name == "Plastic Strain"
        ][0]
        values = [
            plastic_strain,
            material_model.stress.value.tolist(),
        ]
        return [tb_opt], [values]
