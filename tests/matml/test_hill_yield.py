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

from ansys.materials.manager._models._common import IndependentParameter
from ansys.materials.manager._models._common import InterpolationOptions
from ansys.materials.manager._models._common import ModelQualifier
from ansys.materials.manager._models._material_models.hill_yield_criterion import HillYieldCriterion
from ansys.materials.manager._models._material_models.kinematic_hardening import KinematicHardening
from ansys.materials.manager._models._material_models.strain_hardening import StrainHardening
from ansys.materials.manager._models.material import Material
from ansys.materials.manager.util.matml.matml_from_material import MatmlWriter

from ansys.units import Quantity

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
NO_CREEP_XML_FILE_PATH = os.path.join(DIR_PATH, "..", "data", "matml_unittest_hill_yield.xml")
CREEP_XML_FILE_PATH = os.path.join(DIR_PATH, "..", "data", "matml_unittest_hill_yield_creep.xml")
HILL_YIELD = os.path.join(DIR_PATH, "..", "data", "matml_hill_yield.txt")
HILL_YIELD_METADATA = os.path.join(DIR_PATH, "..", "data", "matml_hill_yield_metadata.txt")
HILL_YIELD_VARIABLE = os.path.join(DIR_PATH, "..", "data", "matml_hill_yield_variable.txt")
HILL_YIELD_CREEP = os.path.join(DIR_PATH, "..", "data", "matml_hill_yield_creep.txt")
HILL_YIELD_CREEP_METADATA = os.path.join(DIR_PATH, "..", "data", "matml_hill_yield_creep_metadata.txt")
KINEMATIC_HARDENING = os.path.join(DIR_PATH, "..", "data", "matml_kinematic_harderning.txt")
KINEMATIC_HARDENING_METADATA = os.path.join(DIR_PATH, "..", "data", "matml_kinematic_harderning_metadata.txt")
STRAIN_HARDENING = os.path.join(DIR_PATH, "..", "data", "matml_strain_hardening.txt")
STRAIN_HARDENING_METADATA = os.path.join(DIR_PATH, "..", "data", "matml_strain_hardening_metadata.txt")

def test_read_constant_hill_yield_no_creep():
    material = read_specific_material(NO_CREEP_XML_FILE_PATH, "SFRP")
    assert len(material.models) == 3
    hill_yield = material.models[2]
    assert hill_yield.name == "Hill Yield Criterion"
    assert (
        hill_yield.model_qualifiers[0].name == "Separated Hill Potentials for Plasticity and Creep"
    )
    assert hill_yield.model_qualifiers[0].value == "No"
    assert hill_yield.model_qualifiers[1].name == "Field Variable Compatible"
    assert hill_yield.model_qualifiers[1].value == "Temperature"
    assert hill_yield.interpolation_options.algorithm_type == "Linear Multivariate"
    assert hill_yield.interpolation_options.cached == True
    assert hill_yield.interpolation_options.normalized == True
    assert hill_yield.yield_stress_ratio_x.value == [1.2]
    assert hill_yield.yield_stress_ratio_x.unit == ""
    assert hill_yield.yield_stress_ratio_xy.value == [0.12]
    assert hill_yield.yield_stress_ratio_xy.unit == ""
    assert hill_yield.yield_stress_ratio_xz.value == [0.23]
    assert hill_yield.yield_stress_ratio_xz.unit == ""
    assert hill_yield.yield_stress_ratio_y.value == [0.8]
    assert hill_yield.yield_stress_ratio_y.unit == ""
    assert hill_yield.yield_stress_ratio_yz.value == [0.23]
    assert hill_yield.yield_stress_ratio_yz.unit == ""
    assert hill_yield.yield_stress_ratio_z.value == [0.5]
    assert hill_yield.yield_stress_ratio_z.unit == ""
    assert hill_yield.yield_stress_ratio_x_for_plasticity == None
    assert hill_yield.yield_stress_ratio_y_for_plasticity == None
    assert hill_yield.yield_stress_ratio_z_for_plasticity == None
    assert hill_yield.yield_stress_ratio_xy_for_plasticity == None
    assert hill_yield.yield_stress_ratio_xz_for_plasticity == None
    assert hill_yield.yield_stress_ratio_yz_for_plasticity == None
    assert hill_yield.yield_stress_ratio_x_for_creep == None
    assert hill_yield.yield_stress_ratio_y_for_creep == None
    assert hill_yield.yield_stress_ratio_z_for_creep == None
    assert hill_yield.yield_stress_ratio_xy_for_creep == None
    assert hill_yield.yield_stress_ratio_xz_for_creep == None
    assert hill_yield.yield_stress_ratio_yz_for_creep == None
    assert hill_yield.independent_parameters[0].name == "Temperature"
    assert hill_yield.independent_parameters[0].field_variable == "Temperature"
    assert hill_yield.independent_parameters[0].field_units == "C"
    assert hill_yield.independent_parameters[0].default_value == 22.0
    assert hill_yield.independent_parameters[0].upper_limit == "Program Controlled"
    assert hill_yield.independent_parameters[0].lower_limit == "Program Controlled"
    assert hill_yield.independent_parameters[0].values.value == [7.88860905221012e-31]
    assert hill_yield.independent_parameters[0].values.unit == "C"
    
    


