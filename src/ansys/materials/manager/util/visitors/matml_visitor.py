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

from typing import Optional
import xml.etree.ElementTree as ET

from ansys.units import Quantity

from ansys.materials.manager._models._common.independent_parameter import IndependentParameter
from ansys.materials.manager._models._common.interpolation_options import InterpolationOptions
from ansys.materials.manager._models._common.material_model import MaterialModel
from ansys.materials.manager._models._common.model_qualifier import ModelQualifier
from ansys.materials.manager._models._material_models.density import Density
from ansys.materials.manager._models._material_models.elasticity_anisotropic import (
    ElasticityAnisotropic,
)
from ansys.materials.manager._models._material_models.elasticity_isotropic import (
    ElasticityIsotropic,
)
from ansys.materials.manager._models._material_models.elasticity_orthotropic import (
    ElasticityOrthotropic,
)
from ansys.materials.manager._models.material import Material
from ansys.materials.manager.util.matml.matml_parser import _PATH_TYPE
from ansys.materials.manager.util.matml.utils import (
    convert_to_float_string,
    create_xml_string_value,
    unit_to_xml,
)
from ansys.materials.manager.util.visitors.base_visitor import BaseVisitor
from ansys.materials.manager.util.visitors.common import ModelInfo
from ansys.materials.manager.util.visitors.matml_utils import map_anisotropic_elasticity

from . import matml_strings as matml_strings

MATERIAL_MODEL_MAP = {
    Density: ModelInfo(labels=["Density"], attributes=["density"]),
    ElasticityIsotropic: ModelInfo(
        labels=["Young's Modulus", "Poisson's Ratio"],
        attributes=["youngs_modulus", "poissons_ratio"],
    ),
    ElasticityOrthotropic: ModelInfo(
        labels=[
            "Young's Modulus X direction",
            "Young's Modulus Y direction",
            "Young's Modulus Z direction",
            "Shear Modulus XY",
            "Shear Modulus YZ",
            "Shear Modulus XZ",
            "Poisson's Ratio XY",
            "Poisson's Ratio YZ",
            "Poisson's Ratio XZ",
        ],
        attributes=[
            "youngs_modulus_x",
            "youngs_modulus_y",
            "youngs_modulus_z",
            "shear_modulus_xy",
            "shear_modulus_yz",
            "shear_modulus_xz",
            "poissons_ratio_xy",
            "poissons_ratio_yz",
            "poissons_ratio_xz",
        ],
    ),
    ElasticityAnisotropic: ModelInfo(
        labels=[
            "D[*,1]",
            "D[*,2]",
            "D[*,3]",
            "D[*,4]",
            "D[*,5]",
            "D[*,6]",
        ],
        attributes=[
            "c_11",
            "c_12",
            "c_13",
            "c_14",
            "c_15",
            "c_16",
            "c_22",
            "c_23",
            "c_24",
            "c_25",
            "c_26",
            "c_33",
            "c_34",
            "c_35",
            "c_36",
            "c_44",
            "c_45",
            "c_46",
            "c_55",
            "c_56",
            "c_66",
        ],
        method=map_anisotropic_elasticity,
    ),
}


