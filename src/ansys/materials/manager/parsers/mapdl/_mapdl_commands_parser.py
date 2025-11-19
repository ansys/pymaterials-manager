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
import math

import numpy as np

from ansys.materials.manager._models._common import IndependentParameter, InterpolationOptions
from ansys.materials.manager._models._material_models.elasticity_anisotropic import (
    ElasticityAnisotropic,
)
from ansys.materials.manager._models._material_models.hill_yield_criterion import HillYieldCriterion
from ansys.materials.manager._models._material_models.isotropic_hardening import IsotropicHardening

from ._mapdl_snippets_strings import (
    CONSTANT_MP_PROPERTY,
    EXTRAPOLATION_TYPE_MAP,
    INTERPOLATION_ALGORITHM_MAP,
    MP_DATA,
    MP_TEMP,
    PREDIFINED_TB_FIELDS,
    TB,
    TB_DATA,
    TB_FIELD,
    TB_TEMP,
    TBIN_ALGO,
    TBIN_BNDS,
    TBIN_CACH,
    TBIN_DEFA,
    TBIN_EXTR,
    TBIN_NORM,
    TBPT,
    TEMPERATURE_REFERENCE,
    USER_DEFINED_TB_FIELDS,
)

TABLE_LABELS = {
    "ElasticityIsotropic": "ELASTIC",
    "ElasticityOrthotropic": "ELASTIC",
    "ElasticityAnisotropic": "ELASTIC",
    "CoefficientofThermalExpansionIsotropic": "CTE",
    "CoefficientofThermalExpansionOrthotropic": "CTE",
    "Density": "DENS",
    "ThermalConductivityIsotropic": "THERM",
    "ThermalConductivityOrthotropic": "THERM",
    "IsotropicHardening": "PLASTIC",
    "HillYieldCriterion": "HILL",
    "NeoHookean": "HYPE",
}

TABLE_TBOPT = {
    "ElasticityIsotropic": "ISOT",
    "ElasticityOrthotropic": "OELM",
    "ElasticityAnisotropic": "AELS",
    "CoefficientofThermalExpansionIsotropic": None,
    "CoefficientofThermalExpansionOrthotropic": None,
    "Density": None,
    "ThermalConductivityIsotropic": "COND",
    "ThermalConductivityOrthotropic": "COND",
    "NeoHookean": "NEO",
}


def _get_table_constants(idx, values):
    val1 = values[idx * 6]
    val2 = ""
    val3 = ""
    val4 = ""
    val5 = ""
    val6 = ""
    if len(values) > idx * 6 + 1:
        val2 = values[idx * 6 + 1]
    if len(values) > idx * 6 + 2:
        val3 = values[idx * 6 + 2]
    if len(values) > idx * 6 + 3:
        val4 = values[idx * 6 + 3]
    if len(values) > idx * 6 + 4:
        val5 = values[idx * 6 + 4]
    if len(values) > idx * 6 + 5:
        val6 = values[idx * 6 + 5]
    return val1, val2, val3, val4, val5, val6


def write_constant_property(
    label: str,
    property: float | int | list[float | int] | np.ndarray,
    material_id,
    c1: float | None = None,
    c2: float | None = None,
    c3: float | None = None,
    c4: float | None = None,
    unit: str = "",
):
    """
    Write constant property.

    Example:
    MP,EX,1,1000000,	! Pa
    """
    if isinstance(property, (int, float)):
        c0 = str(property)
    else:
        c0 = str(property).strip("[]")
    return CONSTANT_MP_PROPERTY.format(
        lab=label,
        matid=material_id,
        c0=c0,
        c1=c1 or "",
        c2=c2 or "",
        c3=c3 or "",
        c4=c4 or "",
        unit=unit,
    )


def write_constant_properties(
    labels: list[str],
    properties: list[list[float]],
    property_units: list[str],
    material_id,
    c1: float | None = None,
    c2: float | None = None,
    c3: float | None = None,
    c4: float | None = None,
):
    """
    Write constant properties.

    Example:
    MP,EX,1,1000000,	! Pa
    MP,NUXY,1,0.3,
    """
    property_str = ""
    for i in range(len(labels)):
        label = labels[i]
        property = properties[i]
        unit = property_units[i]
        property_str += write_constant_property(
            label=label,
            property=property,
            material_id=material_id,
            c1=c1,
            c2=c2,
            c3=c3,
            c4=c4,
            unit=unit,
        )
    return property_str