def test_read_variable_temp_hill_yield_no_creep():
    material = read_specific_material(NO_CREEP_XML_FILE_PATH, "SFRP Temp Dependent")
    assert len(material.models) == 3
    hill_yield = material.models[2]
    assert hill_yield.name == "Hill Yield Criterion"
    assert (
        hill_yield.model_qualifiers[0].name == "Separated Hill Potentials for Plasticity and Creep"
    )
    assert hill_yield.model_qualifiers[0].value == "No"
    assert hill_yield.model_qualifiers[1].name == "Field Variable Compatible"
    assert hill_yield.model_qualifiers[1].value == "Temperature"
    assert hill_yield.interpolation_options.algorithm_type == "Linear Multivariate"
    assert hill_yield.interpolation_options.cached == True
    assert hill_yield.interpolation_options.normalized == True
    assert hill_yield.yield_stress_ratio_x.value.tolist() == [1.2, 1.2, 1.4]
    assert hill_yield.yield_stress_ratio_x.unit == ""
    assert hill_yield.yield_stress_ratio_xy.value.tolist() == [0.12, 0.12, 0.12]
    assert hill_yield.yield_stress_ratio_xy.unit == ""
    assert hill_yield.yield_stress_ratio_xz.value.tolist() == [0.23, 0.23, 0.23]
    assert hill_yield.yield_stress_ratio_xz.unit == ""
    assert hill_yield.yield_stress_ratio_y.value.tolist() == [0.8, 0.8, 0.7]
    assert hill_yield.yield_stress_ratio_y.unit == ""
    assert hill_yield.yield_stress_ratio_yz.value.tolist() == [0.23, 0.23, 0.23]
    assert hill_yield.yield_stress_ratio_yz.unit == ""
    assert hill_yield.yield_stress_ratio_z.value.tolist() == [0.5, 0.5, 0.4]
    assert hill_yield.yield_stress_ratio_z.unit == ""
    assert hill_yield.yield_stress_ratio_x_for_plasticity == None
    assert hill_yield.yield_stress_ratio_y_for_plasticity == None
    assert hill_yield.yield_stress_ratio_z_for_plasticity == None
    assert hill_yield.yield_stress_ratio_xy_for_plasticity == None
    assert hill_yield.yield_stress_ratio_xz_for_plasticity == None
    assert hill_yield.yield_stress_ratio_yz_for_plasticity == None
    assert hill_yield.yield_stress_ratio_x_for_creep == None
    assert hill_yield.yield_stress_ratio_y_for_creep == None
    assert hill_yield.yield_stress_ratio_z_for_creep == None
    assert hill_yield.yield_stress_ratio_xy_for_creep == None
    assert hill_yield.yield_stress_ratio_xz_for_creep == None
    assert hill_yield.yield_stress_ratio_yz_for_creep == None
    assert hill_yield.independent_parameters[0].name == "Temperature"
    assert hill_yield.independent_parameters[0].values.value.tolist() == [34, 78, 245]
    assert hill_yield.independent_parameters[0].values.unit == "C"
    assert hill_yield.independent_parameters[0].field_variable == "Temperature"
    assert hill_yield.independent_parameters[0].field_units == "C"
    assert hill_yield.independent_parameters[0].default_value == 22.0
    assert hill_yield.independent_parameters[0].upper_limit == "Program Controlled"
    assert hill_yield.independent_parameters[0].lower_limit == "Program Controlled"


