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

from dataclasses import dataclass
import os
from typing import BinaryIO, Dict, Optional, Sequence, Union
import xml.etree.ElementTree as ET

import ansys.units

from ansys.materials.manager._models._matml.property_info import (
    property_infos as matml_property_infos,
)
from ansys.materials.manager.material import Material

from .matml_parser import (
    BULKDATA_KEY,
    MATERIALS_ELEMENT_KEY,
    MATML_DOC_KEY,
    METADATA_KEY,
    NAME_ATTR,
    NAME_KEY,
    POWER_ATTR,
    UNIT_KEY,
    UNITLESS_KEY,
    UNITS_KEY,
    WBTRANSFER_KEY,
)
from .matml_property_map import MATML_PROPERTY_MAP

_PATH_TYPE = Union[str, os.PathLike]

ROOT_ELEMENT = "EngineeringData"
VERSION = "18.0.0.60"
VERSION_DATE = "29.08.2016 15:02:00"


@dataclass
class MetadataParameter:
    """Name of the parameter, for example pa74."""

    name: str

    """The material model name."""
    model_name: str

    """The parameter value unit."""
    unit: Optional[str]


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
    _metadata_parameters: Dict[str, MetadataParameter]

    def __init__(self, materials: Sequence[Material]):
        """Construct a Matml writer."""
        self._materials = materials
        self._metadata_property_sets = {}
        self._metadata_parameters = {}

    def _add_parameters(self, property_element: ET.Element, material: Material, parameters: Dict):
        # add the parameters of a property set to the tree
        for mat_key, matml_key in parameters.items():
            model = material.get_model_by_name(mat_key)
            assert len(model) == 1
            model = model[0]

            if matml_key in self._metadata_parameters.keys():
                para_key = self._metadata_parameters[matml_key]
            else:
                index = len(self._metadata_parameters) + 1
                para_key = MetadataParameter(f"pa{index}", model.name, model.unit)
                self._metadata_parameters[matml_key] = para_key

            param_element = ET.SubElement(
                property_element, "ParameterValue", {"format": "float", "parameter": para_key.name}
            )
            data_element = ET.SubElement(param_element, "Data")
            data_element.text = str(model.value)
            qualifier_element = ET.SubElement(param_element, "Qualifier", {"name": "Variable Type"})
            qualifier_element.text = "Dependent"

    def _add_property_set(
        self,
        bulkdata_element: ET.Element,
        material: Material,
        property_set_name: str,
        parameter_map: Dict,
        behavior: str,
    ):
        """Add the property set to the XML tree."""
        # check if at least one parameter is specified (case-insensitive)
        # and build a map from material to Matml properties
        available_mat_properties = [model.name.lower() for model in material.models]
        # print(available_mat_properties)
        property_set_parameters = {item: item for item in parameter_map["properties"]}
        for key, mapped_properties in parameter_map["mappings"].items():
            property_set_parameters.update({item: key for item in mapped_properties})

        # build final map with property name in MaterialManager to Matml
        parameters = {
            param: key
            for param, key in property_set_parameters.items()
            if param.lower() in available_mat_properties
        }

        if len(parameters) > 0:
            # get property id from metadata or add it if it does not exist yet
            if property_set_name in self._metadata_property_sets.keys():
                property_id = self._metadata_property_sets[property_set_name]
            else:
                index = len(self._metadata_property_sets) + 1
                property_id = f"pr{index}"
                self._metadata_property_sets[property_set_name] = property_id

            property_data_element = ET.SubElement(
                bulkdata_element, "PropertyData", {"property": property_id}
            )
            data_element = ET.SubElement(property_data_element, "Data", {"format": "string"})
            data_element.text = "-"
            if behavior:
                behavior_element = ET.SubElement(
                    property_data_element, "Qualifier", {"name": "Behavior"}
                )
                behavior_element.text = behavior

            if property_set_name == "Coefficient of Thermal Expansion":
                qualifier_element = ET.SubElement(
                    property_data_element, "Qualifier", {"name": "Definition"}
                )
                qualifier_element.text = "Secant"
            self._add_parameters(property_data_element, material, parameters)

    def _add_materials(self, materials_element: ET.Element):
        """Add the material data to the XML tree."""
        for material in self._materials:
            mat_element = ET.SubElement(materials_element, "Material")
            bulkdata_element = ET.SubElement(mat_element, BULKDATA_KEY)
            name_element = ET.SubElement(bulkdata_element, "Name")
            name_element.text = material.name

            for property_set_name, parameters in MATML_PROPERTY_MAP.items():
                # property sets are exported as orthotropic if it can have an isotropic or
                # orthotropic representation,
                if len(property_set_name.split("::")) in [2, 3]:
                    behavior = property_set_name.split("::")[1]
                else:
                    behavior = ""
                if behavior != "Isotropic":
                    self._add_property_set(
                        bulkdata_element,
                        material,
                        property_set_name.split("::")[0],
                        parameters,
                        behavior,
                    )

    def _write_unit(self, prop_element: ET.Element, value: MetadataParameter):
        """Write unit in one of the following valid forms.

        If there is a unit:
          <Units name="Density">
            <Unit>
              <Name>kg</Name>
            </Unit>
            <Unit power="-3">
              <Name>m</Name>
            </Unit>
          </Units>

        If there is a unit for a property with no unit category defined:
           <Units>
            <Unit>
              <Name>kg</Name>
            </Unit>
            <Unit power="-3">
              <Name>m</Name>
            </Unit>
          </Units>
        If there is no unit:
          <Unitless />
        """
        if value.unit is None:
            ET.SubElement(prop_element, UNITLESS_KEY)
        else:
            unit_tokens = value.unit.split(" ")
            matml_property_info = matml_property_infos[value.model_name]
            unit_category = matml_property_info.unit_category
            unit_name_dict = {}
            if unit_category is not None:
                unit_name_dict[NAME_ATTR] = unit_category
            units_element = ET.SubElement(prop_element, UNITS_KEY, unit_name_dict)
            for unit_token in unit_tokens:
                _, term, exp = ansys.units.unit._filter_unit_term(unit_token)
                power = int(exp)
                power_dict = {}
                if power != 1:
                    power_dict[POWER_ATTR] = str(power)
                unit_element = ET.SubElement(units_element, UNIT_KEY, power_dict)
                unit_name_element = ET.SubElement(unit_element, NAME_KEY)
                unit_name_element.text = term

    def _add_metadata(self, metadata_element: ET.Element):

        # add the metadata to the XML tree
        for key, value in self._metadata_property_sets.items():
            prop_element = ET.SubElement(metadata_element, "PropertyDetails", {"id": value})
            ET.SubElement(prop_element, UNITLESS_KEY)
            name_element = ET.SubElement(prop_element, "Name")
            name_element.text = key

        for key, value in self._metadata_parameters.items():
            prop_element = ET.SubElement(metadata_element, "ParameterDetails", {"id": value.name})

            name_element = ET.SubElement(prop_element, "Name")
            name_element.text = key

            self._write_unit(prop_element, value)

    def _add_transfer_ids(self, root: ET.Element) -> None:
        # add the WB transfer IDs to the XML tree
        wb_transfer_element = ET.SubElement(root, WBTRANSFER_KEY)
        materials_element = ET.SubElement(wb_transfer_element, MATERIALS_ELEMENT_KEY)
        any_uuid = False
        for mat in self._materials:
            if len(mat.uuid) > 0:
                any_uuid = True
                mat_element = ET.SubElement(materials_element, "Material")
                name_element = ET.SubElement(mat_element, "Name")
                name_element.text = mat.name
                transfer_element = ET.SubElement(mat_element, "DataTransferID")
                transfer_element.text = mat.uuid
        if not any_uuid:
            root.remove(wb_transfer_element)

    def _to_etree(
        self,
    ) -> ET.ElementTree:
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