def write_interpolation_options(
    interpolation_options: InterpolationOptions, independent_parameters: list[IndependentParameter]
) -> str:
    """
    Write interpolation options.

    Example:
    TBIN,ALGO,ALMUL
    TBIN,NORM,,ON
    TBIN,EXTR,,BBOX
    TBIN,DEFA,Orientation Tensor A11,0
    TBIN,BNDS,Orientation Tensor A11,0,1
    TBIN,DEFA,Orientation Tensor A22,0
    TBIN,BNDS,Orientation Tensor A22,0,1
    """
    interpolation_string = ""
    if interpolation_options.algorithm_type:
        interpolation_string += TBIN_ALGO.format(
            par1=INTERPOLATION_ALGORITHM_MAP[interpolation_options.algorithm_type]
        )
    par2 = "ON"
    if interpolation_options.normalized == False:
        par2 = "OFF"
    interpolation_string += TBIN_NORM.format(par1="", par2=par2)
    par2 = "ON"
    if interpolation_options.cached == False:
        par2 = "OFF"
    interpolation_string += TBIN_CACH.format(par1="", par2=par2)
    if (
        interpolation_options.extrapolation_type
        and interpolation_options.extrapolation_type != "None"
    ):
        interpolation_string += TBIN_EXTR.format(
            par1="", par2=EXTRAPOLATION_TYPE_MAP[interpolation_options.extrapolation_type]
        )
    else:
        interpolation_string += TBIN_EXTR.format(
            par1="", par2=EXTRAPOLATION_TYPE_MAP["Projection to the Bounding Box"]
        )
    for independent_parameter in independent_parameters:
        if independent_parameter.default_value is not None:
            interpolation_string += TBIN_DEFA.format(
                par1=independent_parameter.name,
                par2=independent_parameter.default_value,
            )
        if (
            independent_parameter.lower_limit is not None
            and independent_parameter.upper_limit is not None
        ):
            if independent_parameter.lower_limit == "Program Controlled":
                lower_limit = min(independent_parameter.values.value.tolist())
            else:
                lower_limit = independent_parameter.lower_limit
            if independent_parameter.upper_limit == "Program Controlled":
                upper_limit = max(independent_parameter.values.value.tolist())
            else:
                upper_limit = independent_parameter.upper_limit
            interpolation_string += TBIN_BNDS.format(
                par1=independent_parameter.name,
                par2=lower_limit,
                par3=upper_limit,
            )
    return interpolation_string


def write_temperature_table_values(
    labels: list[str],
    dependent_parameters: list[list[float]],
    dependent_parameters_unit: list[str],
    material_id: int,
    temperature_parameter: IndependentParameter,
) -> str:
    """
    Write temperature table.

    Example:
    MPTEMP,1,12.0,21.0,,,,
    MPDATA,EX,3,1,2000000,1000000,,,, ! Pa
    MPTEMP,1,12.0,21.0,,,,
    MPDATA,PRXY,3,1,0.35,0.3,,,, !
    """
    n_loops = math.ceil(len(temperature_parameter.values.value) / 6)
    table_str = ""
    temp_vals = temperature_parameter.values.value.tolist()
    for i in range(n_loops):
        t1, t2, t3, t4, t5, t6 = _get_table_constants(i, temp_vals)
        table_str += MP_TEMP.format(sloc=i * 6 + 1, t1=t1, t2=t2, t3=t3, t4=t4, t5=t5, t6=t6)
    for i in range(n_loops):
        j = 0
        for k in range(len(dependent_parameters)):
            dep_vals = dependent_parameters[k]
            dep_unit = dependent_parameters_unit[k]
            c1, c2, c3, c4, c5, c6 = _get_table_constants(i, dep_vals)
            table_str += MP_DATA.format(
                lab=labels[j],
                matid=material_id,
                sloc=i * 6 + 1,
                c1=c1,
                c2=c2,
                c3=c3,
                c4=c4,
                c5=c5,
                c6=c6,
                unit=dep_unit,
            )
            j += 1
    return table_str


