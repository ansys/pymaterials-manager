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

import os
from pathlib import Path

# import xml.dom.minidom
import xml.etree.ElementTree as ET

from utilities import read_matml_file

from ansys.materials.manager._models._common.independent_parameter import IndependentParameter
from ansys.materials.manager._models._material_models.density import Density
from ansys.materials.manager._models.material import Material
from ansys.materials.manager.util.matml.matml_from_material import MatmlWriter

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
XML_FILE_PATH = os.path.join(DIR_PATH, "..", "data", "MatML_unittest_density.xml")

MATERIAL_WITH_CONSTANT_DENSITY_PROP = """<Material><BulkDetails><Name>material with density</Name><PropertyData property="pr0"><Data format="string">-</Data><ParameterValue format="float" parameter="pa0"><Data>1.34</Data><Qualifier name="Variable Type">Dependent</Qualifier></ParameterValue><ParameterValue format="float" parameter="pa1"><Data>7.88860905221012e-31</Data><Qualifier name="Variable Type">Independent</Qualifier><Qualifier name="Field Variable">Temperature</Qualifier></ParameterValue></PropertyData></BulkDetails></Material>"""  # noqa: E501
MATERIAL_WITH_CONSTANT_DENSITY_METADATA = """<Metadata><PropertyDetails id="pr0"><Unitless /><Name>Density</Name></PropertyDetails><ParameterDetails id="pa0"><Unitless /><Name>Density</Name></ParameterDetails><ParameterDetails id="pa1"><Unitless /><Name>Temperature</Name></ParameterDetails></Metadata>"""  # noqa: E501
MATERIAL_WITH_VARIABLE_DENSITY_PROP = """<Material><BulkDetails><Name>material variable with density</Name><PropertyData property="pr0"><Data format="string">-</Data><ParameterValue format="float" parameter="pa0"><Data>12.0, 32.0, 38.0</Data><Qualifier name="Variable Type">Dependent,Dependent,Dependent</Qualifier></ParameterValue><ParameterValue format="float" parameter="pa1"><Data>20.0, 21.0, 23.0</Data><Qualifier name="Variable Type">Independent,Independent,Independent</Qualifier><Qualifier name="Field Variable">Temperature</Qualifier></ParameterValue></PropertyData></BulkDetails></Material>"""  # noqa: E501
MATERIAL_WITH_VARIABLE_DENSITY_METADATA = """<Metadata><PropertyDetails id="pr0"><Unitless /><Name>Density</Name></PropertyDetails><ParameterDetails id="pa0"><Unitless /><Name>Density</Name></ParameterDetails><ParameterDetails id="pa1"><Unitless /><Name>Temperature</Name></ParameterDetails></Metadata>"""  # noqa: E501


def test_read_material_with_constant_density():
    material_dic = read_matml_file(XML_FILE_PATH)
    assert "material with density" in material_dic.keys()
    constant_density_material = material_dic["material with density"]
    assert len(constant_density_material.models) == 2
    density = constant_density_material.models[1]
    assert density.name == "Density"
    assert density.density == [1.34]
    assert len(density.independent_parameters) == 1
    assert density.independent_parameters[0].name == "Temperature"
    assert density.independent_parameters[0].values == [7.88860905221012e-31]


def test_read_model_with_variable_density():
    material_dic = read_matml_file(XML_FILE_PATH)
    assert "material with variable density" in material_dic.keys()
    variable_density_material = material_dic["material with variable density"]
    assert len(variable_density_material.models) == 2
    density = variable_density_material.models[1]
    assert density.name == "Density"
    assert density.density == [12.0, 32.0, 38.0]
    assert len(density.independent_parameters) == 1
    assert density.independent_parameters[0].name == "Temperature"
    assert density.independent_parameters[0].values == [
        20.0,
        21.0,
        23.0,
    ]


def test_write_material_with_constant_density():
    materials = [
        Material(
            name="material with density",
            models=[
                Density(
                    density=[1.34],
                    independent_parameters=[
                        IndependentParameter(name="Temperature", values=[7.88860905221012e-31])
                    ],
                ),
            ],
        )
    ]

    writer = MatmlWriter(materials)
    tree = writer._to_etree()
    material = tree._root.find("Materials").find("MatML_Doc").find("Material")
    metadata = tree._root.find("Materials").find("MatML_Doc").find("Metadata")
    material_string = ET.tostring(material, encoding="utf-8").decode("utf-8")
    metadata_string = ET.tostring(metadata, encoding="utf-8").decode("utf-8")
    assert material_string == MATERIAL_WITH_CONSTANT_DENSITY_PROP
    assert metadata_string == MATERIAL_WITH_CONSTANT_DENSITY_METADATA


def test_write_model_with_variable_density():
    materials = [
        Material(
            name="material variable with density",
            models=[
                Density(
                    density=[12.0, 32.0, 38.0],
                    independent_parameters=[
                        IndependentParameter(name="Temperature", values=[20.0, 21.0, 23.0])
                    ],
                ),
            ],
        )
    ]

    writer = MatmlWriter(materials)
    tree = writer._to_etree()
    material = tree._root.find("Materials").find("MatML_Doc").find("Material")
    metadata = tree._root.find("Materials").find("MatML_Doc").find("Metadata")
    material_string = ET.tostring(material, encoding="utf-8").decode("utf-8")
    metadata_string = ET.tostring(metadata, encoding="utf-8").decode("utf-8")
    assert material_string == MATERIAL_WITH_VARIABLE_DENSITY_PROP
    assert metadata_string == MATERIAL_WITH_VARIABLE_DENSITY_METADATA


materials = [
    Material(
        name="material with density",
        models=[
            Density(
                density=[1.34],
                independent_parameters=[
                    IndependentParameter(name="Temperature", values=[7.88860905221012e-31])
                ],
            ),
        ],
    )
]

material_dic = read_matml_file(XML_FILE_PATH)
export_data = Path.cwd() / "test_export.xml"
writer = MatmlWriter(material_dic.values())
writer.export(str(export_data), indent=True)
