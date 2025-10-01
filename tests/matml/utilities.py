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

import xml.dom.minidom
import xml.etree.ElementTree as ET

from ansys.materials.manager.util.matml.matml_parser import MatmlReader
from ansys.materials.manager.util.matml.matml_to_material import convert_matml_materials


def read_matml_file(file_path):
    parsed_data = MatmlReader.parse_from_file(file_path)
    materials = convert_matml_materials(
        {k: v["material"] for k, v in parsed_data.items()},
        {k: v["transfer_id"] for k, v in parsed_data.items()},
        0,
    )
    return {material.name: material for material in materials}


def get_material_and_metadata_from_xml(tree):
    material = tree._root.find("Materials").find("MatML_Doc").find("Material")
    metadata = tree._root.find("Materials").find("MatML_Doc").find("Metadata")
    material_string = ET.tostring(material, encoding="utf-8").decode("utf-8")
    material_string = xml.dom.minidom.parseString(material_string)
    material_string = material_string.toprettyxml(indent="  ").strip()
    metadata_string = ET.tostring(metadata, encoding="utf-8").decode("utf-8")
    metadata_string = xml.dom.minidom.parseString(metadata_string)
    metadata_string = metadata_string.toprettyxml(indent="  ").strip()
    return material_string, metadata_string


def read_specific_material(file_path, mat_name):
    material_dic = read_matml_file(file_path)
    assert mat_name in material_dic.keys()
    return material_dic[mat_name]