def write_table_dep_values(
    material_id: str | None, label: str, dependent_values: list[float], tb_opt: str = ""
) -> str:
    """
    Write table of dependent values.

    Example:
    TB,ELASTIC,1,,,AELS
    TBDATA,1,100000000,1000000,2000000,3000000,4000000,5000000
    TBDATA,7,150000000,6000000,7000000,8000000,9000000,200000000
    TBDATA,13,10000000,11000000,12000000,50000000,13000000,14000000
    TBDATA,19,60000000,15000000,70000000
    """
    table_str = TB.format(lab=label, matid=material_id, tbopt=tb_opt)
    if tb_opt == "PC":
        table_str = table_str[:-5] + table_str[-4:]
    n_loops = math.ceil(len(dependent_values) / 6)
    for i in range(n_loops):
        c1, c2, c3, c4, c5, c6 = _get_table_constants(i, dependent_values)
        table_str += TB_DATA.format(
            stloc=i * 6 + 1,
            c1=c1,
            c2=c2,
            c3=c3,
            c4=c4,
            c5=c5,
            c6=c6,
        )

    return table_str


def _get_field_variables(
    independent_parameters: list[IndependentParameter],
) -> tuple[list[list[float]], list[str], list[str], str]:
    parameters_str = ""
    idx = 1
    independent_values = []
    independent_values_names = []
    independent_values_units = []
    for independent_parameter in independent_parameters:
        if independent_parameter.name in PREDIFINED_TB_FIELDS.keys():
            parameters_str += f"{independent_parameter.name} = '{PREDIFINED_TB_FIELDS[independent_parameter.name]}' ! {independent_parameter.name}"  # noqa_ E501
        else:
            parameters_str += USER_DEFINED_TB_FIELDS.format(
                name=independent_parameter.name,
                idx=idx,
                unit=(
                    independent_parameter.values.unit
                    if independent_parameter.values.unit != ""
                    else independent_parameter.name
                ),
            )
            idx += 1
        independent_values.append(independent_parameter.values.value.tolist())
        independent_values_names.append(independent_parameter.name)
        independent_values_units.append(independent_parameter.values.unit)
    return independent_values, independent_values_names, independent_values_units, parameters_str


def write_table_values(
    label: str,
    dependent_parameters: list[list[float]],
    material_id: int,
    independent_parameters: list[IndependentParameter],
    tb_opt: str | None = None,
) -> tuple[str, str]:
    """
    Write table variables.

    Example:
    Orientation Tensor A11 = 'UF01' ! Orientation Tensor A11
    Orientation Tensor A22 = 'UF02' ! Orientation Tensor A22
    Temperature = 'TEMP' ! Temperature
    TB,ELASTIC,1,,,OELM
    TBFIELD,Orientation Tensor A11,0 ! Orientation Tensor A11
    TBFIELD,Orientation Tensor A22,0 ! Orientation Tensor A22
    TBFIELD,TEMP,50 ! Temperature
    TBDATA,1,10,10,10,4.54,4.54,4.54
    TBDATA,7,0.1,0.1,0.1
    TBFIELD,Orientation Tensor A11,0 ! Orientation Tensor A11
    TBFIELD,Orientation Tensor A22,0 ! Orientation Tensor A22
    TBFIELD,TEMP,100 ! Temperature
    TBDATA,1,10,10,10,4.54,4.54,4.54
    TBDATA,7,0.1,0.1,0.1
    """
    independent_values, independent_values_names, independent_values_units, parameters_str = (
        _get_field_variables(independent_parameters=independent_parameters)
    )

    table_str = TB.format(lab=label, matid=material_id, tbopt=tb_opt or "")
    if tb_opt == "PC":
        table_str = table_str[:-5] + table_str[-4:]
    dependent_values = list(zip(*dependent_parameters))

    for idx_val, ind_vals in enumerate(list(zip(*independent_values))):
        idx = 0
        for ind_val in ind_vals:
            table_str += TB_FIELD.format(
                type=(
                    PREDIFINED_TB_FIELDS[independent_values_names[idx]]
                    if independent_values_names[idx] in PREDIFINED_TB_FIELDS.keys()
                    else independent_values_names[idx]
                ),
                value=ind_val,
                unit=(
                    independent_values_units[idx]
                    if independent_values_units[idx] != ""
                    else independent_values_names[idx]
                ),
            )
            idx += 1

        dep_vals = dependent_values[idx_val]
        n_loops = math.ceil(len(dep_vals) / 6)
        vals = []
        for j in range(len(dep_vals)):
            vals.append(dep_vals[j])
        for i in range(n_loops):
            c1, c2, c3, c4, c5, c6 = _get_table_constants(i, vals)
            table_str += TB_DATA.format(
                stloc=i * 6 + 1,
                c1=c1,
                c2=c2,
                c3=c3,
                c4=c4,
                c5=c5,
                c6=c6,
            )
    return parameters_str, table_str


