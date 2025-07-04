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

from utilities import get_material_and_metadata_from_xml, read_matml_file

from ansys.materials.manager._models._common.independent_parameter import IndependentParameter
from ansys.materials.manager._models._common.model_qualifier import ModelQualifier
from ansys.materials.manager._models._material_models.fiber_angle import FiberAngle
from ansys.materials.manager._models._material_models.puck_constants import PuckConstants
from ansys.materials.manager._models._material_models.puck_constants_additional import (
    AdditionalPuckConstants,
)
from ansys.materials.manager._models._material_models.stress_limits_orthotropic import (
    StressLimitsOrthotropic,
)
from ansys.materials.manager._models.material import Material
from ansys.materials.manager.util.matml.matml_from_material import MatmlWriter

from ansys.units import Quantity

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
XML_FILE_PATH = os.path.join(DIR_PATH, "..", "data", "MatML_unittest_puck_for_woven.xml")
FIBER_ANGLE = os.path.join(DIR_PATH, "..", "data", "fiber_angle.txt")
FIBER_ANGLE_METADATA = os.path.join(DIR_PATH, "..", "data", "fiber_angle_metadata.txt")
PUCK = os.path.join(DIR_PATH, "..", "data", "puck.txt")
PUCK_METADATA = os.path.join(DIR_PATH, "..", "data", "puck_metadata.txt")
PUCK_ADDITIONAL = os.path.join(DIR_PATH, "..", "data", "puck_additional.txt")
PUCK_ADDITIONAL_METADATA = os.path.join(DIR_PATH, "..", "data", "puck_additional_metadata.txt")
STRESS_LIMITS_ORTHOTROPIC = os.path.join(DIR_PATH, "..", "data", "stress_limits_orthotropic.txt")
STRESS_LIMITS_ORTHOTROPIC_METADATA = os.path.join(DIR_PATH, "..", "data", "stress_limits_orthotropic_metadata.txt")

def test_read_fiber_angle():
    material_dic = read_matml_file(XML_FILE_PATH)
    assert "material with puck for woven" in material_dic.keys()
    assert len(material_dic["material with puck for woven"].models) == 5
    fiber_angle = material_dic["material with puck for woven"].models[1]
    assert fiber_angle.name == "Fiber Angle"
    assert fiber_angle.independent_parameters[0].name == "Fiber Angle"
    assert fiber_angle.independent_parameters[0].values.value == [90.0]
    assert fiber_angle.independent_parameters[0].values.unit == ""
    assert fiber_angle.model_qualifiers[0].name == "Data Set"
    assert fiber_angle.model_qualifiers[0].value == "2"
    assert fiber_angle.model_qualifiers[1].name == "Data Set Information"
    assert (
        fiber_angle.model_qualifiers[1].value
        == "minOccurrences::2$$maxOccurrences::2$$Name::Unidirectional"
    )


def test_read_puck_constants():
    material_dic = read_matml_file(XML_FILE_PATH)
    assert "material with puck for woven" in material_dic.keys()
    assert len(material_dic["material with puck for woven"].models) == 5
    puck_constants = material_dic["material with puck for woven"].models[3]
    assert puck_constants.name == "Puck Constants"
    assert puck_constants.independent_parameters == []
    assert puck_constants.model_qualifiers[0].name == "Data Set"
    assert puck_constants.model_qualifiers[0].value == "2"
    assert puck_constants.model_qualifiers[1].name == "Data Set Information"
    assert (
        puck_constants.model_qualifiers[1].value
        == "minOccurrences::2$$maxOccurrences::2$$Name::Unidirectional"
    )
    assert puck_constants.model_qualifiers[2].name == "Material Classification"
    assert puck_constants.model_qualifiers[2].value == "Material Specific"
    assert puck_constants.compressive_inclination_xz.value == [0.0]
    assert puck_constants.compressive_inclination_xz.unit == ""
    assert puck_constants.compressive_inclination_yz.value == [0.0]
    assert puck_constants.compressive_inclination_yz.unit == ""
    assert puck_constants.tensile_inclination_xz.value == [0.0]
    assert puck_constants.tensile_inclination_xz.unit == ""
    assert puck_constants.tensile_inclination_yz.value == [0.0]
    assert puck_constants.tensile_inclination_yz.unit == ""
    assert puck_constants.material_property == "Woven Specification for Puck"