def test_read_variable_hill_yield_no_creep():
    material = read_specific_material(NO_CREEP_XML_FILE_PATH, "Variable Short Fiber")
    assert len(material.models) == 2
    hill_yield = material.models[0]
    assert hill_yield.name == "Hill Yield Criterion"
    assert (
        hill_yield.model_qualifiers[0].name == "Separated Hill Potentials for Plasticity and Creep"
    )
    assert hill_yield.model_qualifiers[0].value == "No"
    assert hill_yield.model_qualifiers[1].name == "Field Variable Compatible"
    assert hill_yield.model_qualifiers[1].value == "Temperature"
    assert hill_yield.interpolation_options.algorithm_type == "Linear Multivariate"
    assert hill_yield.interpolation_options.cached == True
    assert hill_yield.interpolation_options.normalized == True
    assert hill_yield.yield_stress_ratio_x.value.tolist() == [
        1.0,
        1.38717930847789,
        3.00721990713311,
        1.2181891328774,
        1.0,
        1.38717930847789,
        1.0,
    ]
    assert hill_yield.yield_stress_ratio_x.unit == ""
    assert hill_yield.yield_stress_ratio_xy.value.tolist() == [
        1.27583858742812,
        1.27583858742812,
        1.27583858742812,
        1.27583858742812,
        1.27583858742812,
        1.27583858742812,
        1.27583858742812,
    ]
    assert hill_yield.yield_stress_ratio_xy.unit == ""
    assert hill_yield.yield_stress_ratio_xz.value.tolist() == [
        1.27583858742812,
        1.27583858742812,
        1.27583858742812,
        1.27583858742812,
        1.27583858742812,
        1.27583858742812,
        1.27583858742812,
    ]
    assert hill_yield.yield_stress_ratio_xz.unit == ""
    assert hill_yield.yield_stress_ratio_y.value.tolist() == [
        1.0,
        1.0,
        1.0,
        1.2181891328774,
        1.38717930847789,
        1.38717930847789,
        3.00721990713311,
    ]
    assert hill_yield.yield_stress_ratio_y.unit == ""
    assert hill_yield.yield_stress_ratio_yz.value.tolist() == [
        1.27583858742812,
        1.27583858742812,
        1.27583858742812,
        1.27583858742812,
        1.27583858742812,
        1.27583858742812,
        1.27583858742812,
    ]
    assert hill_yield.yield_stress_ratio_yz.unit == ""
    assert hill_yield.yield_stress_ratio_z.value.tolist() == [
        3.00721990713311,
        1.38717930847789,
        1.0,
        1.21818913296279,
        1.38717930847789,
        1.0,
        1.0,
    ]
    assert hill_yield.yield_stress_ratio_z.unit == ""
    assert hill_yield.yield_stress_ratio_x_for_plasticity == None
    assert hill_yield.yield_stress_ratio_y_for_plasticity == None
    assert hill_yield.yield_stress_ratio_z_for_plasticity == None
    assert hill_yield.yield_stress_ratio_xy_for_plasticity == None
    assert hill_yield.yield_stress_ratio_xz_for_plasticity == None
    assert hill_yield.yield_stress_ratio_yz_for_plasticity == None
    assert hill_yield.yield_stress_ratio_x_for_creep == None
    assert hill_yield.yield_stress_ratio_y_for_creep == None
    assert hill_yield.yield_stress_ratio_z_for_creep == None
    assert hill_yield.yield_stress_ratio_xy_for_creep == None
    assert hill_yield.yield_stress_ratio_xz_for_creep == None
    assert hill_yield.yield_stress_ratio_yz_for_creep == None
    assert hill_yield.independent_parameters[0].name == "Orientation Tensor A11"
    assert hill_yield.independent_parameters[0].values.value.tolist() == [0, 0.5, 1, 0.3333333333, 0, 0.5, 0]
    assert hill_yield.independent_parameters[0].values.units == ""
    assert hill_yield.independent_parameters[0].default_value == "Program Controlled"
    assert hill_yield.independent_parameters[0].upper_limit == "Program Controlled"
    assert hill_yield.independent_parameters[0].lower_limit == "Program Controlled"
    assert hill_yield.independent_parameters[1].name == "Orientation Tensor A22"
    assert hill_yield.independent_parameters[1].values.value.tolist() == [0, 0, 0, 0.3333333333, 0.5, 0.5, 1]
    assert hill_yield.independent_parameters[1].values.units == ""
    assert hill_yield.independent_parameters[1].default_value == "Program Controlled"
    assert hill_yield.independent_parameters[1].upper_limit == "Program Controlled"
    assert hill_yield.independent_parameters[1].lower_limit == "Program Controlled"


