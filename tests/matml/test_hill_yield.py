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
from ansys.materials.manager._models._common.interpolation_options import InterpolationOptions
from ansys.materials.manager._models._common.model_qualifier import ModelQualifier
from ansys.materials.manager._models._material_models.hill_yield_criterion import HillYieldCriterion
from ansys.materials.manager._models._material_models.kinematic_hardening import KinematicHardening
from ansys.materials.manager._models._material_models.strain_hardening import StrainHardening
from ansys.materials.manager._models.material import Material
from ansys.materials.manager.util.matml.matml_from_material import MatmlWriter

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
NO_CREEP_XML_FILE_PATH = os.path.join(DIR_PATH, "..", "data", "MatML_unittest_hill_yield.xml")
CREEP_XML_FILE_PATH = os.path.join(DIR_PATH, "..", "data", "MatML_unittest_hill_yield_creep.xml")

HILL_YIELD = """<?xml version="1.0" ?>
<Material>
  <BulkDetails>
    <Name>SFRP</Name>
    <PropertyData property="pr0">
      <Data format="string">-</Data>
      <Qualifier name="Separated Hill Potentials for Plasticity and Creep">No</Qualifier>
      <ParameterValue parameter="pa0" format="string">
        <Data>Interpolation Options</Data>
        <Qualifier name="AlgorithmType">Linear Multivariate</Qualifier>
        <Qualifier name="Cached">True</Qualifier>
        <Qualifier name="Normalized">True</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa1" format="float">
        <Data>1.2</Data>
        <Qualifier name="Variable Type">Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa2" format="float">
        <Data>0.8</Data>
        <Qualifier name="Variable Type">Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa3" format="float">
        <Data>0.5</Data>
        <Qualifier name="Variable Type">Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa4" format="float">
        <Data>0.12</Data>
        <Qualifier name="Variable Type">Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa5" format="float">
        <Data>0.23</Data>
        <Qualifier name="Variable Type">Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa6" format="float">
        <Data>0.23</Data>
        <Qualifier name="Variable Type">Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa7" format="float">
        <Data>7.88860905221012e-31</Data>
        <Qualifier name="Variable Type">Independent</Qualifier>
        <Qualifier name="Field Variable">Temperature</Qualifier>
        <Qualifier name="Default Data">22.0</Qualifier>
        <Qualifier name="Field Units">C</Qualifier>
        <Qualifier name="Upper Limit">Program Controlled</Qualifier>
        <Qualifier name="Lower Limit">Program Controlled</Qualifier>
      </ParameterValue>
    </PropertyData>
  </BulkDetails>
</Material>"""

HILL_YIELD_VARIABLE = """<?xml version="1.0" ?>
<Material>
  <BulkDetails>
    <Name>SFRP Temp Dependent</Name>
    <PropertyData property="pr0">
      <Data format="string">-</Data>
      <Qualifier name="Separated Hill Potentials for Plasticity and Creep">No</Qualifier>
      <ParameterValue parameter="pa0" format="string">
        <Data>Interpolation Options</Data>
        <Qualifier name="AlgorithmType">Linear Multivariate</Qualifier>
        <Qualifier name="Cached">True</Qualifier>
        <Qualifier name="Normalized">True</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa1" format="float">
        <Data>1.2, 1.2, 1.4</Data>
        <Qualifier name="Variable Type">Dependent,Dependent,Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa2" format="float">
        <Data>0.8, 0.8, 0.7</Data>
        <Qualifier name="Variable Type">Dependent,Dependent,Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa3" format="float">
        <Data>0.5, 0.5, 0.4</Data>
        <Qualifier name="Variable Type">Dependent,Dependent,Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa4" format="float">
        <Data>0.12, 0.12, 0.12</Data>
        <Qualifier name="Variable Type">Dependent,Dependent,Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa5" format="float">
        <Data>0.23, 0.23, 0.23</Data>
        <Qualifier name="Variable Type">Dependent,Dependent,Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa6" format="float">
        <Data>0.23, 0.23, 0.23</Data>
        <Qualifier name="Variable Type">Dependent,Dependent,Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa7" format="float">
        <Data>34.0, 78.0, 245.0</Data>
        <Qualifier name="Variable Type">Independent,Independent,Independent</Qualifier>
        <Qualifier name="Field Variable">Temperature</Qualifier>
        <Qualifier name="Default Data">22.0</Qualifier>
        <Qualifier name="Field Units">C</Qualifier>
        <Qualifier name="Upper Limit">Program Controlled</Qualifier>
        <Qualifier name="Lower Limit">Program Controlled</Qualifier>
      </ParameterValue>
    </PropertyData>
  </BulkDetails>
</Material>"""

