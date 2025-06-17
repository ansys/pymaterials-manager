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
from ansys.materials.manager._models._material_models.elasticity_anisotropic import (
    ElasticityAnisotropic,
)
from ansys.materials.manager._models._material_models.elasticity_isotropic import (
    ElasticityIsotropic,
)
from ansys.materials.manager._models._material_models.elasticity_orthotropic import (
    ElasticityOrthotropic,
)
from ansys.materials.manager._models.material import Material
from ansys.materials.manager.util.matml.matml_from_material import MatmlWriter

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
XML_FILE_PATH = os.path.join(DIR_PATH, "..", "data", "MatML_unittest_elasticity.xml")

ISOTROPIC_ELASTIC = """<?xml version="1.0" ?>
<Material>
  <BulkDetails>
    <Name>Isotropic Test Material</Name>
    <PropertyData property="pr0">
      <Data format="string">-</Data>
      <Qualifier name="Behavior">Isotropic</Qualifier>
      <ParameterValue parameter="pa0" format="string">
        <Data>Interpolation Options</Data>
        <Qualifier name="AlgorithmType">Linear Multivariate</Qualifier>
        <Qualifier name="Cached">True</Qualifier>
        <Qualifier name="Normalized">True</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa1" format="float">
        <Data>1000000.0</Data>
        <Qualifier name="Variable Type">Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa2" format="float">
        <Data>0.3</Data>
        <Qualifier name="Variable Type">Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa3" format="float">
        <Data>7.88860905221012e-31</Data>
        <Qualifier name="Variable Type">Independent</Qualifier>
        <Qualifier name="Field Variable">Temperarture</Qualifier>
        <Qualifier name="Default Data">22</Qualifier>
        <Qualifier name="Field Units">C</Qualifier>
        <Qualifier name="Upper Limit">1.18329135783152E-30</Qualifier>
        <Qualifier name="Lower Limit">3.94430452610506E-31</Qualifier>
      </ParameterValue>
    </PropertyData>
  </BulkDetails>
</Material>"""

ISOTROPIC_ELASTICITY_VARIABLE = """<?xml version="1.0" ?>
<Material>
  <BulkDetails>
    <Name>Variable Isotropic Test Material</Name>
    <PropertyData property="pr0">
      <Data format="string">-</Data>
      <Qualifier name="Behavior">Isotropic</Qualifier>
      <ParameterValue parameter="pa0" format="string">
        <Data>Interpolation Options</Data>
        <Qualifier name="AlgorithmType">Linear Multivariate</Qualifier>
        <Qualifier name="Cached">True</Qualifier>
        <Qualifier name="Normalized">True</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa1" format="float">
        <Data>2000000.0, 1000000.0</Data>
        <Qualifier name="Variable Type">Dependent,Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa2" format="float">
        <Data>0.35, 0.3</Data>
        <Qualifier name="Variable Type">Dependent,Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa3" format="float">
        <Data>12.0, 21.0</Data>
        <Qualifier name="Variable Type">Independent,Independent</Qualifier>
        <Qualifier name="Field Variable">Temperarture</Qualifier>
        <Qualifier name="Default Data">22</Qualifier>
        <Qualifier name="Field Units">C</Qualifier>
        <Qualifier name="Upper Limit">1.18329135783152E-30</Qualifier>
        <Qualifier name="Lower Limit">3.94430452610506E-31</Qualifier>
      </ParameterValue>
    </PropertyData>
  </BulkDetails>
</Material>"""