def write_table_value_per_temperature(
    label: str,
    material_id: int,
    dependent_parameters: list[list[float]],
    temperature_parameter: IndependentParameter,
    tb_opt: str = "",
) -> str:
    """
    Write table values per temperature.

    Example:
    Temperature = 'TEMP' ! Temperature
    TB,HILL,2,,,
    TBTEMP,34
    TBDATA,1,1.2,0.8,0.5,0.12,0.23,0.23
    TBTEMP,78
    TBDATA,1,1.2,0.8,0.5,0.12,0.23,0.23
    """
    table_str = f"{temperature_parameter.name} = '{PREDIFINED_TB_FIELDS[temperature_parameter.name]}' ! {temperature_parameter.name}\n"  # noqa_ E501
    line = TB.format(lab=label, matid=material_id, tbopt=tb_opt)
    if tb_opt == "PC":
        line = line[:-5] + line[-4:]
    table_str += line
    n_loops = math.ceil(len(dependent_parameters) / 6)
    temp_idx = 0
    for temperature in temperature_parameter.values.value:
        table_str += TB_TEMP.format(temp=temperature)
        vals = []
        for dep_vals in dependent_parameters:
            vals.append(dep_vals[temp_idx])
        for i in range(n_loops):
            c1, c2, c3, c4, c5, c6 = _get_table_constants(i, vals)
            table_str += TB_DATA.format(
                stloc=i * 6 + 1,
                c1=c1,
                c2=c2,
                c3=c3,
                c4=c4,
                c5=c5,
                c6=c6,
            )
        temp_idx += 1
    return table_str


def write_tb_points_for_temperature(
    label: str,
    table_parameters: list[list[float]],
    material_id: int,
    temperature_parameter: list[float],
    tb_opt: str,
) -> tuple[str, str]:
    """
    Write points table.

    Example:
    TB,PLASTIC,2,,MISO
    TBFIELD,TEMP,22, !
    TBPT,,0.0,16704754.8966912
    TBPT,,0.000189791542302976,21518003.4164155
    TBPT,,0.000379583084605952,25601270.737195
    TBPT,,0.000569374626908928,29108916.0548528
    """
    table_str = TB.format(lab=label, matid=material_id, tbopt=tb_opt or "")
    if label == "PLASTIC":
        table_str = table_str.replace(",,", ",", 1)
    counts = Counter(temperature_parameter)
    for num, count in counts.items():
        table_str += TB_FIELD.format(type="TEMP", value=num, unit="")
        for i in range(count):
            table_str += TBPT.format(oper="", x=table_parameters[0][i], y=table_parameters[1][i])
    return table_str


def write_temperature_reference_value(material_id: int, temperature: float) -> str:
    """
    Write reference temperature.

    Example:
    MP,REFT,1,21,
    """
    return TEMPERATURE_REFERENCE.format(matid=material_id, temp=temperature)


def get_table_label(model_name: str) -> str | None:
    """Get table label string."""
    return TABLE_LABELS.get(model_name, None)


def get_tbopt(model_name: str) -> str | None:
    """Get table tbopt string."""
    return TABLE_TBOPT.get(model_name, None)


def write_anisotropic_elasticity(model: ElasticityAnisotropic, material_id: int):
    """Write anisotropic elasticity."""
    d = np.column_stack(
        (
            model.column_1.value,
            model.column_2.value,
            model.column_3.value,
            model.column_4.value,
            model.column_5.value,
            model.column_6.value,
        )
    )
    # extract the lower triangular elements column-wise
    dependent_values = []
    for j in range(6):
        dependent_values.extend(d[j:, j])

    material_string = write_table_dep_values(
        material_id=material_id,
        label=TABLE_LABELS[model.__class__.__name__],
        dependent_values=dependent_values,
        tb_opt=TABLE_TBOPT[model.__class__.__name__],
    )
    return material_string