HILL_YIELD_CREEP = """<?xml version="1.0" ?>
<Material>
  <BulkDetails>
    <Name>SFRP</Name>
    <PropertyData property="pr0">
      <Data format="string">-</Data>
      <Qualifier name="Separated Hill Potentials for Plasticity and Creep">Yes</Qualifier>
      <ParameterValue parameter="pa0" format="string">
        <Data>Interpolation Options</Data>
        <Qualifier name="AlgorithmType">Linear Multivariate</Qualifier>
        <Qualifier name="Cached">True</Qualifier>
        <Qualifier name="Normalized">True</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa1" format="float">
        <Data>1.0</Data>
        <Qualifier name="Variable Type">Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa2" format="float">
        <Data>1.0</Data>
        <Qualifier name="Variable Type">Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa3" format="float">
        <Data>1.0</Data>
        <Qualifier name="Variable Type">Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa4" format="float">
        <Data>1.0</Data>
        <Qualifier name="Variable Type">Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa5" format="float">
        <Data>1.0</Data>
        <Qualifier name="Variable Type">Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa6" format="float">
        <Data>1.0</Data>
        <Qualifier name="Variable Type">Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa7" format="float">
        <Data>2.0</Data>
        <Qualifier name="Variable Type">Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa8" format="float">
        <Data>2.0</Data>
        <Qualifier name="Variable Type">Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa9" format="float">
        <Data>2.0</Data>
        <Qualifier name="Variable Type">Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa10" format="float">
        <Data>2.0</Data>
        <Qualifier name="Variable Type">Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa11" format="float">
        <Data>2.0</Data>
        <Qualifier name="Variable Type">Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa12" format="float">
        <Data>2.0</Data>
        <Qualifier name="Variable Type">Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa13" format="float">
        <Data>7.88860905221012e-31</Data>
        <Qualifier name="Variable Type">Independent</Qualifier>
        <Qualifier name="Field Variable">Temperature</Qualifier>
        <Qualifier name="Default Data">22.0</Qualifier>
        <Qualifier name="Field Units">C</Qualifier>
        <Qualifier name="Upper Limit">Program Controlled</Qualifier>
        <Qualifier name="Lower Limit">Program Controlled</Qualifier>
      </ParameterValue>
    </PropertyData>
  </BulkDetails>
</Material>"""

KINEMATIC_HARDENING = """<?xml version="1.0" ?>
<Material>
  <BulkDetails>
    <Name>SFRP</Name>
    <PropertyData property="pr0">
      <Data format="string">-</Data>
      <Qualifier name="Definition">Chaboche</Qualifier>
      <Qualifier name="Number of Kinematic Models">1</Qualifier>
      <Qualifier name="source">ANSYS</Qualifier>
      <ParameterValue parameter="pa0" format="float">
        <Data>12.0</Data>
        <Qualifier name="Variable Type">Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa1" format="float">
        <Data>1.0</Data>
        <Qualifier name="Variable Type">Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa2" format="float">
        <Data>45.0</Data>
        <Qualifier name="Variable Type">Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa3" format="float">
        <Data>7.88860905221012e-31</Data>
        <Qualifier name="Variable Type">Independent</Qualifier>
      </ParameterValue>
    </PropertyData>
  </BulkDetails>
</Material>"""

