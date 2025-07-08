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

import re
from typing import Dict, Sequence
import xml.etree.ElementTree as ET


def parse_unit_string(unit_str: str) -> list[tuple[str, int]]:
    """Parse a unit string into a list of tuples."""
    if unit_str.strip().lower() == "unitless":
        return [("Unitless", 1)]

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
    id = param.attrib.get("id", "")
    entry = {"Name": param.findtext("Name", ""), "UnitsName": "", "Units": ""}
    units = param.find("Units")
    if units is not None:
        entry["UnitsName"] = units.attrib.get("name", "")
        unit_parts = []
        for unit in units.findall("Unit"):
            name = unit.findtext("Name", "")
            power = unit.attrib.get("power")
            if power:
                unit_parts.append(f"{name}^{power}")
            else:
                unit_parts.append(name)
        entry["Units"] = " ".join(unit_parts)
    elif param.find("Unitless") is not None:
        entry["Units"] = "Unitless"
    return id, entry


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

    if unit_list and unit_list[0][0].lower() == "unitless":
        return ET.Element("Unitless")

    units = ET.Element("Units")

    for unit_name, power in unit_list:
        attribs = {"power": str(power)} if power != 1 else {}
        unit_elem = ET.SubElement(units, "Unit", attrib=attribs)
        name_elem = ET.SubElement(unit_elem, "Name")
        name_elem.text = unit_name

    return units


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


def get_data_and_unit(param: Dict) -> tuple[list[float | int], str]:
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
    if units == "Unitless":
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
