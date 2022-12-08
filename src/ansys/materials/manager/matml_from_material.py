from collections.abc import Iterable
from typing import Dict, Sequence, Union, Tuple
import os

from .material import Material
from .property_codes import PropertyCode
from .matml_property_map import MATML_PROPERTY_MAP
from .matml_parser import (Parameter,
                           PropertySet,
                           MATERIALS_ELEMENT_KEY,
                           MATML_DOC_KEY,
                           METADATA_KEY,
                           BULKDATA_KEY,
                           UNITLESS_KEY
                           )
import xml.etree.ElementTree as ET

_PATH_TYPE = Union[str, os.PathLike]

ROOT_ELEMENT = "EngineeringData"
VERSION = "18.0.0.60"
VERSION_DATE = "29.08.2016 15:02:00"

# todo: convert into class

def _inverse_property_map(properties_map: Dict) -> Dict:
    inverse_map = {}
    for key, prop_codes in properties_map.items():
        for prop in prop_codes:
            inverse_map[prop] = key

    return inverse_map
def _add_parameters(property_element: ET.Element,
                    material: Material,
                    parameters: Sequence[PropertyCode],
                    properties_map: Dict,
                    metadata_parameters: Dict):
    # add the parameters of a property set to the tree

    prop_to_matml_map = _inverse_property_map(properties_map)

    for prop_code in parameters:
        matml_key = prop_to_matml_map[prop_code]
        if matml_key in metadata_parameters.keys():
            para_key = metadata_parameters[matml_key]
        else:
            index = len(metadata_parameters) + 1
            para_key = f"pa{index}"
            metadata_parameters[matml_key] = para_key

        param_element = ET.SubElement(property_element,
                                      "ParameterValue",
                                      {"parameter": para_key, "format": "float"}
                                      )
        data_element = ET.SubElement(param_element, "Data")
        data_element.text = str(material.get_property(prop_code))
        qualifier_element = ET.SubElement(param_element, "Qualifier",  {"name": "Variable Type"})
        qualifier_element.text = "Dependent"


def _add_property_set(bulkdata_element: ET.Element,
                      material: Material,
                      property_map: Tuple,
                      behavior: str,
                      metadata_properties: Dict,
                      metadata_parameters: Dict):
    """Add the property set to the XML tree"""

    # check if at least one parameter is specified
    available_mat_properties = material.get_properties()
    available_prop_codes = available_mat_properties.keys()
    parameters_map = property_map[1]
    property_set_parameters = [v[0] for k, v in parameters_map.items()]

    # check if at least one parameter is specified
    parameters = list(set(property_set_parameters) & set(available_prop_codes))
    if len(parameters) > 0:
        property_set_name = property_map[0].split("::")[0]
        # get property id from metadata or add it if it does not exist yet
        if property_set_name in metadata_properties.keys():
            property_id = metadata_properties[property_set_name]
        else:
            index = len(metadata_properties) + 1
            property_id = f"pr{index}"
            metadata_properties[property_set_name] = property_id

        property_data_element = ET.SubElement(bulkdata_element, "PropertyData", {"property": property_id})
        data_element = ET.SubElement(property_data_element, "Data", {"format": "string"})
        data_element.text = "-"
        if behavior:
            behavior_element = ET.SubElement(property_data_element, "Qualifier", {"name": "Behavior"})
            behavior_element.text = behavior

        _add_parameters(property_data_element, material, parameters, parameters_map, metadata_parameters)

def _add_materials(materials: Sequence[Material],
                   materials_element: ET.Element,
                   metadata_properties: Dict,
                   metadata_parameters: Dict):
    """Add the material data to the XML tree"""

    for material in materials:
        mat_element = ET.SubElement(materials_element, "Material")
        bulkdata_element = ET.SubElement(mat_element, BULKDATA_KEY)
        name_element = ET.SubElement(bulkdata_element, "Name")
        name_element.text = material.name

        for property in MATML_PROPERTY_MAP.items():
            # property sets are exported as orthotropic if it can have an isotropic or orthotropic representation,
            if len(property[0].split("::")) == 2:
                behavior = property[0].split("::")[1]
            else:
                behavior = ""
            if behavior != "Isotropic":
                _add_property_set(bulkdata_element,
                                  material,
                                  property,
                                  behavior,
                                  metadata_properties, metadata_parameters)


def _add_metadata(metadata_element: ET.Element,
                  property_set_dict: Dict,
                  parameter_set_dict: Dict):
    # add the metadata to the XML tree
    for key, value in property_set_dict.items():
        prop_element = ET.SubElement(metadata_element, "PropertyDetails", {"id": value})
        ET.SubElement(prop_element, UNITLESS_KEY)
        name_element = ET.SubElement(prop_element, "Name")
        name_element.text = key

    for key, value in parameter_set_dict.items():
        prop_element = ET.SubElement(metadata_element, "ParameterDetails", {"id": value})
        ET.SubElement(prop_element, UNITLESS_KEY)
        name_element = ET.SubElement(prop_element, "Name")
        name_element.text = key



def write_matml(path: _PATH_TYPE,
                materials: Sequence[Material]):
    """
    Write a Matml (engineering data xml file from scratch)

    Parameters
    ----------
    path:
        File path
    materials:
        list of materials
    """
    root = ET.Element(ROOT_ELEMENT)
    tree = ET.ElementTree(root)

    root.attrib["version"] = VERSION
    root.attrib["versiondate"] = VERSION_DATE
    notes_element = ET.SubElement(root, "Notes")
    notes_element.text = "Engineering data xml file generated by pyMaterials."

    materials_element = ET.SubElement(root, MATERIALS_ELEMENT_KEY)
    matml_doc_element = ET.SubElement(materials_element, MATML_DOC_KEY)

    metadata_property_set = {}
    metadata_parameters = {}

    _add_materials(materials, matml_doc_element, metadata_property_set, metadata_parameters)

    metadata_element = ET.SubElement(matml_doc_element, METADATA_KEY)
    _add_metadata(metadata_element, metadata_property_set, metadata_parameters)

    print(f"write xml to {path}")
    tree.write(path)
