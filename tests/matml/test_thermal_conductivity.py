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

from utilities import get_material_and_metadata_from_xml, read_specific_material

from ansys.materials.manager._models._common.independent_parameter import IndependentParameter
from ansys.materials.manager._models._material_models.thermal_conductivity_isotropic import (
    ThermalConductivityIsotropic,
)
from ansys.materials.manager._models._material_models.thermal_conductivity_orthotropic import (
    ThermalConductivityOrthotropic,
)
from ansys.materials.manager._models.material import Material
from ansys.materials.manager.util.matml.matml_from_material import MatmlWriter

from ansys.units import Quantity

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
XML_FILE_PATH = os.path.join(DIR_PATH, "..", "data", "matml_unittest_thermal_conductivity.xml")
THERMAL_CONDUCTIVITY_ISOTROPIC = os.path.join(DIR_PATH, "..", "data", "matml_thermal_conductivity_isotropic.txt")
THERMAL_CONDUCTIVITY_ISOTROPIC_METADATA = os.path.join(DIR_PATH, "..", "data", "matml_thermal_conductivity_isotropic_metadata.txt")
THERMAL_CONDUCTIVITY_ORTHOTROPIC = os.path.join(DIR_PATH, "..", "data", "matml_thermal_conductivity_orthotropic.txt")
THERMAL_CONDUCTIVITY_ORTHOTROPIC_METADATA = os.path.join(DIR_PATH, "..", "data", "matml_thermal_conductivity_orthotropic_metadata.txt")


def test_read_thermal_conductivity_isotropic_material():
    material = read_specific_material(XML_FILE_PATH, "Isotropic Convection Test Material")
    assert len(material.models) == 2
    isotropic_conductivity = material.models[1]
    assert isotropic_conductivity.name == "Thermal Conductivity"
    assert isotropic_conductivity.model_qualifiers[0].name == "Behavior"
    assert isotropic_conductivity.model_qualifiers[0].value == "Isotropic"
    assert isotropic_conductivity.model_qualifiers[1].name == "Field Variable Compatible"
    assert isotropic_conductivity.model_qualifiers[1].value == "Temperature"
    assert isotropic_conductivity.thermal_conductivity.value == [10.0]
    assert isotropic_conductivity.thermal_conductivity.unit == "W m^-1 C^-1"
    assert isotropic_conductivity.independent_parameters[0].name == "Temperature"
    assert isotropic_conductivity.independent_parameters[0].values.value == [7.88860905221012e-31]
    assert isotropic_conductivity.independent_parameters[0].values.unit == "C"
    assert isotropic_conductivity.independent_parameters[0].field_units == "C"
    assert isotropic_conductivity.independent_parameters[0].upper_limit == "Program Controlled"
    assert isotropic_conductivity.independent_parameters[0].lower_limit == "Program Controlled"
    assert isotropic_conductivity.independent_parameters[0].default_value == 22.0


def test_read_thermal_conductivity_orthotropic_material():
    material = read_specific_material(XML_FILE_PATH, "Orthotropic Convection Test Material")
    assert len(material.models) == 2
    orthotropic_conductivity = material.models[1]
    assert orthotropic_conductivity.name == "Thermal Conductivity"
    assert orthotropic_conductivity.model_qualifiers[0].name == "Behavior"
    assert orthotropic_conductivity.model_qualifiers[0].value == "Orthotropic"
    assert orthotropic_conductivity.thermal_conductivity_x.value == [10.0]
    assert orthotropic_conductivity.thermal_conductivity_x.unit == "W m^-1 C^-1"
    assert orthotropic_conductivity.thermal_conductivity_y.value == [15.0]
    assert orthotropic_conductivity.thermal_conductivity_y.unit == "W m^-1 C^-1"
    assert orthotropic_conductivity.thermal_conductivity_z.value == [20.0]
    assert orthotropic_conductivity.thermal_conductivity_z.unit == "W m^-1 C^-1"
    assert orthotropic_conductivity.independent_parameters[0].name == "Temperature"
    assert orthotropic_conductivity.independent_parameters[0].values.value == [7.88860905221012e-31]
    assert orthotropic_conductivity.independent_parameters[0].values.unit == "C"


def test_write_thermal_conductivity_isotropic():
    materials = [
        Material(
            name="Isotropic Convection Test Material",
            models=[
                ThermalConductivityIsotropic(
                    thermal_conductivity=Quantity(value=[10.0], units="W m^-1 C^-1"),
                    independent_parameters=[
                        IndependentParameter(
                            name="Temperature",
                            field_variable="Temperature",
                            values=Quantity(value=[7.88860905221012e-31], units="C"),
                            field_units="C",
                            default_value=22.0,
                            upper_limit="Program Controlled",
                            lower_limit="Program Controlled",
                        ),
                    ],
                ),
            ],
        )
    ]

    writer = MatmlWriter(materials)
    tree = writer._to_etree()
    material_string, metadata_string = get_material_and_metadata_from_xml(tree)
    with open(THERMAL_CONDUCTIVITY_ISOTROPIC, 'r') as file:
        data = file.read()
        assert data == material_string
    with open(THERMAL_CONDUCTIVITY_ISOTROPIC_METADATA, 'r') as file:
      data = file.read()
      assert data == metadata_string


def test_write_thermal_conductivity_orthotropic():
    materials = [
        Material(
            name="Orthotropic Convection Test Material",
            models=[
                ThermalConductivityOrthotropic(
                    thermal_conductivity_x=Quantity(value=[10.0], units="W m^-1 C^-1"),
                    thermal_conductivity_y=Quantity(value=[15.0], units="W m^-1 C^-1"),
                    thermal_conductivity_z=Quantity(value=[20.0], units="W m^-1 C^-1"),
                    independent_parameters=[
                        IndependentParameter(
                            name="Temperature",
                            field_variable="Temperature",
                            values=Quantity(value=[7.88860905221012e-31], units="C"),
                        ),
                    ],
                ),
            ],
        )
    ]

    writer = MatmlWriter(materials)
    tree = writer._to_etree()
    material_string, metadata_string = get_material_and_metadata_from_xml(tree)
    with open(THERMAL_CONDUCTIVITY_ORTHOTROPIC, 'r') as file:
        data = file.read()
        assert data == material_string
    with open(THERMAL_CONDUCTIVITY_ORTHOTROPIC_METADATA, 'r') as file:
      data = file.read()
      assert data == metadata_string