class MatmlVisitor(BaseVisitor):
    """MatmlVisitor."""

    _metadata_property_sets: dict
    _metadata_parameters: dict
    _metadata_parameters_units: dict
    _metadata_property_sets_units: dict

    def __init__(self, materials: list[Material]):
        """Initialize the class."""
        super().__init__(materials=materials)
        self._metadata_parameters = {}
        self._metadata_property_sets = {}
        self._metadata_parameters_units = {}
        self._metadata_property_sets_units = {}
        self.visit_materials()

    def _get_property_id(self, property_name: str) -> str:
        """Get property id."""
        if property_name in self._metadata_property_sets.keys():
            property_id = self._metadata_property_sets[property_name]
        else:
            index = len(self._metadata_property_sets)
            property_id = matml_strings.PROPERTY_ID + str(index)
            self._metadata_property_sets[property_name] = property_id
        return property_id

    def _get_parameter_id(self, parameter_name: str, unit: str | None = None) -> str:
        """Get parameter id."""
        if parameter_name in self._metadata_parameters.keys():
            parameter_id = self._metadata_parameters[parameter_name]
        else:
            index = len(self._metadata_parameters)
            parameter_id = matml_strings.PARAMETER_ID + str(index)
            self._metadata_parameters[parameter_name] = parameter_id
            if unit:
                if unit == "":
                    unit = matml_strings.UNITLESS_KEY
                self._metadata_parameters_units[parameter_name] = unit
        return parameter_id

    def _add_qualifier(
        self, data_element: ET.Element, qualifier_key: str, qualifier_value: str
    ) -> None:
        """Add qualifier."""
        qualifier_element = ET.SubElement(
            data_element, matml_strings.QUALIFIER_KEY, {matml_strings.NAME_KEY: qualifier_key}
        )
        qualifier_element.text = qualifier_value

    def _add_model_qualifiers(
        self, property_data_element: ET.Element, model_qualifiers: list[ModelQualifier] | None
    ) -> None:
        """Add model qualifiers."""
        if len(model_qualifiers) > 0:
            for model_qualifier in model_qualifiers:
                self._add_qualifier(
                    property_data_element, model_qualifier.name, model_qualifier.value
                )

    def _add_interpolation_options(
        self, property_data_element: ET.Element, interpolation_options: InterpolationOptions | None
    ) -> None:
        """Add interpolation options."""
        if interpolation_options:
            parameter_id = self._get_property_id(matml_strings.OPTIONS_VARIABLE_KEY)
            parameter_element = ET.SubElement(
                property_data_element,
                matml_strings.PARAMETER_VALUE_KEY,
                {
                    matml_strings.PARAMETER_KEY: parameter_id,
                    matml_strings.FORMAT_KEY: matml_strings.STRING_KEY,
                },
            )
            data_element = ET.SubElement(parameter_element, matml_strings.DATA_KEY)
            data_element.text = matml_strings.INTERPOLATION_OPTIONS_KEY
            if interpolation_options.algorithm_type:
                self._add_qualifier(
                    parameter_element,
                    matml_strings.ALGORITTHM_TYPE_KEY,
                    interpolation_options.algorithm_type,
                )
            if interpolation_options.cached:
                self._add_qualifier(
                    parameter_element, matml_strings.CACHED_KEY, str(interpolation_options.cached)
                )
            if interpolation_options.normalized:
                self._add_qualifier(
                    parameter_element,
                    matml_strings.NORMALIZED_KEY,
                    str(interpolation_options.normalized),
                )
            if interpolation_options.extrapolation_type:
                self._add_qualifier(
                    parameter_element,
                    matml_strings.EXTRAPOLATION_TYPE_KEY,
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
                    matml_strings.PARAMETER_VALUE_KEY,
                    {
                        matml_strings.PARAMETER_KEY: parameter_id,
                        matml_strings.FORMAT_KEY: matml_strings.FLOAT_KEY,
                    },
                )
                data_element = ET.SubElement(parameter_element, matml_strings.DATA_KEY)
                values = independent_parameter.values
                if isinstance(values, Quantity):
                    values = values.value
                values = ", ".join(f"{v}" for v in values)
                data_element.text = values
                qualifier_value = ",".join([matml_strings.INDEPENDENT_KEY] * len(values.split(",")))
                self._add_qualifier(
                    parameter_element, matml_strings.VARIABLE_TYPE_KEY, qualifier_value
                )
                if independent_parameter.default_value:
                    qualifier_value = convert_to_float_string(independent_parameter.default_value)
                    self._add_qualifier(
                        parameter_element, matml_strings.DEFAULT_DATA_KEY, qualifier_value
                    )
                if independent_parameter.upper_limit:
                    qualifier_value = convert_to_float_string(independent_parameter.upper_limit)
                    self._add_qualifier(
                        parameter_element, matml_strings.UPPER_LIMIT_KEY, qualifier_value
                    )
                if independent_parameter.lower_limit:
                    qualifier_value = convert_to_float_string(independent_parameter.lower_limit)
                    self._add_qualifier(
                        parameter_element, matml_strings.LOWER_LIMIT_KEY, qualifier_value
                    )

    def _populate_dependent_parameters(self, material_model: MaterialModel) -> dict[str, Quantity]:
        """Populate dependent parameters."""
        if material_model.__class__ in MATERIAL_MODEL_MAP.keys():
            mapping = MATERIAL_MODEL_MAP[material_model.__class__]
            labels = mapping.labels
            if mapping.method:
                quantities = mapping.method(material_model)
            else:
                quantities = [getattr(material_model, label) for label in mapping.attributes]
            return dict(zip(labels, quantities))

    def _add_dependent_parameters(
        self, property_data_element: ET.Element, dependent_parameters: dict[str, Quantity]
    ) -> None:
        """Add dependent parameters."""
        for key in dependent_parameters.keys():
            if dependent_parameters[key]:
                unit = matml_strings.UNITLESS_KEY
                if not isinstance(dependent_parameters[key], (str | float | int)):
                    if hasattr(dependent_parameters[key], "unit"):
                        unit = dependent_parameters[key].unit
                    else:
                        unit = matml_strings.UNITLESS_KEY
                parameter_id = self._get_parameter_id(key, unit)
                parameter_element = ET.SubElement(
                    property_data_element,
                    matml_strings.PARAMETER_VALUE_KEY,
                    {
                        matml_strings.PARAMETER_KEY: parameter_id,
                        matml_strings.FORMAT_KEY: matml_strings.FLOAT_KEY,
                    },
                )
                data_element = ET.SubElement(parameter_element, matml_strings.DATA_KEY)
                if isinstance(dependent_parameters[key], Quantity):
                    if hasattr(dependent_parameters[key], "value"):
                        values = create_xml_string_value(dependent_parameters[key].value)
                else:
                    if isinstance(dependent_parameters[key], str):
                        values = dependent_parameters[key]
                    else:
                        values = create_xml_string_value(dependent_parameters[key])
                data_element.text = values
                qualifier_value = ",".join([matml_strings.DEPENDENT_KEY] * len(values.split(",")))
                self._add_qualifier(
                    parameter_element, matml_strings.VARIABLE_TYPE_KEY, qualifier_value
                )

    def _visit_model(self, property_id: str, material_model: MaterialModel) -> ET.Element:
        """Visit material model."""
        property_data_element = ET.Element(
            matml_strings.PROPERTY_DATA_KEY, {matml_strings.PROPERTY_KEY: property_id}
        )
        data_element = ET.SubElement(
            property_data_element,
            matml_strings.DATA_KEY,
            {matml_strings.FORMAT_KEY: matml_strings.STRING_KEY},
        )
        data_element.text = matml_strings.DASH_KEY
        self._add_model_qualifiers(property_data_element, material_model.model_qualifiers)
        self._add_interpolation_options(property_data_element, material_model.interpolation_options)
        dependent_parameters = self._populate_dependent_parameters(material_model)
        self._add_dependent_parameters(property_data_element, dependent_parameters)
        self._add_independent_parameters(
            property_data_element, material_model.independent_parameters
        )

        return property_data_element

    def _add_metadata(self, metadata_element: ET.Element) -> None:
        """Add the metadata to the XML tree."""
        for key, value in self._metadata_property_sets.items():
            prop_element = ET.SubElement(
                metadata_element, matml_strings.PROPERTY_DETAILS_KEY, {matml_strings.ID_KEY: value}
            )
            ET.SubElement(prop_element, matml_strings.UNITLESS_KEY)
            name_element = ET.SubElement(prop_element, matml_strings.NAME_KEY.capitalize())
            name_element.text = key
        for key, value in self._metadata_parameters.items():
            prop_element = ET.SubElement(
                metadata_element, matml_strings.PARAMETER_DETAILS_KEY, {matml_strings.ID_KEY: value}
            )
            units = self._metadata_parameters_units.get(key, None)
            if units:
                prop_element.append(unit_to_xml(units))
            else:
                ET.SubElement(prop_element, matml_strings.UNITLESS_KEY)
            name_element = ET.SubElement(prop_element, matml_strings.NAME_KEY.capitalize())
            name_element.text = key

    def _add_transfer_ids(self, root: ET.Element) -> None:
        """Add the WB transfer IDs to the XML tree."""
        wb_transfer_element = ET.SubElement(root, matml_strings.WBTRANSFER_KEY)
        materials_element = ET.SubElement(wb_transfer_element, matml_strings.MATERIALS_ELEMENT_KEY)
        any_uuid = False
        for mat in self._materials:
            if mat.guid is not None:
                mat_element = ET.SubElement(
                    materials_element, matml_strings.MATERIAL_KEY.capitalize()
                )
                name_element = ET.SubElement(mat_element, matml_strings.NAME_KEY.capitalize())
                name_element.text = mat.name
                transfer_element = ET.SubElement(mat_element, matml_strings.DATA_TRANSFER_ID_KEY)
                transfer_element.text = mat.guid
                any_uuid = True
        if not any_uuid:
            root.remove(wb_transfer_element)

    def _to_etree(self) -> ET.ElementTree:
        """To element tree."""
        root = ET.Element(matml_strings.ROOT_ELEMENT)
        tree = ET.ElementTree(root)
        root.attrib["version"] = matml_strings.VERSION
        root.attrib["versiondate"] = matml_strings.VERSION_DATE
        notes_element = ET.SubElement(root, matml_strings.NOTES_KEY)
        notes_element.text = matml_strings.NOTES_TEXT
        materials_element = ET.SubElement(root, matml_strings.MATERIALS_ELEMENT_KEY)
        matml_doc_element = ET.SubElement(materials_element, matml_strings.MATML_DOC_KEY)
        for material_name, material in self._material_repr.items():
            material_element = ET.SubElement(
                matml_doc_element, matml_strings.MATERIAL_KEY.capitalize()
            )
            bulkdata_element = ET.SubElement(material_element, matml_strings.BULK_DETAILS_KEY)
            name_element = ET.SubElement(bulkdata_element, matml_strings.NAME_KEY.capitalize())
            name_element.text = material_name
            for material_model_element in self._material_repr[material_name]:
                if material_model_element:
                    bulkdata_element.append(material_model_element)
        metadata_element = ET.SubElement(matml_doc_element, matml_strings.METADATA_KEY)
        self._add_metadata(metadata_element)
        self._add_transfer_ids(root)
        return tree

    def _indent(self, tree: ET.ElementTree) -> None:
        """Indent."""
        if hasattr(ET, "indent"):
            ET.indent(tree)
        else:
            print(f"ElementTree does not have `indent`. Python 3.9+ required!")

    def visit_material_model(self, material_name: str, material_model: MaterialModel) -> ET.Element:
        """Visit the material model."""
        material_element = None
        property_id = self._get_property_id(material_model.name)
        material_element = self._visit_model(property_id, material_model)
        self._material_repr[material_name].append(material_element)
        return material_element

    def write(
        self,
        path: _PATH_TYPE,
        indent: Optional[bool] = False,
        xml_declaration: Optional[bool] = False,
    ) -> None:
        """
        Write a MatML (engineering data XML format) representation of materials to file.

        Parameters
        ----------
        path:
            File path.
        indent : Optional[bool]
            Whether to add an indent to format the XML output.
            Defaults to ``false``.
        xml_declaration: Optional[bool]
            Whether to add the XML declaration to the output.
        """
        tree = self._to_etree()
        print(f"write xml to {path}")
        if indent:
            self._indent(tree)
        tree.write(path, xml_declaration=xml_declaration)