def test_read_puck_additional_constants():
    material_dic = read_matml_file(XML_FILE_PATH)
    assert "material with puck for woven" in material_dic.keys()
    assert len(material_dic["material with puck for woven"].models) == 5
    puck_additional_constants = material_dic["material with puck for woven"].models[4]
    assert puck_additional_constants.name == "Additional Puck Constants"
    assert puck_additional_constants.independent_parameters == []
    assert puck_additional_constants.model_qualifiers[0].name == "Data Set"
    assert puck_additional_constants.model_qualifiers[0].value == "2"
    assert puck_additional_constants.model_qualifiers[1].name == "Data Set Information"
    assert (
        puck_additional_constants.model_qualifiers[1].value
        == "minOccurrences::2$$maxOccurrences::2$$Name::Unidirectional"
    )
    assert puck_additional_constants.degradation_parameter_s.value == [0.5]
    assert puck_additional_constants.degradation_parameter_s.unit == ""
    assert puck_additional_constants.degradation_parameter_m.value == [0.5]
    assert puck_additional_constants.degradation_parameter_m.unit == ""
    assert puck_additional_constants.interface_weakening_factor.value == [0.8]
    assert puck_additional_constants.interface_weakening_factor.unit == ""
    assert puck_additional_constants.material_property == "Woven Specification for Puck"


def test_read_stress_limits_orthotropic():
    material_dic = read_matml_file(XML_FILE_PATH)
    assert "material with puck for woven" in material_dic.keys()
    assert "material with puck for woven" in material_dic.keys()
    assert len(material_dic["material with puck for woven"].models) == 5
    stress_limits_orthotropic = material_dic["material with puck for woven"].models[2]
    assert stress_limits_orthotropic.name == "Stress Limits"
    assert stress_limits_orthotropic.independent_parameters == []
    assert stress_limits_orthotropic.model_qualifiers[0].name == "Behavior"
    assert stress_limits_orthotropic.model_qualifiers[0].value == "Orthotropic"
    assert stress_limits_orthotropic.model_qualifiers[1].name == "Data Set"
    assert stress_limits_orthotropic.model_qualifiers[1].value == "2"
    assert stress_limits_orthotropic.model_qualifiers[2].name == "Data Set Information"
    assert (
        stress_limits_orthotropic.model_qualifiers[2].value
        == "minOccurrences::2$$maxOccurrences::2$$Name::Unidirectional"
    )
    assert stress_limits_orthotropic.compressive_x_direction.value == [-100.0]
    assert stress_limits_orthotropic.compressive_x_direction.unit == "Pa"
    assert stress_limits_orthotropic.compressive_y_direction.value == [-101.0]
    assert stress_limits_orthotropic.compressive_y_direction.unit == "Pa"
    assert stress_limits_orthotropic.compressive_z_direction.value == [-102.0]
    assert stress_limits_orthotropic.compressive_z_direction.unit == "Pa"
    assert stress_limits_orthotropic.tensile_x_direction.value == [100.0]
    assert stress_limits_orthotropic.tensile_x_direction.unit == "Pa"
    assert stress_limits_orthotropic.tensile_y_direction.value == [101.0]
    assert stress_limits_orthotropic.tensile_y_direction.unit == "Pa"
    assert stress_limits_orthotropic.tensile_z_direction.value == [102.0]
    assert stress_limits_orthotropic.tensile_z_direction.unit == "Pa"
    assert stress_limits_orthotropic.shear_xy.value == [10.0]
    assert stress_limits_orthotropic.shear_xy.unit == "Pa"
    assert stress_limits_orthotropic.shear_xz.value == [14.0]
    assert stress_limits_orthotropic.shear_xz.unit == "Pa"
    assert stress_limits_orthotropic.shear_yz.value == [12.0]
    assert stress_limits_orthotropic.shear_yz.unit == "Pa"


