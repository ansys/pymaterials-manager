# Copyright (C) 2022 - 2026 ANSYS, Inc. and/or its affiliates.
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

from dataclasses import dataclass
import re
from typing import Any, Sequence, Union
import uuid
import xml.etree.ElementTree as ET

from ansys.units import Quantity

from ansys.materials.manager._models._common.independent_parameter import IndependentParameter
from ansys.materials.manager._models._common.interpolation_options import InterpolationOptions
from ansys.materials.manager._models._common.model_qualifier import ModelQualifier
from ansys.materials.manager.parsers.matml import _matml_strings as matml_strings

MODEL_NAMESPACE = "ansys.materials.manager._models._material_models."


@dataclass
class Parameter:
    """Define a parameter such as density or Young's Modulus."""

    name: str
    data: Any
    qualifiers: dict
    unit: str
    unit_name: str


@dataclass
class PropertySet:
    """Define a PropertySet which contains one or several parameters."""

    name: str
    parameters: dict
    qualifiers: dict
    unit: str
    unit_name: str


def convert(data: str, target: str) -> Union[str, float, list[float]]:
    """
    Convert data to the target format.

    Parameters
    ----------
    data : str
        The data to convert.
    target : str
        The target format. Supported formats are "string" and "float".

    Returns
    -------
    Union[str, float, list[float]]
        The converted data.
    """
    if target == "string":
        return data

    if target != "float":
        raise RuntimeError(f"unsupported format {target}. Skipped formatting {data}")

    if not data or not data.strip():
        return 0.0

    if data.count(",") > 0:
        data = data.split(",")
        return [float(v) for v in data]
    else:
        return float(data)


def xml_to_unit(param: ET.Element) -> tuple[str, dict[str, str]]:
    """
    Convert XML element to a unit string.

    Parameters
    ----------
    param : ET.Element
        The XML element containing the unit information.

    Returns
    -------
    tuple[str, dict[str, str]]
        A tuple containing the unit ID and a dictionary with unit details.
    """
    id = param.attrib.get(matml_strings.ID_KEY, "")
    entry = {
        matml_strings.NAME_KEY.capitalize(): param.findtext(
            matml_strings.NAME_KEY.capitalize(), ""
        ),
        matml_strings.UNITS_NAME_KEY: "",
        matml_strings.UNITS_KEY: "",
    }
    units = param.find(matml_strings.UNITS_KEY)
    if units is not None:
        entry[matml_strings.UNITS_NAME_KEY] = units.attrib.get(matml_strings.NAME_KEY, "")
        unit_parts = []
        for unit in units.findall(matml_strings.UNIT_KEY):
            name = unit.findtext(matml_strings.NAME_KEY.capitalize(), "")
            power = unit.attrib.get(matml_strings.POWER_KEY)
            if power:
                unit_parts.append(f"{name}^{power}")
            else:
                unit_parts.append(name)
        entry[matml_strings.UNITS_KEY] = " ".join(unit_parts)
    elif param.find(matml_strings.UNITLESS_KEY) is not None:
        entry[matml_strings.UNITS_KEY] = matml_strings.UNITLESS_KEY
    return id, entry


def read_metadata(metadata_node: ET.Element) -> dict:
    """Read metadata from the given XML node.

    Parameters
    ----------
    metadata_node : ET.Element
        The XML node containing metadata information.

    Returns
    -------
    dict
        A dictionary containing metadata entries.
    """
    data = {}
    for item in metadata_node.iter(matml_strings.PARAMETER_DETAILS_KEY):
        id, entry = xml_to_unit(item)
        data[id] = entry

    for item in metadata_node.iter(matml_strings.PROPERTY_DETAILS_KEY):
        id, entry = xml_to_unit(item)
        data[id] = entry
    return data


def read_qualifiers(property_node: ET.Element) -> dict:
    """
    Read qualifiers from the given XML node.

    Parameters
    ----------
    property_node : ET.Element
        The XML node containing qualifier information.
    Returns
    -------
    dict
        A dictionary containing qualifier entries.
    """
    qualifiers = {}
    for item in property_node.findall(matml_strings.QUALIFIER_KEY):
        qualifiers[item.attrib[matml_strings.NAME_KEY]] = item.text
    return qualifiers