ORTHOTROPIC_ELASTICITY = """<?xml version="1.0" ?>
<Material>
  <BulkDetails>
    <Name>Orthotropic Test Material</Name>
    <PropertyData property="pr0">
      <Data format="string">-</Data>
      <Qualifier name="Behavior">Orthotropic</Qualifier>
      <ParameterValue parameter="pa0" format="string">
        <Data>Interpolation Options</Data>
        <Qualifier name="AlgorithmType">Linear Multivariate</Qualifier>
        <Qualifier name="Cached">True</Qualifier>
        <Qualifier name="Normalized">True</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa1" format="float">
        <Data>1000000.0</Data>
        <Qualifier name="Variable Type">Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa2" format="float">
        <Data>1500000.0</Data>
        <Qualifier name="Variable Type">Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa3" format="float">
        <Data>2000000.0</Data>
        <Qualifier name="Variable Type">Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa4" format="float">
        <Data>0.3</Data>
        <Qualifier name="Variable Type">Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa5" format="float">
        <Data>0.4</Data>
        <Qualifier name="Variable Type">Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa6" format="float">
        <Data>0.2</Data>
        <Qualifier name="Variable Type">Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa7" format="float">
        <Data>2000000.0</Data>
        <Qualifier name="Variable Type">Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa8" format="float">
        <Data>3000000.0</Data>
        <Qualifier name="Variable Type">Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa9" format="float">
        <Data>1000000.0</Data>
        <Qualifier name="Variable Type">Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa10" format="float">
        <Data>7.88860905221012e-31</Data>
        <Qualifier name="Variable Type">Independent</Qualifier>
        <Qualifier name="Field Variable">Temperarture</Qualifier>
        <Qualifier name="Default Data">22</Qualifier>
        <Qualifier name="Field Units">C</Qualifier>
        <Qualifier name="Upper Limit">1.18329135783152E-30</Qualifier>
        <Qualifier name="Lower Limit">3.94430452610506E-31</Qualifier>
      </ParameterValue>
    </PropertyData>
  </BulkDetails>
</Material>"""

ORTHOTROPIC_ELASTICITY_VARIABLE = """<?xml version="1.0" ?>
<Material>
  <BulkDetails>
    <Name>Variable Orthotropic Test Material</Name>
    <PropertyData property="pr0">
      <Data format="string">-</Data>
      <Qualifier name="Behavior">Orthotropic</Qualifier>
      <ParameterValue parameter="pa0" format="string">
        <Data>Interpolation Options</Data>
        <Qualifier name="AlgorithmType">Linear Multivariate</Qualifier>
        <Qualifier name="Cached">True</Qualifier>
        <Qualifier name="Normalized">True</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa1" format="float">
        <Data>1000000.0, 11000000.0</Data>
        <Qualifier name="Variable Type">Dependent,Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa2" format="float">
        <Data>1500000.0, 15100000.0</Data>
        <Qualifier name="Variable Type">Dependent,Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa3" format="float">
        <Data>2000000.0, 21000000.0</Data>
        <Qualifier name="Variable Type">Dependent,Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa4" format="float">
        <Data>0.3, 0.31</Data>
        <Qualifier name="Variable Type">Dependent,Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa5" format="float">
        <Data>0.4, 0.41</Data>
        <Qualifier name="Variable Type">Dependent,Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa6" format="float">
        <Data>0.2, 0.21</Data>
        <Qualifier name="Variable Type">Dependent,Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa7" format="float">
        <Data>2000000.0, 2100000.0</Data>
        <Qualifier name="Variable Type">Dependent,Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa8" format="float">
        <Data>3000000.0, 3100000.0</Data>
        <Qualifier name="Variable Type">Dependent,Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa9" format="float">
        <Data>1000000.0, 1100000.0</Data>
        <Qualifier name="Variable Type">Dependent,Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa10" format="float">
        <Data>21.0, 22.0</Data>
        <Qualifier name="Variable Type">Independent,Independent</Qualifier>
        <Qualifier name="Field Variable">Temperarture</Qualifier>
        <Qualifier name="Default Data">22</Qualifier>
        <Qualifier name="Field Units">C</Qualifier>
        <Qualifier name="Upper Limit">1.18329135783152E-30</Qualifier>
        <Qualifier name="Lower Limit">3.94430452610506E-31</Qualifier>
      </ParameterValue>
    </PropertyData>
  </BulkDetails>
</Material>"""