def test_write_fiber_angle():
    materials = [
        Material(
            name="material with puck for woven",
            models=[
                FiberAngle(
                    model_qualifiers=[
                        ModelQualifier(name="Data Set", values=["1"]),
                        ModelQualifier(
                            name="Data Set Information",
                            values=["minOccurrences::2$$maxOccurrences::2$$Name::Unidirectional"],
                        ),
                    ],
                    material_property="Woven Specification for Puck",
                    independent_parameters=[
                        IndependentParameter(name="Fiber Angle", values=Quantity(value=[45.0], units=""))
                    ],
                ),
            ],
        )
    ]
    writer = MatmlWriter(materials)
    tree = writer._to_etree()
    material_string, metadata_string = get_material_and_metadata_from_xml(tree)
    with open(FIBER_ANGLE, 'r') as file:
        data = file.read()
        assert data == material_string
    with open(FIBER_ANGLE_METADATA, 'r') as file:
      data = file.read()
      assert data == metadata_string


def test_write_puck_constants():
    materials = [
    Material(
            name="material with puck for woven",
            models=[
                PuckConstants(
                    compressive_inclination_xz=Quantity(value=[0.0], units=""),
                    compressive_inclination_yz=Quantity([0.0], units=""),
                    tensile_inclination_xz=Quantity([0.0], units=""),
                    tensile_inclination_yz=Quantity([0.0], units=""),
                    model_qualifiers=[
                        ModelQualifier(name="Data Set", values=["2"]),
                        ModelQualifier(
                            name="Data Set Information",
                            values=["minOccurrences::2$$maxOccurrences::2$$Name::Unidirectional"],
                        ),
                    ],
                    material_property="Woven Specification for Puck",
                ),
            ],
        )
    ]

    writer = MatmlWriter(materials)
    tree = writer._to_etree()
    material_string, metadata_string = get_material_and_metadata_from_xml(tree)
    with open(PUCK, 'r') as file:
        data = file.read()
        assert data == material_string
    with open(PUCK_METADATA, 'r') as file:
      data = file.read()
      assert data == metadata_string


def test_write_puck_additional_constants():
    materials = [
        Material(
            name="material with puck for woven",
            models=[
                AdditionalPuckConstants(
                    degradation_parameter_s=Quantity(value=[0.5], units=""),
                    degradation_parameter_m=Quantity(value=[0.5], units=""),
                    interface_weakening_factor=Quantity(value=[0.8], units=""),
                    model_qualifiers=[
                        ModelQualifier(name="Data Set", values=["2"]),
                        ModelQualifier(
                            name="Data Set Information",
                            values=["minOccurrences::2$$maxOccurrences::2$$Name::Unidirectional"],
                        ),
                    ],
                    material_property="Woven Specification for Puck",
                ),
            ],
        )
    ]

    writer = MatmlWriter(materials)
    tree = writer._to_etree()
    material_string, metadata_string = get_material_and_metadata_from_xml(tree)
    with open(PUCK_ADDITIONAL, 'r') as file:
        data = file.read()
        assert data == material_string
    with open(PUCK_ADDITIONAL_METADATA, 'r') as file:
      data = file.read()
      assert data == metadata_string


def test_write_stress_limits():
    materials = [
        Material(
            name="material with stress_limits",
            models=[
                StressLimitsOrthotropic(
                    compressive_x_direction=Quantity(value=[-100.0], units="Pa"),
                    compressive_y_direction=Quantity(value=[-101.0], units="Pa"),
                    compressive_z_direction=Quantity(value=[-102.0], units="Pa"),
                    tensile_x_direction=Quantity(value=[100.0], units="Pa"),
                    tensile_y_direction=Quantity(value=[101.0], units="Pa"),
                    tensile_z_direction=Quantity(value=[102.0], units="Pa"),
                    shear_xy=Quantity(value=[10.0], units="Pa"),
                    shear_xz=Quantity(value=[14.0], units="Pa"),
                    shear_yz=Quantity(value=[12.0], units="Pa"),
                ),
            ],
        )
    ]

    writer = MatmlWriter(materials)
    tree = writer._to_etree()
    material_string, metadata_string = get_material_and_metadata_from_xml(tree)
    with open(STRESS_LIMITS_ORTHOTROPIC, 'r') as file:
        data = file.read()
        assert data == material_string
    with open(STRESS_LIMITS_ORTHOTROPIC_METADATA, 'r') as file:
      data = file.read()
      assert data == metadata_string