STRAIN_HARDENING = """<?xml version="1.0" ?>
<Material>
  <BulkDetails>
    <Name>SFRP</Name>
    <PropertyData property="pr0">
      <Data format="string">-</Data>
      <Qualifier name="Reference Units (Length, Time, Temperature, Force)">m, s, K, N</Qualifier>
      <ParameterValue parameter="pa0" format="float">
        <Data>1.0</Data>
        <Qualifier name="Variable Type">Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa1" format="float">
        <Data>2.0</Data>
        <Qualifier name="Variable Type">Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa2" format="float">
        <Data>3.0</Data>
        <Qualifier name="Variable Type">Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa3" format="float">
        <Data>4.0</Data>
        <Qualifier name="Variable Type">Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa4" format="float">
        <Data>7.88860905221012e-31</Data>
        <Qualifier name="Variable Type">Independent</Qualifier>
      </ParameterValue>
    </PropertyData>
  </BulkDetails>
</Material>"""

HILL_YIELD_METADATA = """<?xml version="1.0" ?>
<Metadata>
  <PropertyDetails id="pr0">
    <Unitless/>
    <Name>Hill Yield Criterion</Name>
  </PropertyDetails>
  <ParameterDetails id="pa0">
    <Unitless/>
    <Name>Options Variable</Name>
  </ParameterDetails>
  <ParameterDetails id="pa1">
    <Unitless/>
    <Name>Yield stress ratio in X direction</Name>
  </ParameterDetails>
  <ParameterDetails id="pa2">
    <Unitless/>
    <Name>Yield stress ratio in Y direction</Name>
  </ParameterDetails>
  <ParameterDetails id="pa3">
    <Unitless/>
    <Name>Yield stress ratio in Z direction</Name>
  </ParameterDetails>
  <ParameterDetails id="pa4">
    <Unitless/>
    <Name>Yield stress ratio in XY direction</Name>
  </ParameterDetails>
  <ParameterDetails id="pa5">
    <Unitless/>
    <Name>Yield stress ratio in XZ direction</Name>
  </ParameterDetails>
  <ParameterDetails id="pa6">
    <Unitless/>
    <Name>Yield stress ratio in YZ direction</Name>
  </ParameterDetails>
  <ParameterDetails id="pa7">
    <Unitless/>
    <Name>Temperature</Name>
  </ParameterDetails>
</Metadata>"""

HILL_YIELD_CREEP_METADATA = """<?xml version="1.0" ?>
<Metadata>
  <PropertyDetails id="pr0">
    <Unitless/>
    <Name>Hill Yield Criterion</Name>
  </PropertyDetails>
  <ParameterDetails id="pa0">
    <Unitless/>
    <Name>Options Variable</Name>
  </ParameterDetails>
  <ParameterDetails id="pa1">
    <Unitless/>
    <Name>Yield stress ratio in X direction for plasticity</Name>
  </ParameterDetails>
  <ParameterDetails id="pa2">
    <Unitless/>
    <Name>Yield stress ratio in Y direction for plasticity</Name>
  </ParameterDetails>
  <ParameterDetails id="pa3">
    <Unitless/>
    <Name>Yield stress ratio in Z direction for plasticity</Name>
  </ParameterDetails>
  <ParameterDetails id="pa4">
    <Unitless/>
    <Name>Yield stress ratio in XY direction for plasticity</Name>
  </ParameterDetails>
  <ParameterDetails id="pa5">
    <Unitless/>
    <Name>Yield stress ratio in XZ direction for plasticity</Name>
  </ParameterDetails>
  <ParameterDetails id="pa6">
    <Unitless/>
    <Name>Yield stress ratio in YZ direction for plasticity</Name>
  </ParameterDetails>
  <ParameterDetails id="pa7">
    <Unitless/>
    <Name>Yield stress ratio in X direction for creep</Name>
  </ParameterDetails>
  <ParameterDetails id="pa8">
    <Unitless/>
    <Name>Yield stress ratio in Y direction for creep</Name>
  </ParameterDetails>
  <ParameterDetails id="pa9">
    <Unitless/>
    <Name>Yield stress ratio in Z direction for creep</Name>
  </ParameterDetails>
  <ParameterDetails id="pa10">
    <Unitless/>
    <Name>Yield stress ratio in XY direction for creep</Name>
  </ParameterDetails>
  <ParameterDetails id="pa11">
    <Unitless/>
    <Name>Yield stress ratio in XZ direction for creep</Name>
  </ParameterDetails>
  <ParameterDetails id="pa12">
    <Unitless/>
    <Name>Yield stress ratio in YZ direction for creep</Name>
  </ParameterDetails>
  <ParameterDetails id="pa13">
    <Unitless/>
    <Name>Temperature</Name>
  </ParameterDetails>
</Metadata>"""