def read_property_sets_and_parameters(bulkdata: ET.Element, metadata_dict: dict) -> dict:
    """
    Read property sets and parameters from the given XML node.

    Parameters
    ----------
    bulkdata : ET.Element
        The XML node containing bulk data information.
    metadata_dict : dict
        A dictionary containing metadata entries.
    Returns
    -------
    dict
        A dictionary containing property sets.
    """
    prop_dict = {}

    # iterate over the property sets
    for prop_data in bulkdata.findall(matml_strings.PROPERTY_DATA_KEY):
        property_key = prop_data.attrib[matml_strings.PROPERTY_KEY]
        property_name = metadata_dict[property_key][matml_strings.NAME_KEY.capitalize()]
        property_unit = metadata_dict[property_key].get(matml_strings.UNITS_KEY, "")
        property_unit_name = metadata_dict[property_key].get(matml_strings.UNITS_NAME_KEY, "")
        prop_set_qualifiers = read_qualifiers(prop_data)

        parameters = {}

        # iterate over each parameter
        for parameter in prop_data.findall(matml_strings.PARAMETER_VALUE_KEY):
            parameter_key = parameter.attrib[matml_strings.PARAMETER_KEY]
            parameter_name = metadata_dict[parameter_key][matml_strings.NAME_KEY.capitalize()]
            parameter_format = parameter.attrib[matml_strings.FORMAT_KEY]
            param_qualifiers = read_qualifiers(parameter)
            param_units = metadata_dict[parameter_key].get(matml_strings.UNITS_KEY, "")
            param_units_name = metadata_dict[parameter_key].get(matml_strings.UNITS_NAME_KEY, "")
            data = convert(parameter.find(matml_strings.DATA_KEY).text, parameter_format)

            parameters[parameter_name] = Parameter(
                name=parameter_name,
                data=data,
                qualifiers=param_qualifiers,
                unit=param_units,
                unit_name=param_units_name,
            )

        prop_dict[property_name] = PropertySet(
            name=property_name,
            qualifiers=prop_set_qualifiers,
            parameters=parameters,
            unit=property_unit,
            unit_name=property_unit_name,
        )

    return prop_dict


def read_transfer_ids(root: ET.Element, materials: dict[str, dict]) -> dict[str, str]:
    """
    Read transfer IDs from the given XML root node.

    Parameters
    ----------
    root : ET.Element
        The XML root node.
    materials : dict[str, dict]
        A dictionary containing material entries.
    Returns
    -------
    dict[str, str]
        A dictionary mapping material names to their transfer IDs.
    """
    transfer_ids = {}
    wb_transfer_element = root.find(matml_strings.WBTRANSFER_KEY)
    if wb_transfer_element:
        materials_element = wb_transfer_element.find(matml_strings.MATERIALS_ELEMENT_KEY)
        for mat in materials_element.findall(matml_strings.MATERIAL_KEY.capitalize()):
            mat_name = mat.find(matml_strings.NAME_KEY.capitalize()).text
            transfer_id_element = mat.find(matml_strings.DATA_TRANSFER_ID_KEY)

            if not mat_name in materials.keys():
                raise RuntimeError(f"Transfer ID could not be set for material {mat_name}")
            if not transfer_id_element:
                transfer_ids[mat_name] = str(uuid.uuid4())
            transfer_ids[mat_name] = transfer_id_element.text
    else:
        for material in materials.keys():
            transfer_ids[material] = str(uuid.uuid4())
    return transfer_ids


def read_materials(matml_doc_node: ET.Element, metadata_dict: dict) -> dict:
    """
    Read materials from the given XML node.

    Parameters
    ----------
    matml_doc_node : ET.Element
        The XML node containing material information.
    metadata_dict : dict
        A dictionary containing metadata entries.
    Returns
    -------
    dict
        A dictionary containing material entries.
    """
    materials = {}
    for material in matml_doc_node.findall(matml_strings.MATERIAL_KEY.capitalize()):
        bulkdata = material.find(matml_strings.BULK_DETAILS_KEY)
        name = bulkdata.find(matml_strings.NAME_KEY.capitalize()).text
        data = read_property_sets_and_parameters(bulkdata, metadata_dict)
        materials[name] = data

    return materials


def parse_property_set_name(property_set_name):
    """
    Remove spaces, dashes and backslashes from the property set name.

    Parameters
    ----------
    property_set_name : str
        Property set name.

    Returns
    -------
    str
        the material model class name.
    """
    return property_set_name.replace(" ", "").replace("-", "").replace("/", "")


def get_data_and_unit(param: dict) -> tuple[list[float | int], str]:
    """
    Get data and unit from parameter.

    Parameters
    ----------
    param : Dict
        Parameter to parse.

    Returns
    -------
    tuple[list[float | int], str]
        Data and units.
    """
    units = param.unit
    if units == matml_strings.UNITLESS_KEY:
        units = ""
    data = param.data
    if not isinstance(data, Sequence):
        data = [data]
    return data, units


def create_xml_string_value(values: float | int | list[float | int]) -> str:
    """
    Extract the value for the xml.

    Parameters
    ----------
    values : float | int | list[float | int]
        Value to be parsed.

    Returns
    -------
    str
        Parsed value to add to xml data.
    """
    return ", ".join(f"{v}" for v in values)


