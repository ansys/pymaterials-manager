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
from ansys.materials.manager._models._material_models.density import Density
from ansys.materials.manager._models.material import Material
from ansys.materials.manager.util.matml.matml_from_material import MatmlWriter
from ansys.units import Quantity

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
XML_FILE_PATH = os.path.join(DIR_PATH, "..", "data", "MatML_unittest_density.xml")
DENSITY = os.path.join(DIR_PATH, "..", "data", "density.txt")
DENSITY_METADATA = os.path.join(DIR_PATH, "..", "data", "density_metadata.txt")
DENSITY_VARIABLE = os.path.join(DIR_PATH, "..", "data", "density_variable.txt")


def test_read_material_with_constant_density():
  constant_density_material = read_specific_material(XML_FILE_PATH, "material with density")
  assert len(constant_density_material.models) == 2
  density = constant_density_material.models[1]
  assert density.name == "Density"
  assert density.density.value == [1.34]
  assert density.density.unit == "kg m^-3"
  assert len(density.independent_parameters) == 1
  assert density.independent_parameters[0].name == "Temperature"
  assert density.independent_parameters[0].values.value == [7.88860905221012e-31]
  assert density.independent_parameters[0].values.unit == "C"

def test_read_model_with_variable_density():
  variable_density_material = read_specific_material(XML_FILE_PATH, "material with variable density")
  assert len(variable_density_material.models) == 2
  density = variable_density_material.models[1]
  assert density.name == "Density"
  assert density.density.value.tolist() == [12.0, 32.0, 38.0]
  assert density.density.unit == "kg m^-3"
  assert len(density.independent_parameters) == 1
  assert density.independent_parameters[0].name == "Temperature"
  assert density.independent_parameters[0].values.value.tolist() == [
      20.0,
      21.0,
      23.0,
  ]
  assert density.independent_parameters[0].values.unit == "C"

def test_write_material_with_constant_density():
    materials = [
        Material(
            name="material with density",
            models=[
                Density(
                    density=Quantity(value=[1.34], units="kg m^-3"),
                    independent_parameters=[
                        IndependentParameter(name="Temperature", values=Quantity(value=[7.88860905221012e-31], units="C"))
                    ],
                ),
            ],
        )
    ]

    writer = MatmlWriter(materials)
    tree = writer._to_etree()
    material_string, metadata_string = get_material_and_metadata_from_xml(tree)
    print(metadata_string)
    with open(DENSITY, 'r') as file:
        data = file.read()
        assert data == material_string
    with open(DENSITY_METADATA, 'r') as file:
      data = file.read()
      assert data == metadata_string


def test_write_model_with_variable_density():
    materials = [
        Material(
            name="material variable with density",
            models=[
                Density(
                    density=Quantity(value=[12.0, 32.0, 38.0], units="kg m^-3"),
                    independent_parameters=[
                        IndependentParameter(name="Temperature", values=Quantity(value=[20.0, 21.0, 23.0], units="C"))
                    ],
                ),
            ],
        )
    ]

    writer = MatmlWriter(materials)
    tree = writer._to_etree()
    material_string, metadata_string = get_material_and_metadata_from_xml(tree)
    with open(DENSITY_VARIABLE, 'r') as file:
        data = file.read()
        assert data == material_string
    with open(DENSITY_METADATA, 'r') as file:
      data = file.read()
      assert data == metadata_string