KINEMATIC_HARDENING_METADATA = """<?xml version="1.0" ?>
<Metadata>
  <PropertyDetails id="pr0">
    <Unitless/>
    <Name>Kinematic Hardening</Name>
  </PropertyDetails>
  <ParameterDetails id="pa0">
    <Unitless/>
    <Name>Yield Stress</Name>
  </ParameterDetails>
  <ParameterDetails id="pa1">
    <Unitless/>
    <Name>Material Constant γ1</Name>
  </ParameterDetails>
  <ParameterDetails id="pa2">
    <Unitless/>
    <Name>Material Constant C1</Name>
  </ParameterDetails>
  <ParameterDetails id="pa3">
    <Unitless/>
    <Name>Temperature</Name>
  </ParameterDetails>
</Metadata>"""

STRAIN_HARDENING_METADATA = """<?xml version="1.0" ?>
<Metadata>
  <PropertyDetails id="pr0">
    <Unitless/>
    <Name>Strain Hardening</Name>
  </PropertyDetails>
  <ParameterDetails id="pa0">
    <Unitless/>
    <Name>Creep Constant 1</Name>
  </ParameterDetails>
  <ParameterDetails id="pa1">
    <Unitless/>
    <Name>Creep Constant 2</Name>
  </ParameterDetails>
  <ParameterDetails id="pa2">
    <Unitless/>
    <Name>Creep Constant 3</Name>
  </ParameterDetails>
  <ParameterDetails id="pa3">
    <Unitless/>
    <Name>Creep Constant 4</Name>
  </ParameterDetails>
  <ParameterDetails id="pa4">
    <Unitless/>
    <Name>Temperature</Name>
  </ParameterDetails>
</Metadata>"""


def test_read_constant_hill_yield_no_creep():
    material_dic = read_matml_file(NO_CREEP_XML_FILE_PATH)
    assert "SFRP" in material_dic.keys()
    assert len(material_dic["SFRP"].models) == 3
    hill_yield = material_dic["SFRP"].models[2]
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
    assert hill_yield.yield_stress_ratio_x == [1.2]
    assert hill_yield.yield_stress_ratio_xy == [0.12]
    assert hill_yield.yield_stress_ratio_xz == [0.23]
    assert hill_yield.yield_stress_ratio_y == [0.8]
    assert hill_yield.yield_stress_ratio_yz == [0.23]
    assert hill_yield.yield_stress_ratio_z == [0.5]
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
    assert hill_yield.independent_parameters[0].unit == "C"
    assert hill_yield.independent_parameters[0].default_value == 22.0
    assert hill_yield.independent_parameters[0].upper_limit == "Program Controlled"
    assert hill_yield.independent_parameters[0].lower_limit == "Program Controlled"


def test_read_variable_temp_hill_yield_no_creep():
    material_dic = read_matml_file(NO_CREEP_XML_FILE_PATH)
    assert "SFRP Temp Dependent" in material_dic.keys()
    assert len(material_dic["SFRP Temp Dependent"].models) == 3
    hill_yield = material_dic["SFRP Temp Dependent"].models[2]
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
    assert hill_yield.yield_stress_ratio_x == [1.2, 1.2, 1.4]
    assert hill_yield.yield_stress_ratio_xy == [0.12, 0.12, 0.12]
    assert hill_yield.yield_stress_ratio_xz == [0.23, 0.23, 0.23]
    assert hill_yield.yield_stress_ratio_y == [0.8, 0.8, 0.7]
    assert hill_yield.yield_stress_ratio_yz == [0.23, 0.23, 0.23]
    assert hill_yield.yield_stress_ratio_z == [0.5, 0.5, 0.4]
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
    assert hill_yield.independent_parameters[0].values == [34, 78, 245]
    assert hill_yield.independent_parameters[0].unit == "C"
    assert hill_yield.independent_parameters[0].default_value == 22.0
    assert hill_yield.independent_parameters[0].upper_limit == "Program Controlled"
    assert hill_yield.independent_parameters[0].lower_limit == "Program Controlled"


