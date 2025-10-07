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

from pathlib import Path

from ansys.units import Quantity
from utilities import get_material_and_metadata_from_xml, read_specific_material

from ansys.materials.manager._models._common import IndependentParameter, UserParameter
from ansys.materials.manager._models._material_models.usermat import ModelCoefficients
from ansys.materials.manager._models.material import Material
from ansys.materials.manager.util.matml.matml_from_material import MatmlWriter

DIR_PATH = Path(__file__).resolve().parent
XML_FILE_PATH = DIR_PATH.joinpath("..", "data", "matml_unittest_usermat.xml")
USER_MAT = DIR_PATH.joinpath("..", "data", "matml_user_mat.txt")
USER_MAT_METADATA = DIR_PATH.joinpath("..", "data", "matml_user_mat_metadata.txt")
USER_MAT_VARIABLE = DIR_PATH.joinpath("..", "data", "matml_user_mat_variable.txt")
USER_MAT_VARIABLE_METADATA = DIR_PATH.joinpath("..", "data", "matml_user_mat_variable_metadata.txt")


def test_read_usermat():
    material = read_specific_material(XML_FILE_PATH, "usermat")
    assert len(material.models) == 4
    usermat = material.models[3]
    assert usermat.name == "Model Coefficients"
    assert usermat.model_qualifiers[0].name == "UserMat"
    assert usermat.model_qualifiers[0].value == "USER"
    assert usermat.model_qualifiers[1].name == "Custom Qualifier"
    assert usermat.model_qualifiers[1].value == "Custom Qualifier Value"
    assert usermat.material_property == "UserDefinedPropertySet"
    assert usermat.independent_parameters[0].name == "Temperature"
    assert usermat.independent_parameters[0].values.value == [7.88860905221012e-31]
    assert usermat.independent_parameters[0].values.unit == "C"
    assert usermat.user_parameters[0].name == "y"
    assert usermat.user_parameters[0].values.value == [0.0]
    assert usermat.user_parameters[0].values.unit == ""
    assert usermat.user_parameters[0].user_mat_constant == 1


def test_variable_user_mat():
    material = read_specific_material(XML_FILE_PATH, "variable usermat")
    assert len(material.models) == 4
    usermat = material.models[3]
    assert usermat.name == "Model Coefficients"
    assert usermat.model_qualifiers[0].name == "UserMat"
    assert usermat.model_qualifiers[0].value == "USER"
    assert usermat.material_property == "CustomPset"
    assert usermat.independent_parameters[0].name == "Temperature"
    assert usermat.independent_parameters[0].values.value.tolist() == [10.0, 20.0]
    assert usermat.independent_parameters[0].values.unit == "C"
    assert usermat.user_parameters[0].name == "alpha"
    assert usermat.user_parameters[0].values.value.tolist() == [0.1, 0.4]
    assert usermat.user_parameters[0].values.unit == ""
    assert usermat.user_parameters[0].user_mat_constant == 1
    assert usermat.user_parameters[1].name == "beta"
    assert usermat.user_parameters[1].values.value.tolist() == [0.2, 0.8]
    assert usermat.user_parameters[0].values.unit == ""
    assert usermat.user_parameters[1].user_mat_constant == 2


def test_write_constant_usermat():
    materials = [
        Material(
            name="isotropic material with strain limit",
            models=[
                ModelCoefficients(
                    user_parameters=[
                        UserParameter(
                            name="y",
                            values=Quantity(value=[0.0], units=""),
                            user_mat_constant=1,
                        )
                    ],
                    independent_parameters=[
                        IndependentParameter(
                            name="Temperature",
                            values=Quantity(value=[7.88860905221012e-31], units="C"),
                        )
                    ],
                    material_property="UserDefinedPropertySet",
                ),
            ],
        )
    ]

    writer = MatmlWriter(materials)
    tree = writer._to_etree()
    material_string, metadata_string = get_material_and_metadata_from_xml(tree)
    with open(USER_MAT, "r", encoding="utf8") as file:
        data = file.read()
        assert data == material_string
    with open(USER_MAT_METADATA, "r", encoding="utf8") as file:
        data = file.read()
        assert data == metadata_string


def test_write_variable_usermat():
    materials = [
        Material(
            name="variable usermat",
            models=[
                ModelCoefficients(
                    user_parameters=[
                        UserParameter(
                            name="alpha",
                            values=Quantity(value=[0.1, 0.4], units=""),
                            user_mat_constant=1,
                        ),
                        UserParameter(
                            name="beta",
                            values=Quantity(value=[0.2, 0.8], units=""),
                            user_mat_constant=2,
                        ),
                    ],
                    independent_parameters=[
                        IndependentParameter(
                            name="Temperature", values=Quantity(value=[10.0, 20.0], units="C")
                        )
                    ],
                    material_property="CustomPset",
                ),
            ],
        )
    ]

    writer = MatmlWriter(materials)
    tree = writer._to_etree()
    material_string, metadata_string = get_material_and_metadata_from_xml(tree)
    with open(USER_MAT_VARIABLE, "r") as file:
        data = file.read()
        assert data == material_string

    with open(USER_MAT_VARIABLE_METADATA, "r", encoding="utf8") as file:
        data = file.read()
        assert data == metadata_string