def test_read_constant_hill_yield_creep():
    material = read_specific_material(CREEP_XML_FILE_PATH, "SFRP")
    assert len(material.models) == 5
    hill_yield = material.models[2]
    assert hill_yield.name == "Hill Yield Criterion"
    assert (
        hill_yield.model_qualifiers[0].name == "Separated Hill Potentials for Plasticity and Creep"
    )
    assert hill_yield.model_qualifiers[0].value == "Yes"
    assert hill_yield.yield_stress_ratio_x_for_plasticity.value == [1.0]
    assert hill_yield.yield_stress_ratio_x_for_plasticity.unit == ""
    assert hill_yield.yield_stress_ratio_xy_for_plasticity.value == [1.0]
    assert hill_yield.yield_stress_ratio_xy_for_plasticity.unit == ""
    assert hill_yield.yield_stress_ratio_xz_for_plasticity.value == [1.0]
    assert hill_yield.yield_stress_ratio_xz_for_plasticity.unit == ""
    assert hill_yield.yield_stress_ratio_y_for_plasticity.value == [1.0]
    assert hill_yield.yield_stress_ratio_y_for_plasticity.unit == ""
    assert hill_yield.yield_stress_ratio_yz_for_plasticity.value == [1.0]
    assert hill_yield.yield_stress_ratio_yz_for_plasticity.unit == ""
    assert hill_yield.yield_stress_ratio_z_for_plasticity.value == [1.0]
    assert hill_yield.yield_stress_ratio_z_for_plasticity.unit == ""
    assert hill_yield.yield_stress_ratio_x_for_creep.value == [2.0]
    assert hill_yield.yield_stress_ratio_x_for_creep.unit == ""
    assert hill_yield.yield_stress_ratio_y_for_creep.value == [2.0]
    assert hill_yield.yield_stress_ratio_y_for_creep.unit == ""
    assert hill_yield.yield_stress_ratio_z_for_creep.value == [2.0]
    assert hill_yield.yield_stress_ratio_z_for_creep.unit == ""
    assert hill_yield.yield_stress_ratio_xy_for_creep.value == [2.0]
    assert hill_yield.yield_stress_ratio_xy_for_creep.unit == ""
    assert hill_yield.yield_stress_ratio_xz_for_creep.value == [2.0]
    assert hill_yield.yield_stress_ratio_xz_for_creep.unit == ""
    assert hill_yield.yield_stress_ratio_yz_for_creep.value == [2.0]
    assert hill_yield.yield_stress_ratio_yz_for_creep.unit == ""
    assert hill_yield.yield_stress_ratio_x == None
    assert hill_yield.yield_stress_ratio_y == None
    assert hill_yield.yield_stress_ratio_z == None
    assert hill_yield.yield_stress_ratio_xy == None
    assert hill_yield.yield_stress_ratio_xz == None
    assert hill_yield.yield_stress_ratio_yz == None
    assert hill_yield.independent_parameters[0].name == "Temperature"
    assert hill_yield.independent_parameters[0].values.value == [7.88860905221012e-31]
    assert hill_yield.independent_parameters[0].values.unit == "C"


