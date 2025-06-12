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

from ansys.materials.manager._models._common.dependent_parameter import DependentParameter
from ansys.materials.manager._models._common.independent_parameter import IndependentParameter
from ansys.materials.manager._models._common.interpolation_options import InterpolationOptions
from ansys.materials.manager._models._common.model_qualifier import ModelQualifier
from ansys.materials.manager._models.material import Material
from ansys.materials.manager.util.matml.property_to_model_field import PROPERTY_TO_MODEL_FIELD


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
            cls_name = "ansys.materials.manager._models." + propset_name.replace(" ", "")
            property_map = []
            arguments = {}
            qualifiers = []
            for qualifier in property_set.qualifiers.keys():
                if qualifier == "Behavior":
                    cls_name += property_set.qualifiers[qualifier]
                    propset_name += "::" + property_set.qualifiers[qualifier]
                qualifiers.append(
                    ModelQualifier(name=qualifier, value=property_set.qualifiers[qualifier])
                )
            cls = locate(cls_name)
            if cls:
                property_map += list(cls.model_fields.keys())
                independent_parameters = []
                for name in property_map:
                    if name == "independent_parameters":
                        for param_value in property_set.parameters.values():
                            ind_param = param_value.qualifiers.get("Variable Type")
                            if ind_param and ind_param.split(",")[0] == "Independent":
                                independent_param = IndependentParameter(
                                    name=param_value.name,
                                    values=(
                                        param_value.data
                                        if isinstance(param_value.data, Sequence)
                                        else [param_value.data]
                                    ),
                                    default_value=param_value.qualifiers.get("Default Data", ""),
                                    units=param_value.qualifiers.get("Field Units", ""),
                                    upper_limit=param_value.qualifiers.get("Upper Limit", None),
                                    lower_limit=param_value.qualifiers.get("Lower Limit", None),
                                )
                                independent_parameters.append(independent_param)

                    if name in PROPERTY_TO_MODEL_FIELD.keys():
                        param = property_set.parameters[PROPERTY_TO_MODEL_FIELD[name]]
                        data = param.data
                        if not isinstance(data, Sequence):
                            data = [data]
                        arguments[name] = DependentParameter(
                            name=PROPERTY_TO_MODEL_FIELD[name], values=data
                        )

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
                obj = cls.load(arguments)
                models.append(obj)
            else:
                print(f"Could not find a material model for: {cls_name.split(".")[-1]}")

        mapdl_material = Material(
            material_name=mat_id, material_id=global_material_index, models=models
        )

        if mat_id in transfer_ids.keys():
            mapdl_material.guid = transfer_ids[mat_id]

        materials.append(mapdl_material)

        global_material_index += 1

    return materials