ANISOTROPIC_ELASTICITY = """<?xml version="1.0" ?>
<Material>
  <BulkDetails>
    <Name>Anisotropic Test Material</Name>
    <PropertyData property="pr0">
      <Data format="string">-</Data>
      <Qualifier name="Behavior">Anisotropic</Qualifier>
      <ParameterValue parameter="pa0" format="float">
        <Data>100000000.0, 1000000.0, 2000000.0, 3000000.0, 4000000.0, 5000000.0</Data>
        <Qualifier name="Variable Type">Dependent,Dependent,Dependent,Dependent,Dependent,Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa1" format="float">
        <Data>7.88860905221012e-31, 150000000.0, 6000000.0, 7000000.0, 8000000.0, 9000000.0</Data>
        <Qualifier name="Variable Type">Dependent,Dependent,Dependent,Dependent,Dependent,Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa2" format="float">
        <Data>7.88860905221012e-31, 7.88860905221012e-31, 200000000.0, 10000000.0, 11000000.0, 12000000.0</Data>
        <Qualifier name="Variable Type">Dependent,Dependent,Dependent,Dependent,Dependent,Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa3" format="float">
        <Data>7.88860905221012e-31, 7.88860905221012e-31, 7.88860905221012e-31, 50000000.0, 13000000.0, 14000000.0</Data>
        <Qualifier name="Variable Type">Dependent,Dependent,Dependent,Dependent,Dependent,Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa4" format="float">
        <Data>7.88860905221012e-31, 7.88860905221012e-31, 7.88860905221012e-31, 7.88860905221012e-31, 60000000.0, 15000000.0</Data>
        <Qualifier name="Variable Type">Dependent,Dependent,Dependent,Dependent,Dependent,Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa5" format="float">
        <Data>7.88860905221012e-31, 7.88860905221012e-31, 7.88860905221012e-31, 7.88860905221012e-31, 7.88860905221012e-31, 70000000.0</Data>
        <Qualifier name="Variable Type">Dependent,Dependent,Dependent,Dependent,Dependent,Dependent</Qualifier>
      </ParameterValue>
    </PropertyData>
  </BulkDetails>
</Material>"""  # noqa: E501

ISOTROPIC_ELASTICITY_METADATA = """<?xml version="1.0" ?>
<Metadata>
  <PropertyDetails id="pr0">
    <Unitless/>
    <Name>Elasticity</Name>
  </PropertyDetails>
  <ParameterDetails id="pa0">
    <Unitless/>
    <Name>Options Variable</Name>
  </ParameterDetails>
  <ParameterDetails id="pa1">
    <Unitless/>
    <Name>Young's Modulus</Name>
  </ParameterDetails>
  <ParameterDetails id="pa2">
    <Unitless/>
    <Name>Poisson's Ratio</Name>
  </ParameterDetails>
  <ParameterDetails id="pa3">
    <Unitless/>
    <Name>Temperature</Name>
  </ParameterDetails>
</Metadata>"""

ORTHOTROPIC_ELASTICITY_METADATA = """<?xml version="1.0" ?>
<Metadata>
  <PropertyDetails id="pr0">
    <Unitless/>
    <Name>Elasticity</Name>
  </PropertyDetails>
  <ParameterDetails id="pa0">
    <Unitless/>
    <Name>Options Variable</Name>
  </ParameterDetails>
  <ParameterDetails id="pa1">
    <Unitless/>
    <Name>Young's Modulus X direction</Name>
  </ParameterDetails>
  <ParameterDetails id="pa2">
    <Unitless/>
    <Name>Young's Modulus Y direction</Name>
  </ParameterDetails>
  <ParameterDetails id="pa3">
    <Unitless/>
    <Name>Young's Modulus Z direction</Name>
  </ParameterDetails>
  <ParameterDetails id="pa4">
    <Unitless/>
    <Name>Poisson's Ratio YZ</Name>
  </ParameterDetails>
  <ParameterDetails id="pa5">
    <Unitless/>
    <Name>Poisson's Ratio XZ</Name>
  </ParameterDetails>
  <ParameterDetails id="pa6">
    <Unitless/>
    <Name>Poisson's Ratio XY</Name>
  </ParameterDetails>
  <ParameterDetails id="pa7">
    <Unitless/>
    <Name>Shear Modulus YZ</Name>
  </ParameterDetails>
  <ParameterDetails id="pa8">
    <Unitless/>
    <Name>Shear Modulus XZ</Name>
  </ParameterDetails>
  <ParameterDetails id="pa9">
    <Unitless/>
    <Name>Shear Modulus XY</Name>
  </ParameterDetails>
  <ParameterDetails id="pa10">
    <Unitless/>
    <Name>Temperature</Name>
  </ParameterDetails>
</Metadata>"""

