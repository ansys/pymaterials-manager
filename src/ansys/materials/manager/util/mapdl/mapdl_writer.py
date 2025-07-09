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

import math

from ansys.units import Quantity

from ansys.materials.manager._models._common import IndependentParameter, InterpolationOptions

from .mapdl_snippets_strings import (
    CONSTANT_MP_PROPERTY,
    EXTRAPOLATION_TYPE_MAP,
    INTERPOLATION_ALGORITHM_MAP,
    MP_DATA,
    MP_TEMP,
    PREDIFINED_TB_FIELDS,
    TB,
    TB_DATA,
    TB_FIELD,
    TBIN_ALGO,
    TBIN_BNDS,
    TBIN_CACH,
    TBIN_DEFA,
    TBIN_EXTR,
    TBIN_NORM,
    USER_DEFINED_TB_FIELDS,
)


def _get_table_constants(idx, values):
    val1 = values[idx * 6 + 1]
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
    property: Quantity,
    material_id,
    c1: float | None = None,
    c2: float | None = None,
    c3: float | None = None,
    c4: float | None = None,
):
    """Write constant property."""
    if isinstance(property.value, int, float):
        c0 = str(property.value)
    else:
        c0 = str(property.value).strip("[]")
    return CONSTANT_MP_PROPERTY.format(
        lab=label,
        matid=material_id,
        c0=c0,
        c1=c1 or "",
        c2=c2 or "",
        c3=c3 or "",
        c4=c4 or "",
        unit=property.unit,
    )


def write_interpolation_options(
    interpolation_options: InterpolationOptions, independent_parameters: list[IndependentParameter]
) -> str:
    """Write interpolation options."""
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
    if interpolation_options.extrapolation_type:
        interpolation_string += TBIN_EXTR.format(
            par1="", par2=EXTRAPOLATION_TYPE_MAP[interpolation_options.extrapolation_type]
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
            interpolation_string += TBIN_BNDS.format(
                par1=independent_parameter.name,
                par2=independent_parameter.lower_limit,
                par3=independent_parameter.upper_limit,
            )
    return interpolation_string


def write_temperature_table_values(
    label: str,
    dependent_parameters: list[Quantity],
    material_id: int,
    temerature_parameter: IndependentParameter,
) -> str:
    """Write temperature table."""
    n_loops = math.ceil(len(temerature_parameter.values.value) / 6)
    table_str = ""
    temp_vals = temerature_parameter.values.value.tolist()
    for i in range(n_loops):
        t1, t2, t3, t4, t5, t6 = _get_table_constants(i, temp_vals)
        table_str += MP_TEMP.format(sloc=i * 6 + 1, t1=t1, t2=t2, t3=t3, t4=t4, t5=t5, t6=t6)
    for i in range(n_loops):
        for dependent_parameter in dependent_parameters:
            dep_vals = dependent_parameter.value
            dep_unit = dependent_parameter.unit
            c1, c2, c3, c4, c5, c6 = _get_table_constants(i, dep_vals)
            table_str += MP_DATA.format(
                lab=label,
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
    return table_str


def write_table_values(
    label: str,
    dependent_parameter: list[Quantity],
    material_id: int,
    independent_parameters: list[IndependentParameter],
    tb_opt: str | None = None,
) -> tuple[str, str]:
    """Write table variables."""
    parameters_str = ""
    idx = 1
    independent_values = []
    independent_values_names = []
    independent_values_units = []
    for independent_parameter in independent_parameters:
        if independent_parameter.name in PREDIFINED_TB_FIELDS.keys():
            parameters_str += PREDIFINED_TB_FIELDS[independent_parameter.name]
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
    table_str = TB.format(lab=label, matid=material_id, tbopt=tb_opt or "")

    dependent_values = list(zip(*dependent_parameter))

    for idx_val, ind_vals in enumerate(list(zip(*independent_values))):
        idx = 0
        for ind_val in ind_vals:
            table_str += TB_FIELD.format(
                type=independent_values_names[idx],
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
        for i in range(n_loops):
            c1, c2, c3, c4, c5, c6 = _get_table_constants(i, dep_vals.value)
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


def write_tb_points(
    label: str,
    dependent_parameter: Quantity,
    material_id: int,
    independent_parameters: list[IndependentParameter],
    tb_opt: str,
) -> tuple[str, str]:
    """Write points table."""
    pass