def write_isotropic_hardening(self, model: IsotropicHardening, material_id: int):
    """Write isotropic hardening."""
    plastic_strain = [
        ind_param.values.value.tolist()
        for ind_param in model.independent_parameters
        if ind_param.name == "Plastic Strain"
    ][0]
    temperature = [
        ind_param.values.value.tolist()
        for ind_param in model.independent_parameters
        if ind_param.name == "Temperature"
    ]
    table_parameters = [
        plastic_strain,
        model.stress.value.tolist(),
    ]
    table_label = TABLE_LABELS[model.__class__.__name__]
    table_tbopt = TABLE_TBOPT[model.__class__.__name__]
    if len(model.independent_parameters) == 1:
        temperature_parameter = len(table_parameters[0]) * [0]
        material_string = write_tb_points_for_temperature(
            label=table_label,
            table_parameters=table_parameters,
            material_id=material_id,
            temperature_parameter=temperature_parameter,
            tb_opt=table_tbopt,
        )

    elif len(model.independent_parameters) == 2 and len(temperature) == 1:
        material_string = write_tb_points_for_temperature(
            label=table_label,
            table_parameters=table_parameters,
            material_id=material_id,
            temperature_parameter=temperature[0],
            tb_opt=table_tbopt,
        )
    else:
        raise Exception("Only variable supported at the moment is temperature")
    return material_string


def write_hill_yield(self, model: HillYieldCriterion, material_id: int):
    """Write Hill yield."""
    label = TABLE_LABELS[model.__class__.__name__]
    for qualifier in model.model_qualifiers:
        if qualifier.name == "Separated Hill Potentials for Plasticity and Creep":
            creep = True if qualifier.value == "Yes" else False

    if not creep:
        dependent_values = [
            model.yield_stress_ratio_x.value,
            model.yield_stress_ratio_y.value,
            model.yield_stress_ratio_z.value,
            model.yield_stress_ratio_xy.value,
            model.yield_stress_ratio_yz.value,
            model.yield_stress_ratio_xz.value,
        ]
        tb_opt = ""
    else:
        dependent_values = [
            model.yield_stress_ratio_x_for_plasticity.value,
            model.yield_stress_ratio_y_for_plasticity.value,
            model.yield_stress_ratio_z_for_plasticity.value,
            model.yield_stress_ratio_xy_for_plasticity.value,
            model.yield_stress_ratio_yz_for_plasticity.value,
            model.yield_stress_ratio_xz_for_plasticity.value,
            model.yield_stress_ratio_x_for_creep.value,
            model.yield_stress_ratio_y_for_creep.value,
            model.yield_stress_ratio_z_for_creep.value,
            model.yield_stress_ratio_xy_for_creep.value,
            model.yield_stress_ratio_yz_for_creep.value,
            model.yield_stress_ratio_xz_for_creep.value,
        ]
        tb_opt = "PC"

    if not model.independent_parameters:
        dependent_values = [
            dep_val[0] for dep_val in dependent_values if isinstance(dep_val, np.ndarray)
        ]
        material_string = write_table_dep_values(
            material_id=material_id,
            label=label,
            dependent_values=dependent_values,
            tb_opt=tb_opt,
        )
        return material_string
    elif (
        len(model.independent_parameters) == 1
        and model.independent_parameters[0].name == "Temperature"
    ):
        if len(model.independent_parameters[0].values.value) == 1:
            material_string = write_table_dep_values(
                material_id=material_id,
                label=label,
                dependent_values=dependent_values,
                tb_opt=tb_opt,
            )
        else:
            material_string = write_table_value_per_temperature(
                label=label,
                material_id=material_id,
                dependent_parameters=dependent_values,
                temperature_parameter=model.independent_parameters[0],
                tb_opt=tb_opt,
            )
        return material_string
    else:
        parameters_str, table_str = write_table_values(
            label=label,
            dependent_parameters=dependent_values,
            material_id=material_id,
            independent_parameters=model.independent_parameters,
            tb_opt=tb_opt,
        )
        material_string = parameters_str + "\n" + table_str
        return material_string
