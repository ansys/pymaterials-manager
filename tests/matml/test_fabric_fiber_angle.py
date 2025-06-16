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

from utilities import read_matml_file

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
XML_FILE_PATH = os.path.join(DIR_PATH, "..", "data", "MatML_unittest_fabric_fiber_angle.xml")


def test_read_constant_fabric_fiber_angle_0_deg():
    material_dic = read_matml_file(XML_FILE_PATH)
    assert "Plain woven Resin Epoxy/UD Resin Epoxy/T300 Typical 65%; angle=0" in material_dic.keys()
    assert (
        len(material_dic["Plain woven Resin Epoxy/UD Resin Epoxy/T300 Typical 65%; angle=0"].models)
        == 4
    )
    fabric_fiber_angle = material_dic[
        "Plain woven Resin Epoxy/UD Resin Epoxy/T300 Typical 65%; angle=0"
    ].models[3]
    assert fabric_fiber_angle.name == "Fabric Fiber Angle"
    assert fabric_fiber_angle.model_qualifiers[0].name == "Field Variable Compatible"
    assert fabric_fiber_angle.model_qualifiers[0].value == "Temperature"
    assert fabric_fiber_angle.interpolation_options.algorithm_type == "Linear Multivariate"
    assert fabric_fiber_angle.interpolation_options.cached == True
    assert fabric_fiber_angle.interpolation_options.normalized == True
    assert fabric_fiber_angle.fabric_fiber_angle == [0.0]
    assert fabric_fiber_angle.independent_parameters == []


def test_read_constant_fabric_fiber_angle_35_deg():
    material_dic = read_matml_file(XML_FILE_PATH)
    assert (
        "Plain woven Resin Epoxy/UD Resin Epoxy/T300 Typical 65%; angle=35" in material_dic.keys()
    )
    assert (
        len(
            material_dic["Plain woven Resin Epoxy/UD Resin Epoxy/T300 Typical 65%; angle=35"].models
        )
        == 4
    )
    fabric_fiber_angle = material_dic[
        "Plain woven Resin Epoxy/UD Resin Epoxy/T300 Typical 65%; angle=35"
    ].models[3]
    assert fabric_fiber_angle.name == "Fabric Fiber Angle"
    assert fabric_fiber_angle.model_qualifiers[0].name == "Field Variable Compatible"
    assert fabric_fiber_angle.model_qualifiers[0].value == "Temperature"
    assert fabric_fiber_angle.interpolation_options.algorithm_type == "Linear Multivariate"
    assert fabric_fiber_angle.interpolation_options.cached == True
    assert fabric_fiber_angle.interpolation_options.normalized == True
    assert fabric_fiber_angle.fabric_fiber_angle == [35.0]
    assert fabric_fiber_angle.independent_parameters == []


def test_read_constant_fabric_fiber_angle_45_deg():
    material_dic = read_matml_file(XML_FILE_PATH)
    assert (
        "Plain woven Resin Epoxy/UD Resin Epoxy/T300 Typical 65%; angle=45" in material_dic.keys()
    )
    assert (
        len(
            material_dic["Plain woven Resin Epoxy/UD Resin Epoxy/T300 Typical 65%; angle=45"].models
        )
        == 4
    )
    fabric_fiber_angle = material_dic[
        "Plain woven Resin Epoxy/UD Resin Epoxy/T300 Typical 65%; angle=45"
    ].models[3]
    assert fabric_fiber_angle.name == "Fabric Fiber Angle"
    assert fabric_fiber_angle.model_qualifiers[0].name == "Field Variable Compatible"
    assert fabric_fiber_angle.model_qualifiers[0].value == "Temperature"
    assert fabric_fiber_angle.interpolation_options.algorithm_type == "Linear Multivariate"
    assert fabric_fiber_angle.interpolation_options.cached == True
    assert fabric_fiber_angle.interpolation_options.normalized == True
    assert fabric_fiber_angle.fabric_fiber_angle == [45.0]
    assert fabric_fiber_angle.independent_parameters == []


def test_read_variable_fabric_fiber_angle():
    material_dic = read_matml_file(XML_FILE_PATH)
    assert "Variable Plain woven Resin Epoxy/UD Resin Epoxy/T300 Typical 65%" in material_dic.keys()
    assert (
        len(material_dic["Variable Plain woven Resin Epoxy/UD Resin Epoxy/T300 Typical 65%"].models)
        == 4
    )
    fabric_fiber_angle = material_dic[
        "Variable Plain woven Resin Epoxy/UD Resin Epoxy/T300 Typical 65%"
    ].models[3]
    assert fabric_fiber_angle.name == "Fabric Fiber Angle"
    assert fabric_fiber_angle.model_qualifiers[0].name == "Field Variable Compatible"
    assert fabric_fiber_angle.model_qualifiers[0].value == "Temperature"
    assert fabric_fiber_angle.interpolation_options.algorithm_type == "Linear Multivariate"
    assert fabric_fiber_angle.interpolation_options.cached == True
    assert fabric_fiber_angle.interpolation_options.normalized == True
    assert fabric_fiber_angle.fabric_fiber_angle == [55, 52.5, 50, 47.5, 45, 42.5, 40, 37.5, 35]
    assert fabric_fiber_angle.independent_parameters[0].name == "Shear Angle"
    assert fabric_fiber_angle.independent_parameters[0].values == [
        -0.349065850398866,
        -0.261799387799149,
        -0.174532925199433,
        -0.0872664625997165,
        0,
        0.0872664625997165,
        0.174532925199433,
        0.261799387799149,
        0.349065850398866,
    ]
    assert fabric_fiber_angle.independent_parameters[0].units == "radian"
    assert fabric_fiber_angle.independent_parameters[0].upper_limit == "0.349065850398866"
    assert fabric_fiber_angle.independent_parameters[0].lower_limit == "-0.3490658503988659"
    assert fabric_fiber_angle.independent_parameters[0].default_value == "0"


def test_read_ply_type():
    material_dic = read_matml_file(XML_FILE_PATH)
    assert "Plain woven Resin Epoxy/UD Resin Epoxy/T300 Typical 65%; angle=0" in material_dic.keys()
    assert (
        len(material_dic["Plain woven Resin Epoxy/UD Resin Epoxy/T300 Typical 65%; angle=0"].models)
        == 4
    )
    ply_type = material_dic[
        "Plain woven Resin Epoxy/UD Resin Epoxy/T300 Typical 65%; angle=0"
    ].models[0]
    assert ply_type.name == "Ply Type"
    assert ply_type.model_qualifiers[0].name == "source"
    assert ply_type.model_qualifiers[0].value == "ACP"
    assert ply_type.model_qualifiers[1].name == "Type"
    assert ply_type.model_qualifiers[1].value == "Woven"