def test_read_constant_kinematic_hardening_creep():
    material = read_specific_material(CREEP_XML_FILE_PATH, "SFRP")
    assert len(material.models) == 5
    kinematic_hardening = material.models[3]
    assert kinematic_hardening.name == "Kinematic Hardening"
    assert kinematic_hardening.model_qualifiers[0].name == "Definition"
    assert kinematic_hardening.model_qualifiers[0].value == "Chaboche"
    assert kinematic_hardening.model_qualifiers[1].name == "Number of Kinematic Models"
    assert kinematic_hardening.model_qualifiers[1].value == "1"
    assert kinematic_hardening.model_qualifiers[2].name == "source"
    assert kinematic_hardening.model_qualifiers[2].value == "ANSYS"
    assert kinematic_hardening.yield_stress.value == [12.0]
    assert kinematic_hardening.yield_stress.unit == "Pa"
    assert kinematic_hardening.material_constant_gamma_1.value == [1.0]
    assert kinematic_hardening.material_constant_gamma_1.unit == ""
    assert kinematic_hardening.material_constant_c_1.value == [45.0]
    assert kinematic_hardening.material_constant_c_1.unit == "Pa"
    assert kinematic_hardening.material_constant_gamma_2 == None
    assert kinematic_hardening.material_constant_c_2 == None
    assert kinematic_hardening.material_constant_gamma_3 == None
    assert kinematic_hardening.material_constant_c_3 == None
    assert kinematic_hardening.material_constant_gamma_4 == None
    assert kinematic_hardening.material_constant_c_4 == None
    assert kinematic_hardening.material_constant_gamma_5 == None
    assert kinematic_hardening.material_constant_c_5 == None
    assert kinematic_hardening.independent_parameters[0].name == "Temperature"
    assert kinematic_hardening.independent_parameters[0].values.value == [7.88860905221012e-31]
    assert kinematic_hardening.independent_parameters[0].values.unit == "C"
    

def test_read_constant_strain_hardening_creep():
    material = read_specific_material(CREEP_XML_FILE_PATH, "SFRP")
    assert len(material.models) == 5
    strain_hardening = material.models[4]
    assert strain_hardening.name == "Strain Hardening"
    assert (
        strain_hardening.model_qualifiers[0].name
        == "Reference Units (Length, Time, Temperature, Force)"
    )
    assert strain_hardening.model_qualifiers[0].value == "m, s, K, N"
    assert strain_hardening.creep_constant_1.value == [1.0]
    assert strain_hardening.creep_constant_1.unit == ""
    assert strain_hardening.creep_constant_2.value == [2.0]
    assert strain_hardening.creep_constant_2.unit == ""
    assert strain_hardening.creep_constant_3.value == [3.0]
    assert strain_hardening.creep_constant_3.unit == ""
    assert strain_hardening.creep_constant_4.value == [4.0]
    assert strain_hardening.creep_constant_4.unit == ""
    assert strain_hardening.independent_parameters[0].name == "Temperature"
    assert strain_hardening.independent_parameters[0].values.value == [7.88860905221012e-31]
    assert strain_hardening.independent_parameters[0].values.unit == "C"