ANISOTROPIC_ELASTICITY_METADATA = """<?xml version="1.0" ?>
<Metadata>
  <PropertyDetails id="pr0">
    <Unitless/>
    <Name>Elasticity</Name>
  </PropertyDetails>
  <ParameterDetails id="pa0">
    <Unitless/>
    <Name>D[*,1]</Name>
  </ParameterDetails>
  <ParameterDetails id="pa1">
    <Unitless/>
    <Name>D[*,2]</Name>
  </ParameterDetails>
  <ParameterDetails id="pa2">
    <Unitless/>
    <Name>D[*,3]</Name>
  </ParameterDetails>
  <ParameterDetails id="pa3">
    <Unitless/>
    <Name>D[*,4]</Name>
  </ParameterDetails>
  <ParameterDetails id="pa4">
    <Unitless/>
    <Name>D[*,5]</Name>
  </ParameterDetails>
  <ParameterDetails id="pa5">
    <Unitless/>
    <Name>D[*,6]</Name>
  </ParameterDetails>
</Metadata>"""


def test_read_constant_elastic_isotropic_material():
    material_dic = read_matml_file(XML_FILE_PATH)
    assert "Isotropic Test Material" in material_dic.keys()
    assert len(material_dic["Isotropic Test Material"].models) == 2
    isotropic_elasticity = material_dic["Isotropic Test Material"].models[1]

    assert isotropic_elasticity.name == "Elasticity"
    assert isotropic_elasticity.model_qualifiers[0].name == "Behavior"
    assert isotropic_elasticity.model_qualifiers[0].value == "Isotropic"
    assert isotropic_elasticity.model_qualifiers[1].name == "Derive from"
    assert isotropic_elasticity.model_qualifiers[1].value == "Young's Modulus and Poisson's Ratio"
    assert isotropic_elasticity.model_qualifiers[2].name == "Field Variable Compatible"
    assert isotropic_elasticity.model_qualifiers[2].value == "Temperature"
    assert isotropic_elasticity.interpolation_options.algorithm_type == "Linear Multivariate"
    assert isotropic_elasticity.interpolation_options.cached == True
    assert isotropic_elasticity.interpolation_options.normalized == True
    assert isotropic_elasticity.independent_parameters[0].name == "Temperature"
    assert isotropic_elasticity.independent_parameters[0].values == [7.88860905221012e-31]
    assert isotropic_elasticity.independent_parameters[0].units == "C"
    assert isotropic_elasticity.independent_parameters[0].upper_limit == "1.18329135783152E-30"
    assert isotropic_elasticity.independent_parameters[0].lower_limit == "3.94430452610506E-31"
    assert isotropic_elasticity.independent_parameters[0].default_value == "22"
    assert isotropic_elasticity.youngs_modulus == [1000000.0]
    assert isotropic_elasticity.poissons_ratio == [0.3]