def test_read_variable_hill_yield_no_creep():
    material_dic = read_matml_file(NO_CREEP_XML_FILE_PATH)
    assert "Variable Short Fiber" in material_dic.keys()
    assert len(material_dic["Variable Short Fiber"].models) == 2
    hill_yield = material_dic["Variable Short Fiber"].models[0]
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
    assert hill_yield.yield_stress_ratio_x == [
        1.0,
        1.38717930847789,
        3.00721990713311,
        1.2181891328774,
        1.0,
        1.38717930847789,
        1.0,
    ]
    assert hill_yield.yield_stress_ratio_xy == [
        1.27583858742812,
        1.27583858742812,
        1.27583858742812,
        1.27583858742812,
        1.27583858742812,
        1.27583858742812,
        1.27583858742812,
    ]
    assert hill_yield.yield_stress_ratio_xz == [
        1.27583858742812,
        1.27583858742812,
        1.27583858742812,
        1.27583858742812,
        1.27583858742812,
        1.27583858742812,
        1.27583858742812,
    ]
    assert hill_yield.yield_stress_ratio_y == [
        1.0,
        1.0,
        1.0,
        1.2181891328774,
        1.38717930847789,
        1.38717930847789,
        3.00721990713311,
    ]
    assert hill_yield.yield_stress_ratio_yz == [
        1.27583858742812,
        1.27583858742812,
        1.27583858742812,
        1.27583858742812,
        1.27583858742812,
        1.27583858742812,
        1.27583858742812,
    ]
    assert hill_yield.yield_stress_ratio_z == [
        3.00721990713311,
        1.38717930847789,
        1.0,
        1.21818913296279,
        1.38717930847789,
        1.0,
        1.0,
    ]
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
    assert hill_yield.independent_parameters[0].values == [0, 0.5, 1, 0.3333333333, 0, 0.5, 0]
    assert hill_yield.independent_parameters[0].default_value == "Program Controlled"
    assert hill_yield.independent_parameters[0].upper_limit == "Program Controlled"
    assert hill_yield.independent_parameters[0].lower_limit == "Program Controlled"
    assert hill_yield.independent_parameters[1].name == "Orientation Tensor A22"
    assert hill_yield.independent_parameters[1].values == [0, 0, 0, 0.3333333333, 0.5, 0.5, 1]
    assert hill_yield.independent_parameters[1].default_value == "Program Controlled"
    assert hill_yield.independent_parameters[1].upper_limit == "Program Controlled"
    assert hill_yield.independent_parameters[1].lower_limit == "Program Controlled"


def test_read_constant_hill_yield_creep():
    material_dic = read_matml_file(CREEP_XML_FILE_PATH)
    assert "SFRP" in material_dic.keys()
    assert len(material_dic["SFRP"].models) == 5
    hill_yield = material_dic["SFRP"].models[2]
    assert hill_yield.name == "Hill Yield Criterion"
    assert (
        hill_yield.model_qualifiers[0].name == "Separated Hill Potentials for Plasticity and Creep"
    )
    assert hill_yield.model_qualifiers[0].value == "Yes"
    assert hill_yield.yield_stress_ratio_x == None
    assert hill_yield.yield_stress_ratio_xy == None
    assert hill_yield.yield_stress_ratio_xz == None
    assert hill_yield.yield_stress_ratio_y == None
    assert hill_yield.yield_stress_ratio_yz == None
    assert hill_yield.yield_stress_ratio_z == None
    assert hill_yield.yield_stress_ratio_x_for_plasticity == [1.0]
    assert hill_yield.yield_stress_ratio_y_for_plasticity == [1.0]
    assert hill_yield.yield_stress_ratio_z_for_plasticity == [1.0]
    assert hill_yield.yield_stress_ratio_xy_for_plasticity == [1.0]
    assert hill_yield.yield_stress_ratio_xz_for_plasticity == [1.0]
    assert hill_yield.yield_stress_ratio_yz_for_plasticity == [1.0]
    assert hill_yield.yield_stress_ratio_x_for_creep == [2.0]
    assert hill_yield.yield_stress_ratio_y_for_creep == [2.0]
    assert hill_yield.yield_stress_ratio_z_for_creep == [2.0]
    assert hill_yield.yield_stress_ratio_xy_for_creep == [2.0]
    assert hill_yield.yield_stress_ratio_xz_for_creep == [2.0]
    assert hill_yield.yield_stress_ratio_yz_for_creep == [2.0]
    assert hill_yield.independent_parameters[0].name == "Temperature"
    assert hill_yield.independent_parameters[0].values == [7.88860905221012e-31]