def test_write_constant_hill_yield_no_creep():
    materials = [
        Material(
            name="SFRP",
            models=[
                HillYieldCriterion(
                    yield_stress_ratio_x=Quantity(value=[1.2], units=""),
                    yield_stress_ratio_xy=Quantity(value=[0.12], units=""),
                    yield_stress_ratio_xz=Quantity(value=[0.23], units=""),
                    yield_stress_ratio_y=Quantity(value=[0.8], units=""),
                    yield_stress_ratio_yz=Quantity(value=[0.23], units=""),
                    yield_stress_ratio_z=Quantity(value=[0.5], units=""),
                    independent_parameters=[
                        IndependentParameter(
                            name="Temperature",
                            values=Quantity(value=[7.88860905221012e-31], units="C"),
                            default_value=22.0,
                            field_variable="Temperature",
                            field_units="C",
                            upper_limit="Program Controlled",
                            lower_limit="Program Controlled",
                        ),
                    ],
                    interpolation_options=InterpolationOptions(
                        algorithm_type="Linear Multivariate",
                        cached=True,
                        normalized=True,
                    ),
                ),
            ],
        )
    ]

    writer = MatmlWriter(materials)
    tree = writer._to_etree()
    material_string, metadata_string = get_material_and_metadata_from_xml(tree)
    with open(HILL_YIELD, 'r') as file:
        data = file.read()
        assert data == material_string
    with open(HILL_YIELD_METADATA, 'r') as file:
      data = file.read()
      assert data == metadata_string


def test_write_variable_hill_yield_no_creep():
    materials = [
        Material(
            name="SFRP Temp Dependent",
            models=[
                HillYieldCriterion(
                    yield_stress_ratio_x=Quantity(value=[1.2, 1.2, 1.4], units=""),
                    yield_stress_ratio_xy=Quantity(value=[0.12, 0.12, 0.12], units=""),
                    yield_stress_ratio_xz=Quantity(value=[0.23, 0.23, 0.23], units=""),
                    yield_stress_ratio_y=Quantity(value=[0.8, 0.8, 0.7], units=""),
                    yield_stress_ratio_yz=Quantity(value=[0.23, 0.23, 0.23], units=""),
                    yield_stress_ratio_z=Quantity(value=[0.5, 0.5, 0.4], units=""),
                    independent_parameters=[
                        IndependentParameter(
                            name="Temperature",
                            values=Quantity(value=[34.0, 78.0, 245.0], units="C"),
                            default_value=22.0,
                            field_variable="Temperature",
                            field_units="C",
                            upper_limit="Program Controlled",
                            lower_limit="Program Controlled",
                        ),
                    ],
                    interpolation_options=InterpolationOptions(
                        algorithm_type="Linear Multivariate",
                        cached=True,
                        normalized=True,
                    ),
                ),
            ],
        )
    ]
    writer = MatmlWriter(materials)
    tree = writer._to_etree()
    material_string, metadata_string = get_material_and_metadata_from_xml(tree)
    with open(HILL_YIELD_VARIABLE, 'r') as file:
        data = file.read()
        assert data == material_string
    with open(HILL_YIELD_METADATA, 'r') as file:
      data = file.read()
      assert data == metadata_string