def test_read_constant_elastic_orthotropic_material():
    material_dic = read_matml_file(XML_FILE_PATH)
    assert "Orthotropic Test Material" in material_dic.keys()
    assert len(material_dic["Orthotropic Test Material"].models) == 2
    orthotropic_elasticity = material_dic["Orthotropic Test Material"].models[1]
    assert orthotropic_elasticity.name == "Elasticity"
    assert orthotropic_elasticity.model_qualifiers[0].name == "Behavior"
    assert orthotropic_elasticity.model_qualifiers[0].value == "Orthotropic"
    assert orthotropic_elasticity.model_qualifiers[1].name == "Field Variable Compatible"
    assert orthotropic_elasticity.model_qualifiers[1].value == "Temperature"
    assert orthotropic_elasticity.interpolation_options.algorithm_type == "Linear Multivariate"
    assert orthotropic_elasticity.interpolation_options.cached == True
    assert orthotropic_elasticity.interpolation_options.normalized == True
    assert orthotropic_elasticity.youngs_modulus_x == [10000000.0]
    assert orthotropic_elasticity.youngs_modulus_y == [15000000.0]
    assert orthotropic_elasticity.youngs_modulus_z == [20000000.0]
    assert orthotropic_elasticity.poissons_ratio_xy == [0.2]
    assert orthotropic_elasticity.poissons_ratio_yz == [0.3]
    assert orthotropic_elasticity.poissons_ratio_xz == [0.4]
    assert orthotropic_elasticity.shear_modulus_xy == [1000000.0]
    assert orthotropic_elasticity.shear_modulus_yz == [2000000.0]
    assert orthotropic_elasticity.shear_modulus_xz == [3000000.0]
    assert orthotropic_elasticity.independent_parameters[0].name == "Temperature"
    assert orthotropic_elasticity.independent_parameters[0].values == [7.88860905221012e-31]
    assert orthotropic_elasticity.independent_parameters[0].units == "C"
    assert orthotropic_elasticity.independent_parameters[0].upper_limit == "1.18329135783152E-30"
    assert orthotropic_elasticity.independent_parameters[0].lower_limit == "3.94430452610506E-31"
    assert orthotropic_elasticity.independent_parameters[0].default_value == "22"


def test_read_constant_elastic_anisotropic_material():
    material_dic = read_matml_file(XML_FILE_PATH)
    assert "Anisotropic Test Material" in material_dic.keys()
    assert len(material_dic["Anisotropic Test Material"].models) == 2
    orthotropic_elasticity = material_dic["Anisotropic Test Material"].models[1]
    assert orthotropic_elasticity.name == "Elasticity"
    assert orthotropic_elasticity.model_qualifiers[0].name == "Behavior"
    assert orthotropic_elasticity.model_qualifiers[0].value == "Anisotropic"
    assert orthotropic_elasticity.column_1 == [
        100000000,
        1000000,
        2000000,
        3000000,
        4000000,
        5000000,
    ]
    assert orthotropic_elasticity.column_2 == [
        7.88860905221012e-31,
        150000000,
        6000000,
        7000000,
        8000000,
        9000000,
    ]
    assert orthotropic_elasticity.column_3 == [
        7.88860905221012e-31,
        7.88860905221012e-31,
        200000000,
        10000000,
        11000000,
        12000000,
    ]
    assert orthotropic_elasticity.column_4 == [
        7.88860905221012e-31,
        7.88860905221012e-31,
        7.88860905221012e-31,
        50000000,
        13000000,
        14000000,
    ]
    assert orthotropic_elasticity.column_5 == [
        7.88860905221012e-31,
        7.88860905221012e-31,
        7.88860905221012e-31,
        7.88860905221012e-31,
        60000000,
        15000000,
    ]
    assert orthotropic_elasticity.column_6 == [
        7.88860905221012e-31,
        7.88860905221012e-31,
        7.88860905221012e-31,
        7.88860905221012e-31,
        7.88860905221012e-31,
        70000000,
    ]


def test_read_variable_elastic_isotropic_material():
    material_dic = read_matml_file(XML_FILE_PATH)
    assert "Variable Isotropic Test Material" in material_dic.keys()
    assert len(material_dic["Variable Isotropic Test Material"].models) == 2
    isotropic_elasticity = material_dic["Variable Isotropic Test Material"].models[1]
    assert isotropic_elasticity.name == "Elasticity"
    assert isotropic_elasticity.model_qualifiers[0].name == "Behavior"
    assert isotropic_elasticity.model_qualifiers[0].value == "Isotropic"
    assert isotropic_elasticity.model_qualifiers[1].name == "Derive from"
    assert isotropic_elasticity.model_qualifiers[1].value == "Young's Modulus and Poisson's Ratio"
    assert isotropic_elasticity.model_qualifiers[2].name == "Field Variable Compatible"
    assert isotropic_elasticity.model_qualifiers[2].value == "Temperature"
    assert isotropic_elasticity.interpolation_options.algorithm_type == "Linear Multivariate"
    assert isotropic_elasticity.interpolation_options.cached == True
    assert isotropic_elasticity.interpolation_options.normalized == True
    assert isotropic_elasticity.independent_parameters[0].name == "Temperature"
    assert isotropic_elasticity.independent_parameters[0].values == [12, 21]
    assert isotropic_elasticity.independent_parameters[0].units == "C"
    assert isotropic_elasticity.independent_parameters[0].upper_limit == "1.18329135783152E-30"
    assert isotropic_elasticity.independent_parameters[0].lower_limit == "3.94430452610506E-31"
    assert isotropic_elasticity.independent_parameters[0].default_value == "22"
    assert isotropic_elasticity.youngs_modulus == [2000000, 1000000]
    assert isotropic_elasticity.poissons_ratio == [0.35, 0.3]