def convert_to_float_or_keep(val: float | str | None) -> float | str | None:
    """
    Attempt to convert a string to float.

    Parameters
    ----------
    val : str | None
        The value to convert.
    Returns
    -------
    float | str | None
        - float if conversion succeeds
        - original string if conversion fails
        - None if input is None
    """
    if val is None:
        return None
    try:
        return float(val)
    except (ValueError, TypeError):
        return val


def convert_to_float_string(value: float | str) -> str:
    """
    Convert a float to string or keep it as it is otherwise.

    Parameters
    ----------
    value : float | str
        Value to be parsed.

    Returns
    -------
    str
        Parsed value.
    """
    return str(value).replace("e", "E") if type(value) == float else value


def get_material_model_name_and_qualifiers(
    property_set_name: str, property_set: dict
) -> tuple[str, list[ModelQualifier]]:
    """
    Get the material model class name and qualifiers.

    Parameters
    ----------
    property_set_name : str
        Property set name.
    property_set : dict
        Property set data.

    Returns
    -------
    tuple[str, list[ModelQualifier]]
        The material model class name and qualifiers.
    """
    cls_name = MODEL_NAMESPACE + parse_property_set_name(property_set_name)
    qualifiers = []
    for qualifier in property_set.qualifiers.keys():
        if qualifier == matml_strings.BEHAVIOR_KEY:
            cls_name += property_set.qualifiers[qualifier].replace(" ", "")
        qualifiers.append(ModelQualifier(name=qualifier, value=property_set.qualifiers[qualifier]))
    return cls_name, qualifiers


def fill_independent_parameter(param_value: Parameter) -> IndependentParameter:
    """
    Fill an IndependentParameter from a Parameter.

    Parameters
    ----------
    param_value : Parameter
        The parameter to convert.
    Returns
    -------
    IndependentParameter
        The converted IndependentParameter.
    """
    data, units = get_data_and_unit(param_value)
    independent_param = IndependentParameter(
        name=param_value.name,
        values=Quantity(value=data, units=units),
        default_value=convert_to_float_or_keep(
            param_value.qualifiers.get(matml_strings.DEFAULT_DATA_KEY, None)
        ),
        upper_limit=convert_to_float_or_keep(
            param_value.qualifiers.get(matml_strings.UPPER_LIMIT_KEY, None)
        ),
        lower_limit=convert_to_float_or_keep(
            param_value.qualifiers.get(matml_strings.LOWER_LIMIT_KEY, None)
        ),
    )
    return independent_param


def fill_interpolation_options(variable_options: dict) -> InterpolationOptions:
    """
    Fill InterpolationOptions from variable options.

    Parameters
    ----------
    variable_options : dict
        The variable options to convert.

    Returns
    -------
    InterpolationOptions
        The converted InterpolationOptions.
    """
    interpolation_options = InterpolationOptions(
        algorithm_type=variable_options.get(matml_strings.ALGORITHM_TYPE_KEY, ""),
        normalized=variable_options.get(matml_strings.NORMALIZED_KEY, True),
        cached=variable_options.get(matml_strings.CACHED_KEY, True),
        extrapolation_type=variable_options.get(matml_strings.EXTRAPOLATION_TYPE_KEY, "None"),
    )
    return interpolation_options


def parse_unit_string(unit_str: str) -> list[tuple[str, int]]:
    """Parse a unit string into a list of tuples."""
    if unit_str.strip().lower() == matml_strings.UNITLESS_KEY.lower():
        return [(matml_strings.UNITLESS_KEY, 1)]

    pattern = r"([a-zA-Z]+)(?:\^?(-?\d+))?"
    units = unit_str.split(" ")
    result = []

    for unit in units:
        match = re.fullmatch(pattern, unit.strip())
        if match:
            name = match.group(1)
            power = int(match.group(2)) if match.group(2) else 1
            result.append((name, power))
        else:
            raise ValueError(f"Invalid unit format: {unit}")

    return result


def unit_to_xml(unit: str) -> ET.Element:
    """
    Convert a unit string to an XML element.

    Parameters
    ----------
    unit : str
        The unit string to convert, e.g., "kg*m-3" or "Pa".

    Returns
    -------
    ET.Element
        An XML element representing the units.
    """
    unit_list = parse_unit_string(unit)

    if unit_list and unit_list[0][0].lower() == matml_strings.UNITLESS_KEY.lower():
        return ET.Element(matml_strings.UNITLESS_KEY)

    units = ET.Element(matml_strings.UNITS_KEY)

    for unit_name, power in unit_list:
        attribs = {matml_strings.POWER_KEY: str(power)} if power != 1 else {}
        unit_elem = ET.SubElement(units, matml_strings.UNIT_KEY, attrib=attribs)
        name_elem = ET.SubElement(unit_elem, matml_strings.NAME_KEY.capitalize())
        name_elem.text = unit_name

    return units