def test_write_constant_hill_yield_creep():
    materials = [
        Material(
            name="SFRP",
            models=[
                HillYieldCriterion(
                    yield_stress_ratio_x_for_plasticity=Quantity(value=[1.0], units=""),
                    yield_stress_ratio_y_for_plasticity=Quantity(value=[1.0], units=""),
                    yield_stress_ratio_z_for_plasticity=Quantity(value=[1.0], units=""),
                    yield_stress_ratio_xy_for_plasticity=Quantity(value=[1.0], units=""),
                    yield_stress_ratio_xz_for_plasticity=Quantity(value=[1.0], units=""),
                    yield_stress_ratio_yz_for_plasticity=Quantity(value=[1.0], units=""),
                    yield_stress_ratio_x_for_creep=Quantity(value=[2.0], units=""),
                    yield_stress_ratio_y_for_creep=Quantity(value=[2.0], units=""),
                    yield_stress_ratio_z_for_creep=Quantity(value=[2.0], units=""),
                    yield_stress_ratio_xy_for_creep=Quantity(value=[2.0], units=""),
                    yield_stress_ratio_xz_for_creep=Quantity(value=[2.0], units=""),
                    yield_stress_ratio_yz_for_creep=Quantity(value=[2.0], units=""),
                    independent_parameters=[
                        IndependentParameter(
                            name="Temperature",
                            values=Quantity(value=[7.88860905221012e-31], units="C"),
                            default_value=22.0,
                            field_variable="Temperature",
                            field_units="C",
                            upper_limit="Program Controlled",
                            lower_limit="Program Controlled",
                        ),
                    ],
                    interpolation_options=InterpolationOptions(
                        algorithm_type="Linear Multivariate",
                        cached=True,
                        normalized=True,
                    ),
                    model_qualifiers=[
                        ModelQualifier(
                            name="Separated Hill Potentials for Plasticity and Creep", value="Yes"
                        )
                    ],
                ),
            ],
        )
    ]

    writer = MatmlWriter(materials)
    tree = writer._to_etree()
    material_string, metadata_string = get_material_and_metadata_from_xml(tree)
    with open(HILL_YIELD_CREEP, 'r') as file:
        data = file.read()
        assert data == material_string
    with open(HILL_YIELD_CREEP_METADATA, 'r') as file:
      data = file.read()
      assert data == metadata_string


def test_write_kinematic_hardening():
    materials = [
        Material(
            name="SFRP",
            models=[
                KinematicHardening(
                    yield_stress=Quantity(value=[12.0], units="Pa"),
                    material_constant_gamma_1=Quantity(value=[1.0], units=""),
                    material_constant_c_1=Quantity(value=[45.0], units="Pa"),
                    independent_parameters=[
                        IndependentParameter(name="Temperature", values=Quantity(value=[7.88860905221012e-31], units="C")),
                    ],
                ),
            ],
        )
    ]

    writer = MatmlWriter(materials)
    tree = writer._to_etree()
    material_string, metadata_string = get_material_and_metadata_from_xml(tree)
    with open(KINEMATIC_HARDENING, 'r') as file:
        data = file.read()
        assert data == material_string
    with open(KINEMATIC_HARDENING_METADATA, 'r', encoding='utf-8') as file:
      data = file.read()
      assert data == metadata_string



def test_write_strain_hardening():
    materials = [
        Material(
            name="SFRP",
            models=[
                StrainHardening(
                    creep_constant_1=Quantity(value=[1.0], units=""),
                    creep_constant_2=Quantity(value=[2.0], units=""),
                    creep_constant_3=Quantity(value=[3.0], units=""),
                    creep_constant_4=Quantity(value=[4.0], units=""),
                    independent_parameters=[
                        IndependentParameter(name="Temperature", values=Quantity(value=[7.88860905221012e-31], units="C")),
                    ],
                    model_qualifiers=[
                        ModelQualifier(
                            name="Reference Units (Length, Time, Temperature, Force)",
                            value="m, s, K, N",
                        )
                    ],
                ),
            ],
        )
    ]

    writer = MatmlWriter(materials)
    tree = writer._to_etree()
    material_string, metadata_string = get_material_and_metadata_from_xml(tree)
    with open(STRAIN_HARDENING, 'r') as file:
        data = file.read()
        assert data == material_string
    with open(STRAIN_HARDENING_METADATA, 'r') as file:
      data = file.read()
      assert data == metadata_string