def test_read_constant_kinematic_hardening_creep():
    material_dic = read_matml_file(CREEP_XML_FILE_PATH)
    assert "SFRP" in material_dic.keys()
    assert len(material_dic["SFRP"].models) == 5
    kinematic_hardening = material_dic["SFRP"].models[3]
    assert kinematic_hardening.name == "Kinematic Hardening"
    assert kinematic_hardening.model_qualifiers[0].name == "Definition"
    assert kinematic_hardening.model_qualifiers[0].value == "Chaboche"
    assert kinematic_hardening.model_qualifiers[1].name == "Number of Kinematic Models"
    assert kinematic_hardening.model_qualifiers[1].value == "1"
    assert kinematic_hardening.model_qualifiers[2].name == "source"
    assert kinematic_hardening.model_qualifiers[2].value == "ANSYS"
    assert kinematic_hardening.yield_stress == [12.0]
    assert kinematic_hardening.material_constant_gamma_1 == [1.0]
    assert kinematic_hardening.material_constant_c_1 == [45.0]
    assert kinematic_hardening.material_constant_gamma_2 == None
    assert kinematic_hardening.material_constant_c_2 == None
    assert kinematic_hardening.material_constant_gamma_3 == None
    assert kinematic_hardening.material_constant_c_3 == None
    assert kinematic_hardening.material_constant_gamma_4 == None
    assert kinematic_hardening.material_constant_c_4 == None
    assert kinematic_hardening.material_constant_gamma_5 == None
    assert kinematic_hardening.material_constant_c_5 == None
    assert kinematic_hardening.independent_parameters[0].name == "Temperature"
    assert kinematic_hardening.independent_parameters[0].values == [7.88860905221012e-31]


def test_read_constant_strain_hardening_creep():
    material_dic = read_matml_file(CREEP_XML_FILE_PATH)
    assert "SFRP" in material_dic.keys()
    assert len(material_dic["SFRP"].models) == 5
    strain_hardening = material_dic["SFRP"].models[4]
    assert strain_hardening.name == "Strain Hardening"
    assert (
        strain_hardening.model_qualifiers[0].name
        == "Reference Units (Length, Time, Temperature, Force)"
    )
    assert strain_hardening.model_qualifiers[0].value == "m, s, K, N"
    assert strain_hardening.creep_constant_1 == [1.0]
    assert strain_hardening.creep_constant_2 == [2.0]
    assert strain_hardening.creep_constant_3 == [3.0]
    assert strain_hardening.creep_constant_4 == [4.0]
    assert strain_hardening.independent_parameters[0].name == "Temperature"
    assert strain_hardening.independent_parameters[0].values == [7.88860905221012e-31]