def test_read_variable_elastic_orthotropic_material():
    material_dic = read_matml_file(XML_FILE_PATH)
    assert "Variable Orthotropic Test Material" in material_dic.keys()
    assert len(material_dic["Variable Orthotropic Test Material"].models) == 2
    orthotropic_elasticity = material_dic["Variable Orthotropic Test Material"].models[1]
    assert orthotropic_elasticity.name == "Elasticity"
    assert orthotropic_elasticity.model_qualifiers[0].name == "Behavior"
    assert orthotropic_elasticity.model_qualifiers[0].value == "Orthotropic"
    assert orthotropic_elasticity.model_qualifiers[1].name == "Field Variable Compatible"
    assert orthotropic_elasticity.model_qualifiers[1].value == "Temperature"
    assert orthotropic_elasticity.interpolation_options.algorithm_type == "Linear Multivariate"
    assert orthotropic_elasticity.interpolation_options.cached == True
    assert orthotropic_elasticity.interpolation_options.normalized == True
    assert orthotropic_elasticity.youngs_modulus_x == [10000000.0, 11000000.0]
    assert orthotropic_elasticity.youngs_modulus_y == [15000000.0, 15100000]
    assert orthotropic_elasticity.youngs_modulus_z == [20000000.0, 21000000]
    assert orthotropic_elasticity.poissons_ratio_xy == [0.2, 0.21]
    assert orthotropic_elasticity.poissons_ratio_yz == [0.3, 0.31]
    assert orthotropic_elasticity.poissons_ratio_xz == [0.4, 0.41]
    assert orthotropic_elasticity.shear_modulus_xy == [1000000.0, 1100000]
    assert orthotropic_elasticity.shear_modulus_yz == [2000000.0, 2100000]
    assert orthotropic_elasticity.shear_modulus_xz == [3000000.0, 3100000]
    assert orthotropic_elasticity.independent_parameters[0].name == "Temperature"
    assert orthotropic_elasticity.independent_parameters[0].values == [21, 22]
    assert orthotropic_elasticity.independent_parameters[0].units == "C"
    assert orthotropic_elasticity.independent_parameters[0].upper_limit == "1.18329135783152E-30"
    assert orthotropic_elasticity.independent_parameters[0].lower_limit == "3.94430452610506E-31"
    assert orthotropic_elasticity.independent_parameters[0].default_value == "22"


