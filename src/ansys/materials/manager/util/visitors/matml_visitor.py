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

import xml.etree.ElementTree as ET

from ansys.units import Quantity

from ansys.materials.manager._models._common.independent_parameter import IndependentParameter
from ansys.materials.manager._models._common.interpolation_options import InterpolationOptions
from ansys.materials.manager._models._common.material_model import MaterialModel
from ansys.materials.manager._models._common.model_qualifier import ModelQualifier
from ansys.materials.manager._models._material_models.density import Density
from ansys.materials.manager._models._material_models.elasticity_isotropic import (
    ElasticityIsotropic,
)
from ansys.materials.manager.util.matml.utils import (
    convert_to_float_string,
    create_xml_string_value,
)
from ansys.materials.manager.util.visitors.base_visitor import BaseVisitor

# matml material property keys
ELASTICITY = "Elasticity"

# matml material parameter keys
DENSITY = "Density"
YOUNGS_MODULUS = "Young's Modulus"
POISSONS_RATIO = "Poisson's Ratio"

###################
PROPERTY_ID = "pr"
PARAMETER_ID = "pa"
PROPERTY_DATA_KEY = "PropertyData"
DATA_KEY = "Data"
PROPERTY_KEY = "property"
FORMAT_KEY = "format"
STRING_KEY = "string"
DASH_KEY = "-"
QUALIFIER_KEY = "Qualifier"
NAME_KEY = "name"
OPTIONS_VARIABLE_KEY = "Options Variable"
PARAMETER_VALUE_KEY = "ParameterValue"
PARAMETER_KEY = "parameter"
INTERPOLATION_OPTIONS_KEY = "Interpolation Options"
ALGORITTHM_TYPE_KEY = "AlgorithmType"
CACHED_KEY = "Cached"
NORMALIZED_KEY = "Normalized"
EXTRAPOLATION_TYPE_KEY = "ExtrapolationType"
UNITLESS_KEY = "Unitless"
FLOAT_KEY = "float"
INDEPENDENT_KEY = "Independent"
VARIABLE_TYPE_KEY = "Variable Type"
DEFAULT_DATA_KEY = "Default Data"
UPPER_LIMIT_KEY = "Upper Limit"
LOWER_LIMIT_KEY = "Lower Limit"