def test_write_constant_hill_yield_no_creep():
    materials = [
        Material(
            name="SFRP",
            models=[
                HillYieldCriterion(
                    yield_stress_ratio_x=[1.2],
                    yield_stress_ratio_xy=[0.12],
                    yield_stress_ratio_xz=[0.23],
                    yield_stress_ratio_y=[0.8],
                    yield_stress_ratio_yz=[0.23],
                    yield_stress_ratio_z=[0.5],
                    independent_parameters=[
                        IndependentParameter(
                            name="Temperature",
                            field_variable="Temperature",
                            values=[7.88860905221012e-31],
                            default_value=22.0,
                            unit="C",
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
    assert material_string == HILL_YIELD
    assert metadata_string == HILL_YIELD_METADATA


def test_write_variable_hill_yield_no_creep():
    materials = [
        Material(
            name="SFRP Temp Dependent",
            models=[
                HillYieldCriterion(
                    yield_stress_ratio_x=[1.2, 1.2, 1.4],
                    yield_stress_ratio_xy=[0.12, 0.12, 0.12],
                    yield_stress_ratio_xz=[0.23, 0.23, 0.23],
                    yield_stress_ratio_y=[0.8, 0.8, 0.7],
                    yield_stress_ratio_yz=[0.23, 0.23, 0.23],
                    yield_stress_ratio_z=[0.5, 0.5, 0.4],
                    independent_parameters=[
                        IndependentParameter(
                            name="Temperature",
                            field_variable="Temperature",
                            values=[34.0, 78.0, 245.0],
                            default_value=22.0,
                            unit="C",
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
    assert material_string == HILL_YIELD_VARIABLE
    assert metadata_string == HILL_YIELD_METADATA


def test_write_constant_hill_yield_creep():
    materials = [
        Material(
            name="SFRP",
            models=[
                HillYieldCriterion(
                    yield_stress_ratio_x_for_plasticity=[1.0],
                    yield_stress_ratio_y_for_plasticity=[1.0],
                    yield_stress_ratio_z_for_plasticity=[1.0],
                    yield_stress_ratio_xy_for_plasticity=[1.0],
                    yield_stress_ratio_xz_for_plasticity=[1.0],
                    yield_stress_ratio_yz_for_plasticity=[1.0],
                    yield_stress_ratio_x_for_creep=[2.0],
                    yield_stress_ratio_y_for_creep=[2.0],
                    yield_stress_ratio_z_for_creep=[2.0],
                    yield_stress_ratio_xy_for_creep=[2.0],
                    yield_stress_ratio_xz_for_creep=[2.0],
                    yield_stress_ratio_yz_for_creep=[2.0],
                    independent_parameters=[
                        IndependentParameter(
                            name="Temperature",
                            field_variable="Temperature",
                            values=[7.88860905221012e-31],
                            default_value=22.0,
                            unit="C",
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
    assert material_string == HILL_YIELD_CREEP
    assert metadata_string == HILL_YIELD_CREEP_METADATA


def test_write_kinematic_hardening():
    materials = [
        Material(
            name="SFRP",
            models=[
                KinematicHardening(
                    yield_stress=[12.0],
                    material_constant_gamma_1=[1.0],
                    material_constant_c_1=[45.0],
                    independent_parameters=[
                        IndependentParameter(name="Temperature", values=[7.88860905221012e-31]),
                    ],
                ),
            ],
        )
    ]

    writer = MatmlWriter(materials)
    tree = writer._to_etree()
    material_string, metadata_string = get_material_and_metadata_from_xml(tree)
    assert material_string == KINEMATIC_HARDENING
    assert metadata_string == KINEMATIC_HARDENING_METADATA


def test_write_strain_hardening():
    materials = [
        Material(
            name="SFRP",
            models=[
                StrainHardening(
                    creep_constant_1=[1.0],
                    creep_constant_2=[2.0],
                    creep_constant_3=[3.0],
                    creep_constant_4=[4.0],
                    independent_parameters=[
                        IndependentParameter(name="Temperature", values=[7.88860905221012e-31]),
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
    assert material_string == STRAIN_HARDENING
    assert metadata_string == STRAIN_HARDENING_METADATA

# writer = MatmlWriter(materials)
# tree = writer._to_etree()
# material_string, metadata_string = get_material_and_metadata_from_xml(tree)
# writer.export("trial.xml", indent=True)

# path = r"D:\AnsysDev\pymaterials-manager\tests\data"
# with open(path + "\\ply_type.txt", "w") as text_file:
#     text_file.write(material_string)
# with open(path + "\\ply_type_metadata.txt", "w") as text_file:
#     text_file.write(metadata_string)

# # material_dic = read_matml_file(XML_FILE_PATH)
# # print("read")
