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

"""Provides the ``MatmlWriter`` class."""

import os
from typing import BinaryIO, Dict, Optional, Sequence, Union
import xml.etree.ElementTree as ET

from ansys.materials.manager._models._common.independent_parameter import IndependentParameter
from ansys.materials.manager._models._common.interpolation_options import InterpolationOptions
from ansys.materials.manager._models._common.material_model import MaterialModel
from ansys.materials.manager.material import Material
from ansys.materials.manager.util.matml.property_to_model_field import PROPERTY_TO_MODEL_FIELD

from .matml_parser import (
    BULKDATA_KEY,
    MATERIALS_ELEMENT_KEY,
    MATML_DOC_KEY,
    METADATA_KEY,
    UNITLESS_KEY,
    WBTRANSFER_KEY,
)

_PATH_TYPE = Union[str, os.PathLike]

ROOT_ELEMENT = "EngineeringData"
VERSION = "18.0.0.60"
VERSION_DATE = "29.08.2016 15:02:00"


class MatmlWriter:
    """
    Exports a list of MAPDL materials to an engineering data XML file.

    Examples
    --------
    > writer = MatmlWriter(materials)
    > writer.export('engineering_data.xml')
    """

    _materials: Sequence[Material]
    _metadata_property_sets: Dict
    _metadata_parameters: Dict

    def __init__(self, materials: Sequence[Material]):
        """Construct a Matml writer."""
        self._materials = materials
        self._metadata_property_sets = {}
        self._metadata_parameters = {}

    def _add_dependent_parameters(
        self, property_element: ET.Element, models: Dict, parameters: Dict
    ):
        # add the parameters of a property set to the tree
        for mat_key, matml_key in parameters.items():
            if models[mat_key]:
                if matml_key in self._metadata_parameters.keys():
                    para_key = self._metadata_parameters[matml_key]
                else:
                    index = len(self._metadata_parameters)
                    para_key = f"pa{index}"
                    self._metadata_parameters[matml_key] = para_key

                param_element = ET.SubElement(
                    property_element, "ParameterValue", {"format": "float", "parameter": para_key}
                )

                data_element = ET.SubElement(param_element, "Data")
                values = str(models[mat_key]).strip("[]")
                data_element.text = values
                qualifier_element = ET.SubElement(
                    param_element, "Qualifier", {"name": "Variable Type"}
                )
                qualifier_element.text = ",".join(["Dependent"] * len(values.split(",")))

    def _add_interpolation_options(
        self, property_element, interpolation_options: InterpolationOptions
    ):
        if "Options Variable" in self._metadata_parameters.keys():
            parameter_id = self._metadata_parameters["Options Variable"]
        else:
            index = len(self._metadata_parameters)
            parameter_id = f"pa{index}"
            self._metadata_parameters["Options Variable"] = parameter_id
        param_element = ET.SubElement(
            property_element, "ParameterValue", {"format": "float", "parameter": parameter_id}
        )
        data_element = ET.SubElement(param_element, "Data")
        data_element.text = "Interpolation Options"
        if interpolation_options.algorithm_type:
            qualifier_element = ET.SubElement(param_element, "Qualifier", {"name": "AlgorithmType"})
            qualifier_element.text = interpolation_options.algorithm_type
        if interpolation_options.cached:
            qualifier_element = ET.SubElement(param_element, "Qualifier", {"name": "Cached"})
            qualifier_element.text = str(interpolation_options.cached)
        if interpolation_options.normalized:
            qualifier_element = ET.SubElement(param_element, "Qualifier", {"name": "Normalized"})
            qualifier_element.text = str(interpolation_options.normalized)
        if interpolation_options.extrapolation_type:
            qualifier_element = ET.SubElement(
                param_element, "Qualifier", {"name": "ExtrapolationType"}
            )
            qualifier_element.text = str(interpolation_options.extrapolation_type)

    def _add_independent_parameters(
        self, property_element: ET.Element, independent_parameters: list[IndependentParameter]
    ):
        for independent_parameter in independent_parameters:
            if independent_parameter.name in self._metadata_parameters.keys():
                parameter_id = self._metadata_parameters[independent_parameter.name]
            else:
                index = len(self._metadata_parameters)
                parameter_id = f"pa{index}"
                self._metadata_parameters[independent_parameter.name] = parameter_id

            param_element = ET.SubElement(
                property_element, "ParameterValue", {"format": "float", "parameter": parameter_id}
            )
            data_element = ET.SubElement(param_element, "Data")
            values = str(independent_parameter.values).strip("[]")
            data_element.text = values
            qualifier_element = ET.SubElement(param_element, "Qualifier", {"name": "Variable Type"})
            qualifier_element.text = ",".join(["Independent"] * len(values.split(",")))
            qualifier_element = ET.SubElement(
                param_element, "Qualifier", {"name": "Field Variable"}
            )
            qualifier_element.text = independent_parameter.name
            if independent_parameter.default_value:
                qualifier_element = ET.SubElement(
                    param_element, "Qualifier", {"name": "Default Data"}
                )
                qualifier_element.text = str(independent_parameter.default_value)
            if independent_parameter.units:
                qualifier_element = ET.SubElement(
                    param_element, "Qualifier", {"name": "Field Units"}
                )
                qualifier_element.text = independent_parameter.units
            if independent_parameter.upper_limit:
                qualifier_element = ET.SubElement(
                    param_element, "Qualifier", {"name": "Upper Limit"}
                )
                qualifier_element.text = independent_parameter.upper_limit
            if independent_parameter.lower_limit:
                qualifier_element = ET.SubElement(
                    param_element, "Qualifier", {"name": "Lower Limit"}
                )
                qualifier_element.text = independent_parameter.lower_limit

    def _add_material_model(
        self,
        bulkdata_element,
        material_model: MaterialModel,
        property_set_name: str,
    ):
        model_attributes = list(material_model.model_fields.keys())
        dependent_parameters = {
            model_attribute: PROPERTY_TO_MODEL_FIELD[model_attribute]
            for model_attribute in model_attributes
            if model_attribute in PROPERTY_TO_MODEL_FIELD.keys()
        }

        # for model_qualifier in model_qualifiers:
        if len(dependent_parameters) > 0:
            # get property id from metadata or add it if it does not exist yet
            if property_set_name in self._metadata_property_sets.keys():
                property_id = self._metadata_property_sets[property_set_name]
            else:
                index = len(self._metadata_property_sets)
                property_id = f"pr{index}"
                self._metadata_property_sets[property_set_name] = property_id

            property_data_element = ET.SubElement(
                bulkdata_element, "PropertyData", {"property": property_id}
            )
            data_element = ET.SubElement(property_data_element, "Data", {"format": "string"})
            data_element.text = "-"
            if len(material_model.model_qualifiers) > 0:
                for model_qualifier in material_model.model_qualifiers:
                    qualifier_element = ET.SubElement(
                        property_data_element, "Qualifier", {"name": model_qualifier.name}
                    )
                    qualifier_element.text = model_qualifier.value

            if material_model.interpolation_options:
                self._add_interpolation_options(
                    property_data_element, material_model.interpolation_options
                )
            self._add_dependent_parameters(
                property_data_element, material_model.model_dump(), dependent_parameters
            )
            if len(material_model.independent_parameters) > 0:
                self._add_independent_parameters(
                    property_data_element, material_model.independent_parameters
                )

    def _add_materials(self, materials_element: ET.Element):
        """Add the material data to the XML tree."""
        for material in self._materials:
            mat_element = ET.SubElement(materials_element, "Material")
            bulkdata_element = ET.SubElement(mat_element, BULKDATA_KEY)
            name_element = ET.SubElement(bulkdata_element, "Name")
            name_element.text = material.name
            for material_model in material.models:
                model_name = material_model.name
                self._add_material_model(
                    bulkdata_element,
                    material_model,
                    model_name,
                )

    def _add_metadata(self, metadata_element: ET.Element):
        # add the metadata to the XML tree
        for key, value in self._metadata_property_sets.items():
            prop_element = ET.SubElement(metadata_element, "PropertyDetails", {"id": value})
            ET.SubElement(prop_element, UNITLESS_KEY)
            name_element = ET.SubElement(prop_element, "Name")
            name_element.text = key

        for key, value in self._metadata_parameters.items():
            prop_element = ET.SubElement(metadata_element, "ParameterDetails", {"id": value})
            ET.SubElement(prop_element, UNITLESS_KEY)
            name_element = ET.SubElement(prop_element, "Name")
            name_element.text = key

    def _add_transfer_ids(self, root: ET.Element) -> None:
        # add the WB transfer IDs to the XML tree
        wb_transfer_element = ET.SubElement(root, WBTRANSFER_KEY)
        materials_element = ET.SubElement(wb_transfer_element, MATERIALS_ELEMENT_KEY)
        for mat in self._materials:
            mat_element = ET.SubElement(materials_element, "Material")
            name_element = ET.SubElement(mat_element, "Name")
            name_element.text = mat.name
            transfer_element = ET.SubElement(mat_element, "DataTransferID")
            transfer_element.text = mat.guid

    def _to_etree(self) -> ET.ElementTree:
        root = ET.Element(ROOT_ELEMENT)
        tree = ET.ElementTree(root)

        root.attrib["version"] = VERSION
        root.attrib["versiondate"] = VERSION_DATE
        notes_element = ET.SubElement(root, "Notes")
        notes_element.text = "Engineering data xml file generated by pyMaterials."

        materials_element = ET.SubElement(root, MATERIALS_ELEMENT_KEY)
        matml_doc_element = ET.SubElement(materials_element, MATML_DOC_KEY)

        self._add_materials(matml_doc_element)

        # add metadata to the XML tree
        metadata_element = ET.SubElement(matml_doc_element, METADATA_KEY)
        self._add_metadata(metadata_element)

        # add transfer id to the XML tree
        self._add_transfer_ids(root)
        return tree

    def _indent(self, tree) -> None:
        if hasattr(ET, "indent"):
            ET.indent(tree)
        else:
            print(f"ElementTree does not have `indent`. Python 3.9+ required!")

    def write(
        self,
        buffer: BinaryIO,
        indent: Optional[bool] = False,
        xml_declaration: Optional[bool] = False,
    ) -> None:
        """
        Write a MatML (engineering data XML format) representation of materials to buffer.

        Parameters
        ----------
        buffer:
            Buffer to write to.
        indent : Optional[bool]
            Whether to add an indent to format the XML output.
            Defaults to ``false``.
        xml_declaration: Optional[bool]
            Whether to add the XML declaration to the output.
        """
        tree = self._to_etree()

        if indent:
            self._indent(tree)
        buffer.write(ET.tostring(tree.getroot(), xml_declaration=xml_declaration))

    def export(
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