class MatmlVisitor(BaseVisitor):
    """MatmlVisitor."""

    _material_models: list[ET.Element]
    _metadata_property_sets: dict
    _metadata_parameters: dict
    _metadata_parameters_units: dict
    _metadata_property_sets_units: dict

    def __init__(self):
        """Initialize the class."""
        super().__init__()
        self._material_models = []
        self._metadata_parameters = {}
        self._metadata_property_sets = {}
        self._metadata_parameters_units = {}
        self._metadata_property_sets_units = {}

    def _get_property_id(self, property_name: str) -> str:
        """Get property id."""
        if property_name in self._metadata_property_sets.keys():
            property_id = self._metadata_property_sets[property_name]
        else:
            index = len(self._metadata_property_sets)
            property_id = PROPERTY_ID + str(index)
        return property_id

    def _get_parameter_id(self, parameter_name: str, unit: str | None = None) -> str:
        """Get parameter id."""
        if parameter_name in self._metadata_parameters.keys():
            parameter_id = self._metadata_parameters[parameter_name]
        else:
            index = len(self._metadata_parameters)
            parameter_id = PARAMETER_ID + str(index)
            if unit:
                if unit == "":
                    unit = UNITLESS_KEY
                self._metadata_parameters_units[parameter_name] = unit
        return parameter_id

    def _add_qualifier(self, data_element: ET.Element, qualifier_key: str, qualifier_value: str):
        """Add qualifier."""
        qualifier_element = ET.SubElement(data_element, QUALIFIER_KEY, {NAME_KEY: qualifier_key})
        qualifier_element.text = qualifier_value

    def _add_model_qualifiers(
        self, property_data_element: ET.Element, model_qualifiers: list[ModelQualifier] | None
    ) -> None:
        """Add model qualifiers."""
        if len(model_qualifiers) > 0:
            for model_qualifier in model_qualifiers:
                self._add_qualifier(property_data_element, model_qualifier)

    def _add_interpolation_options(
        self, property_data_element: ET.Element, interpolation_options: InterpolationOptions | None
    ) -> None:
        """Add interpolation options."""
        if interpolation_options:
            parameter_id = self._get_property_id(OPTIONS_VARIABLE_KEY)
            parameter_element = ET.SubElement(
                property_data_element,
                PARAMETER_VALUE_KEY,
                {PARAMETER_KEY: parameter_id, FORMAT_KEY: STRING_KEY},
            )
            data_element = ET.SubElement(parameter_element, DATA_KEY)
            data_element.text = INTERPOLATION_OPTIONS_KEY
            if interpolation_options.algorithm_type:
                self._add_qualifier(
                    parameter_element, ALGORITTHM_TYPE_KEY, interpolation_options.algorithm_type
                )
            if interpolation_options.cached:
                self._add_qualifier(
                    parameter_element, CACHED_KEY, str(interpolation_options.cached)
                )
            if interpolation_options.normalized:
                self._add_qualifier(
                    parameter_element, NORMALIZED_KEY, str(interpolation_options.normalized)
                )
            if interpolation_options.extrapolation_type:
                self._add_qualifier(
                    parameter_element,
                    EXTRAPOLATION_TYPE_KEY,
                    interpolation_options.extrapolation_type,
                )

    def _add_independent_parameters(
        self,
        property_data_element: ET.Element,
        independent_parameters: list[IndependentParameter] | None,
    ) -> None:
        """Add independent parameters."""
        if independent_parameters:
            for independent_parameter in independent_parameters:
                parameter_id = self._get_parameter_id(
                    independent_parameter.name, independent_parameter.values.unit
                )
                parameter_element = ET.SubElement(
                    property_data_element,
                    PARAMETER_VALUE_KEY,
                    {PARAMETER_KEY: parameter_id, FORMAT_KEY: FLOAT_KEY},
                )
                data_element = ET.SubElement(parameter_element, DATA_KEY)
                values = independent_parameter.values
                if isinstance(values, Quantity):
                    values = values.value
                values = ", ".join(f"{v}" for v in values)
                data_element.text = values
                qualifier_value = ",".join([INDEPENDENT_KEY] * len(values.split(",")))
                self._add_qualifier(parameter_element, VARIABLE_TYPE_KEY, qualifier_value)
                if independent_parameter.default_value:
                    qualifier_value = convert_to_float_string(independent_parameter.default_value)
                    self._add_qualifier(parameter_element, DEFAULT_DATA_KEY, qualifier_value)
                if independent_parameter.upper_limit:
                    qualifier_value = convert_to_float_string(independent_parameter.upper_limit)
                    self._add_qualifier(parameter_element, UPPER_LIMIT_KEY, qualifier_value)
                if independent_parameter.lower_limit:
                    qualifier_value = convert_to_float_string(independent_parameter.lower_limit)
                    self._add_qualifier(parameter_element, LOWER_LIMIT_KEY, qualifier_value)

    def _populate_dependent_parameters(
        self, dependent_names: list[str], material_model: MaterialModel
    ) -> dict[str, Quantity]:
        """Populate dependent parameters."""
        material_dict = material_model.model_dump()
        dependent_parameters = {}
        for key, value in material_dict.items():
            for dependent_name in dependent_names:
                if dependent_name == key:
                    dependent_parameters[key] = value
        return

    def _add_dependent_parameters(
        self, property_data_element: ET.Element, dependent_parameters: dict[str, Quantity]
    ):
        """Add dependent parameters."""
        for key in dependent_parameters.keys():
            unit = UNITLESS_KEY
            if not isinstance(dependent_parameters[key], (str | float | int)):
                unit = dependent_parameters[key].get("units", UNITLESS_KEY)
            self._get_parameter_id(key, unit)
            parameter_element = ET.SubElement(property_data_element)
            data_element = ET.SubElement(parameter_element, DATA_KEY)
            if isinstance(dependent_parameters[key], dict):
                if "value" in dependent_parameters[key].keys():
                    values = create_xml_string_value(dependent_parameters[key]["value"])
            else:
                if isinstance(dependent_parameters[key], str):
                    values = dependent_parameters[key]
                else:
                    values = create_xml_string_value(dependent_parameters[key])
            data_element.text = values
            qualifier_value = ",".join(["Dependent"] * len(values.split(",")))
            self._add_qualifier(parameter_element, VARIABLE_TYPE_KEY, qualifier_value)

    def _visit_material_model(
        self, property_id: str, dependent_names: list[str], material_model: MaterialModel
    ):
        """Visit material model."""
        property_data_element = ET.Element(PROPERTY_DATA_KEY, {PROPERTY_KEY: property_id})
        data_element = ET.SubElement(property_data_element, DATA_KEY, {FORMAT_KEY: STRING_KEY})
        data_element.text = DASH_KEY
        self._add_model_qualifiers(property_data_element, material_model.model_qualifiers)
        self._add_interpolation_options(property_data_element, material_model.interpolation_options)
        self._add_independent_parameters(
            property_data_element, material_model.independent_parameters
        )
        dependent_parameters = self._populate_dependent_parameters(dependent_names, material_model)
        self._add_dependent_parameters(property_data_element, dependent_parameters)
        self._material_models.append(property_data_element)

    def visit_density(self, material_model: Density):
        """Visit density."""
        property_id = self._get_property_id(DENSITY)
        depenent_names = [DENSITY]
        self._visit_material_model(property_id)

    def visit_elasticity(self, material_model: ElasticityIsotropic):
        """Visit elasticity."""
        property_id = self._get_property_id(ELASTICITY)
        dependent_names = [YOUNGS_MODULUS, POISSONS_RATIO]
        self._visit_material_model(property_id, dependent_names, material_model)
