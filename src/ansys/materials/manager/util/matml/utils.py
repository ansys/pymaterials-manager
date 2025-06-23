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

NOT_DEPENDENT_PARAMETER_FIELDS = [
    "name",
    "independent_parameters",
    "interpolation_options",
    "model_qualifiers",
    "supported_packages",
]


def xml_to_unit(param: ET.Element) -> tuple[str, dict[str, str]]:
    """Convert XML element to a unit string."""
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
                unit_parts.append(f"{name}{power}")
            else:
                unit_parts.append(name)
        entry["Units"] = "*".join(unit_parts)
    elif param.find("Unitless") is not None:
        entry["Units"] = "Unitless"

    return id, entry


def unit_to_xml(params, tag_name):
    """Convert a list of parameters to XML string. tag_name: ParameterDetails or PropertyDetails."""
    root = ET.Element("root")
    for param in params:
        pd = ET.SubElement(root, tag_name, id=param["id"])
        ET.SubElement(pd, "Name").text = param["name"]

        if param["unit"] == "unitless":
            ET.SubElement(pd, "Unitless")
        else:
            units = ET.SubElement(pd, "Units")
            if param["unit_name"]:
                units.set("name", param["unit_name"])
            for part in param["unit"].split("*"):
                name = "".join(filter(str.isalpha, part))
                power = "".join(filter(lambda x: x == "-" or x.isdigit(), part[len(name) :]))
                unit_elem = ET.SubElement(units, "Unit")
                if power:
                    unit_elem.set("power", power)
                ET.SubElement(unit_elem, "Name").text = name

    return ET.tostring(root, encoding="unicode")