def test_write_constant_elastic_isotropic_material():
    materials = [
        Material(
            name="Isotropic Test Material",
            models=[
                ElasticityIsotropic(
                    youngs_modulus=[1000000],
                    poissons_ratio=[0.3],
                    independent_parameters=[
                        IndependentParameter(
                            name="Temperature",
                            field_variable="Temperarture",
                            default_value="22",
                            upper_limit="1.18329135783152E-30",
                            lower_limit="3.94430452610506E-31",
                            values=[7.88860905221012e-31],
                            units="C",
                        )
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
    assert material_string == ISOTROPIC_ELASTIC
    assert metadata_string == ISOTROPIC_ELASTICITY_METADATA


def test_write_constant_elastic_orthotropic_material():
    materials = [
        Material(
            name="Orthotropic Test Material",
            models=[
                ElasticityOrthotropic(
                    youngs_modulus_x=[1000000],
                    youngs_modulus_y=[1500000],
                    youngs_modulus_z=[2000000],
                    poissons_ratio_xy=[0.2],
                    poissons_ratio_yz=[0.3],
                    poissons_ratio_xz=[0.4],
                    shear_modulus_xy=[1000000],
                    shear_modulus_yz=[2000000],
                    shear_modulus_xz=[3000000],
                    independent_parameters=[
                        IndependentParameter(
                            name="Temperature",
                            field_variable="Temperarture",
                            default_value="22",
                            upper_limit="1.18329135783152E-30",
                            lower_limit="3.94430452610506E-31",
                            values=[7.88860905221012e-31],
                            units="C",
                        )
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
    assert material_string == ORTHOTROPIC_ELASTICITY
    assert metadata_string == ORTHOTROPIC_ELASTICITY_METADATA


def test_write_constant_elastic_anisotropic_material():
    materials = [
        Material(
            name="Anisotropic Test Material",
            models=[
                ElasticityAnisotropic(
                    column_1=[100000000, 1000000, 2000000, 3000000, 4000000, 5000000],
                    column_2=[7.88860905221012e-31, 150000000, 6000000, 7000000, 8000000, 9000000],
                    column_3=[
                        7.88860905221012e-31,
                        7.88860905221012e-31,
                        200000000,
                        10000000,
                        11000000,
                        12000000,
                    ],
                    column_4=[
                        7.88860905221012e-31,
                        7.88860905221012e-31,
                        7.88860905221012e-31,
                        50000000,
                        13000000,
                        14000000,
                    ],
                    column_5=[
                        7.88860905221012e-31,
                        7.88860905221012e-31,
                        7.88860905221012e-31,
                        7.88860905221012e-31,
                        60000000,
                        15000000,
                    ],
                    column_6=[
                        7.88860905221012e-31,
                        7.88860905221012e-31,
                        7.88860905221012e-31,
                        7.88860905221012e-31,
                        7.88860905221012e-31,
                        70000000,
                    ],
                ),
            ],
        )
    ]

    writer = MatmlWriter(materials)
    tree = writer._to_etree()
    material_string, metadata_string = get_material_and_metadata_from_xml(tree)
    assert material_string == ANISOTROPIC_ELASTICITY
    assert metadata_string == ANISOTROPIC_ELASTICITY_METADATA


def test_write_variable_elastic_isotropic_material():
    materials = [
        Material(
            name="Variable Isotropic Test Material",
            models=[
                ElasticityIsotropic(
                    youngs_modulus=[2000000, 1000000],
                    poissons_ratio=[0.35, 0.3],
                    independent_parameters=[
                        IndependentParameter(
                            name="Temperature",
                            field_variable="Temperarture",
                            default_value="22",
                            upper_limit="1.18329135783152E-30",
                            lower_limit="3.94430452610506E-31",
                            values=[12.0, 21.0],
                            units="C",
                        )
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
    assert material_string == ISOTROPIC_ELASTICITY_VARIABLE
    assert metadata_string == ISOTROPIC_ELASTICITY_METADATA


def test_write_variable_elastic_orthotropic_material():
    materials = [
        Material(
            name="Variable Orthotropic Test Material",
            models=[
                ElasticityOrthotropic(
                    youngs_modulus_x=[1000000, 11000000],
                    youngs_modulus_y=[1500000, 15100000],
                    youngs_modulus_z=[2000000, 21000000],
                    poissons_ratio_xy=[0.2, 0.21],
                    poissons_ratio_yz=[0.3, 0.31],
                    poissons_ratio_xz=[0.4, 0.41],
                    shear_modulus_xy=[1000000, 1100000],
                    shear_modulus_yz=[2000000, 2100000],
                    shear_modulus_xz=[3000000, 3100000],
                    independent_parameters=[
                        IndependentParameter(
                            name="Temperature",
                            field_variable="Temperarture",
                            default_value="22",
                            upper_limit="1.18329135783152E-30",
                            lower_limit="3.94430452610506E-31",
                            values=[21.0, 22.0],
                            units="C",
                        )
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
    assert material_string == ORTHOTROPIC_ELASTICITY_VARIABLE
    assert metadata_string == ORTHOTROPIC_ELASTICITY_METADATA
