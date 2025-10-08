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

"""Provides a function to convert MatML entries into Material objects."""

from pydoc import locate
from typing import Dict, Sequence

from ansys.units import Quantity

from ansys.materials.manager._models._common import (
    IndependentParameter,
    InterpolationOptions,
    ModelQualifier,
    UserParameter,
)
from ansys.materials.manager._models.material import Material
from ansys.materials.manager.util.common import convert_to_float_or_keep

from .matml_parser import BEHAVIOR_KEY
from .utils import get_data_and_unit, parse_property_set_name

MODEL_NAMESPACE = "ansys.materials.manager._models._material_models."


def convert_matml_materials(
    materials_dict: Dict, transfer_ids: Dict, index_offset: int
) -> Sequence[Material]:
    """
    Convert a list of materials into Material objects.

    Parameters
    ----------
    materials_dict:
        dict of raw material data from a matml import
    transfer_ids:
        dict of material names and unique transfer ids
    index_offset:
        int to offset the material id (number) to avoid conflicts with already existing materials
    Returns a list of Material objects
    """
    materials = []

    global_material_index = 1 + index_offset
    # loop over the materials
    for mat_id, material_data in materials_dict.items():
        models = []
        # loop over the defined property sets
        for propset_name, property_set in material_data.items():
            cls_name = MODEL_NAMESPACE + parse_property_set_name(propset_name)
            property_map = []
            arguments = {}
            qualifiers = []
            for qualifier in property_set.qualifiers.keys():
                if qualifier == BEHAVIOR_KEY:
                    cls_name += property_set.qualifiers[qualifier].replace(" ", "")
                qualifiers.append(
                    ModelQualifier(name=qualifier, value=property_set.qualifiers[qualifier])
                )
            cls = locate(cls_name)
            if cls:
                property_map += list(cls.model_fields.keys())
                titles = {
                    name: field_info.matml_name
                    for name, field_info in cls.__fields__.items()
                    if hasattr(field_info, "matml_name")  # noqa: E501
                }
                independent_parameters = []
                for name in property_map:
                    if name == "independent_parameters":
                        for param_value in property_set.parameters.values():
                            ind_param = param_value.qualifiers.get("Variable Type")
                            if ind_param and ind_param.split(",")[0] == "Independent":
                                data, units = get_data_and_unit(param_value)
                                independent_param = IndependentParameter(
                                    name=param_value.name,
                                    values=Quantity(value=data, units=units),
                                    default_value=convert_to_float_or_keep(
                                        param_value.qualifiers.get("Default Data", None)
                                    ),
                                    upper_limit=convert_to_float_or_keep(
                                        param_value.qualifiers.get("Upper Limit", None)
                                    ),
                                    lower_limit=convert_to_float_or_keep(
                                        param_value.qualifiers.get("Lower Limit", None)
                                    ),
                                )
                                independent_parameters.append(independent_param)
                    if name in titles.keys() and cls.__class__.__name__ != "ModelCoefficients":
                        param_name = titles[name]
                        if param_name in property_set.parameters.keys():
                            param = property_set.parameters[param_name]
                            if name not in ["red", "green", "blue", "material_property"]:
                                data, units = get_data_and_unit(param)
                                arguments[name] = Quantity(value=data, units=units)
                            else:
                                data = param.data
                                if isinstance(data, float):
                                    data = int(data)
                                arguments[name] = data

                    if name == "model_qualifiers":
                        arguments["model_qualifiers"] = qualifiers

                arguments["independent_parameters"] = independent_parameters
                if "Options Variable" in property_set.parameters.keys():
                    variable_options = property_set.parameters["Options Variable"].qualifiers
                    interpolation_options = InterpolationOptions(
                        algorithm_type=variable_options.get("AlgorithmType", ""),
                        normalized=variable_options.get("Normalized", True),
                        cached=variable_options.get("Cached", True),
                        quantized=variable_options.get("Quantized", None),
                        extrapolation_type=variable_options.get("ExtrapolationType", "None"),
                    )
                    arguments["interpolation_options"] = interpolation_options
                if cls_name.split(".")[-1] == "ModelCoefficients":
                    user_parameters = []
                    for key_param, value_param in property_set.parameters.items():
                        if value_param.qualifiers.get("UserMat Constant", None):
                            data, units = get_data_and_unit(value_param)
                            user_param = UserParameter(
                                name=key_param,
                                values=Quantity(value=data, units=units),
                                user_mat_constant=value_param.qualifiers["UserMat Constant"],
                            )
                            user_parameters.append(user_param)
                    arguments["user_parameters"] = user_parameters

                obj = cls.load(arguments)
                models.append(obj)
            else:
                print(f"Could not find a material model for: {cls_name.split('.')[-1]}")

        mapdl_material = Material(name=mat_id, material_id=global_material_index, models=models)

        if mat_id in transfer_ids.keys():
            mapdl_material.guid = transfer_ids[mat_id]

        materials.append(mapdl_material)

        global_material_index += 1

    return materials
