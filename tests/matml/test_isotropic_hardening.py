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
from ansys.materials.manager._models._material_models.isotropic_hardening import IsotropicHardening
from ansys.materials.manager._models._material_models.isotropic_hardening_voce_law import (
    IsotropicHardeningVoceLaw,
)
from ansys.materials.manager._models.material import Material
from ansys.materials.manager.util.matml.matml_from_material import MatmlWriter

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
VOCE_XML_FILE_PATH = os.path.join(
    DIR_PATH, "..", "data", "MatML_unittest_voce_isotropic_hardening.xml"
)
MULTILINEAR_XML_FILE_PATH = os.path.join(
    DIR_PATH, "..", "data", "MatML_unittest_multilinear_isotropic_hardening.xml"
)

MULTILINEAR = """<?xml version="1.0" ?>
<Material>
  <BulkDetails>
    <Name>SFRP</Name>
    <PropertyData property="pr0">
      <Data format="string">-</Data>
      <Qualifier name="Definition">Multilinear</Qualifier>
      <ParameterValue parameter="pa0" format="float">
        <Data>29.52801806, 30.93946596, 31.56895322, 32.83324607, 34.28804632, 35.45779394, 36.7206105, 37.86550163, 38.9800331, 40.37409873, 41.70507301, 42.87224516, 43.84021506, 44.94150614, 45.83281545, 46.81708774, 47.66814815, 48.32197593, 49.03683773, 49.69403185, 50.38934957, 50.9180887, 51.42733217, 52.07041013, 52.53035234, 52.99417352, 53.42471716, 54.00033621, 54.36001955, 54.71963936, 55.13624926</Data>
        <Qualifier name="Variable Type">Dependent,Dependent,Dependent,Dependent,Dependent,Dependent,Dependent,Dependent,Dependent,Dependent,Dependent,Dependent,Dependent,Dependent,Dependent,Dependent,Dependent,Dependent,Dependent,Dependent,Dependent,Dependent,Dependent,Dependent,Dependent,Dependent,Dependent,Dependent,Dependent,Dependent,Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa1" format="float">
        <Data>0.0, 0.000175189, 0.000257223, 0.00043005, 0.000643825, 0.000828966, 0.00104416, 0.001255108, 0.001477263, 0.00178269, 0.002108789, 0.002428809, 0.002723618, 0.003098638, 0.003439709, 0.003864545, 0.004281943, 0.004640923, 0.00507901, 0.005531357, 0.006070993, 0.006529747, 0.007015966, 0.007698042, 0.008235242, 0.008819543, 0.009399517, 0.010228087, 0.010773853, 0.011338467, 0.01201311</Data>
        <Qualifier name="Variable Type">Independent,Independent,Independent,Independent,Independent,Independent,Independent,Independent,Independent,Independent,Independent,Independent,Independent,Independent,Independent,Independent,Independent,Independent,Independent,Independent,Independent,Independent,Independent,Independent,Independent,Independent,Independent,Independent,Independent,Independent,Independent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa2" format="float">
        <Data>7.88860905221012e-31, 7.88860905221012e-31, 7.88860905221012e-31, 7.88860905221012e-31, 7.88860905221012e-31, 7.88860905221012e-31, 7.88860905221012e-31, 7.88860905221012e-31, 7.88860905221012e-31, 7.88860905221012e-31, 7.88860905221012e-31, 7.88860905221012e-31, 7.88860905221012e-31, 7.88860905221012e-31, 7.88860905221012e-31, 7.88860905221012e-31, 7.88860905221012e-31, 7.88860905221012e-31, 7.88860905221012e-31, 7.88860905221012e-31, 7.88860905221012e-31, 7.88860905221012e-31, 7.88860905221012e-31, 7.88860905221012e-31, 7.88860905221012e-31, 7.88860905221012e-31, 7.88860905221012e-31, 7.88860905221012e-31, 7.88860905221012e-31, 7.88860905221012e-31, 7.88860905221012e-31</Data>
        <Qualifier name="Variable Type">Independent,Independent,Independent,Independent,Independent,Independent,Independent,Independent,Independent,Independent,Independent,Independent,Independent,Independent,Independent,Independent,Independent,Independent,Independent,Independent,Independent,Independent,Independent,Independent,Independent,Independent,Independent,Independent,Independent,Independent,Independent</Qualifier>
      </ParameterValue>
    </PropertyData>
  </BulkDetails>
</Material>"""  # noqa: E501

MULTILINEAR_VARIABLE = """<?xml version="1.0" ?>
<Material>
  <BulkDetails>
    <Name>SFRP Temp Dependent</Name>
    <PropertyData property="pr0">
      <Data format="string">-</Data>
      <Qualifier name="Definition">Multilinear</Qualifier>
      <ParameterValue parameter="pa0" format="float">
        <Data>29.52801806, 30.93946596, 31.56895322, 32.83324607, 34.28804632, 35.45779394, 36.7206105, 37.86550163, 38.9800331, 40.37409873</Data>
        <Qualifier name="Variable Type">Dependent,Dependent,Dependent,Dependent,Dependent,Dependent,Dependent,Dependent,Dependent,Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa1" format="float">
        <Data>0.0, 0.000175189, 0.000257223, 0.00043005, 0.000643825, 0.000828966, 0.00104416, 0.001255108, 0.001477263, 0.00178269</Data>
        <Qualifier name="Variable Type">Independent,Independent,Independent,Independent,Independent,Independent,Independent,Independent,Independent,Independent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa2" format="float">
        <Data>22.0, 22.0, 22.0, 22.0, 22.0, 45.0, 45.0, 45.0, 45.0, 45.0</Data>
        <Qualifier name="Variable Type">Independent,Independent,Independent,Independent,Independent,Independent,Independent,Independent,Independent,Independent</Qualifier>
      </ParameterValue>
    </PropertyData>
  </BulkDetails>
</Material>"""  # noqa: E501

VOCE = """<?xml version="1.0" ?>
<Material>
  <BulkDetails>
    <Name>SFRP</Name>
    <PropertyData property="pr0">
      <Data format="string">-</Data>
      <Qualifier name="Behavior">Voce Law</Qualifier>
      <Qualifier name="Definition">Nonlinear</Qualifier>
      <ParameterValue parameter="pa0" format="float">
        <Data>28264641.0</Data>
        <Qualifier name="Variable Type">Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa1" format="float">
        <Data>526886855.0</Data>
        <Qualifier name="Variable Type">Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa2" format="float">
        <Data>18328164.0</Data>
        <Qualifier name="Variable Type">Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa3" format="float">
        <Data>406.479025</Data>
        <Qualifier name="Variable Type">Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa4" format="float">
        <Data>7.88860905221012e-31</Data>
        <Qualifier name="Variable Type">Independent</Qualifier>
      </ParameterValue>
    </PropertyData>
  </BulkDetails>
</Material>"""

VOCE_VARIABLE = """<?xml version="1.0" ?>
<Material>
  <BulkDetails>
    <Name>SFRP Temp Dependent</Name>
    <PropertyData property="pr0">
      <Data format="string">-</Data>
      <Qualifier name="Behavior">Voce Law</Qualifier>
      <Qualifier name="Definition">Nonlinear</Qualifier>
      <ParameterValue parameter="pa0" format="float">
        <Data>28264641.0, 34264641.0, 39264641.0</Data>
        <Qualifier name="Variable Type">Dependent,Dependent,Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa1" format="float">
        <Data>526886855.0, 670000000.0, 870000000.0</Data>
        <Qualifier name="Variable Type">Dependent,Dependent,Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa2" format="float">
        <Data>18328164.0, 15000000.0, 15347000.0</Data>
        <Qualifier name="Variable Type">Dependent,Dependent,Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa3" format="float">
        <Data>406.479025, 387.0, 387.0</Data>
        <Qualifier name="Variable Type">Dependent,Dependent,Dependent</Qualifier>
      </ParameterValue>
      <ParameterValue parameter="pa4" format="float">
        <Data>22.0, 112.4, 267.0</Data>
        <Qualifier name="Variable Type">Independent,Independent,Independent</Qualifier>
      </ParameterValue>
    </PropertyData>
  </BulkDetails>
</Material>"""  # noqa: E501

MULTILINEAR_METADATA = """<?xml version="1.0" ?>
<Metadata>
  <PropertyDetails id="pr0">
    <Unitless/>
    <Name>Isotropic Hardening</Name>
  </PropertyDetails>
  <ParameterDetails id="pa0">
    <Unitless/>
    <Name>Stress</Name>
  </ParameterDetails>
  <ParameterDetails id="pa1">
    <Unitless/>
    <Name>Plastic Strain</Name>
  </ParameterDetails>
  <ParameterDetails id="pa2">
    <Unitless/>
    <Name>Temperature</Name>
  </ParameterDetails>
</Metadata>"""

VOCE_METADATA = """<?xml version="1.0" ?>
<Metadata>
  <PropertyDetails id="pr0">
    <Unitless/>
    <Name>Isotropic Hardening</Name>
  </PropertyDetails>
  <ParameterDetails id="pa0">
    <Unitless/>
    <Name>Initial Yield Stress</Name>
  </ParameterDetails>
  <ParameterDetails id="pa1">
    <Unitless/>
    <Name>Linear Coefficient</Name>
  </ParameterDetails>
  <ParameterDetails id="pa2">
    <Unitless/>
    <Name>Exponential Coefficient</Name>
  </ParameterDetails>
  <ParameterDetails id="pa3">
    <Unitless/>
    <Name>Exponential Saturation Parameter</Name>
  </ParameterDetails>
  <ParameterDetails id="pa4">
    <Unitless/>
    <Name>Temperature</Name>
  </ParameterDetails>
</Metadata>"""


def test_read_constant_voce_isotropic_hardening_material():
    material_dic = read_matml_file(VOCE_XML_FILE_PATH)
    assert "SFRP" in material_dic.keys()
    assert len(material_dic["SFRP"].models) == 2
    isotropic_hardening = material_dic["SFRP"].models[1]
    assert isotropic_hardening.name == "Isotropic Hardening"
    assert isotropic_hardening.model_qualifiers[0].name == "Definition"
    assert isotropic_hardening.model_qualifiers[0].value == "Nonlinear"
    assert isotropic_hardening.model_qualifiers[1].name == "Behavior"
    assert isotropic_hardening.model_qualifiers[1].value == "Voce Law"
    assert isotropic_hardening.model_qualifiers[2].name == "Field Variable Compatible"
    assert isotropic_hardening.model_qualifiers[2].value == "Temperature"
    assert isotropic_hardening.initial_yield_stress.value == [28264641]
    assert isotropic_hardening.initial_yield_stress.unit == "Pa"
    assert isotropic_hardening.linear_coefficient.value == [526886855]
    assert isotropic_hardening.linear_coefficient.unit == "Pa"
    assert isotropic_hardening.exponential_coefficient.value == [18328164]
    assert isotropic_hardening.exponential_coefficient.unit == "Pa"
    assert isotropic_hardening.exponential_saturation_parameter.value == [406.479025]
    assert isotropic_hardening.exponential_saturation_parameter.unit == ""
    assert isotropic_hardening.independent_parameters[0].name == "Temperature"
    assert isotropic_hardening.independent_parameters[0].values.value == [7.88860905221012e-31]
    assert isotropic_hardening.independent_parameters[0].values.unit == "C"


def test_read_variable_voce_isotropic_hardening_material():
    material_dic = read_matml_file(VOCE_XML_FILE_PATH)
    assert "SFRP Temp Dependent" in material_dic.keys()
    assert len(material_dic["SFRP Temp Dependent"].models) == 2
    isotropic_hardening = material_dic["SFRP Temp Dependent"].models[1]
    assert isotropic_hardening.name == "Isotropic Hardening"
    assert isotropic_hardening.model_qualifiers[0].name == "Definition"
    assert isotropic_hardening.model_qualifiers[0].value == "Nonlinear"
    assert isotropic_hardening.model_qualifiers[1].name == "Behavior"
    assert isotropic_hardening.model_qualifiers[1].value == "Voce Law"
    assert isotropic_hardening.model_qualifiers[2].name == "Field Variable Compatible"
    assert isotropic_hardening.model_qualifiers[2].value == "Temperature"
    assert isotropic_hardening.initial_yield_stress.value.tolist() == [28264641, 34264641, 39264641]
    assert isotropic_hardening.initial_yield_stress.unit == "Pa"
    assert isotropic_hardening.linear_coefficient.value.tolist() == [526886855, 670000000, 870000000]
    assert isotropic_hardening.linear_coefficient.unit == "Pa"
    assert isotropic_hardening.exponential_coefficient.value.tolist() == [18328164, 15000000, 15347000]
    assert isotropic_hardening.exponential_coefficient.unit == "Pa"
    assert isotropic_hardening.exponential_saturation_parameter.value.tolist() == [406.479025, 387, 387]
    assert isotropic_hardening.exponential_saturation_parameter.unit == ""
    assert isotropic_hardening.independent_parameters[0].name == "Temperature"
    assert isotropic_hardening.independent_parameters[0].values.value.tolist() == [22, 112.4, 267]
    assert isotropic_hardening.independent_parameters[0].values.unit == "C"


def test_read_constant_multilinear_isotropic_hardening_material():
    material_dic = read_matml_file(MULTILINEAR_XML_FILE_PATH)
    assert "SFRP" in material_dic.keys()
    assert len(material_dic["SFRP"].models) == 2
    isotropic_hardening = material_dic["SFRP"].models[1]
    assert isotropic_hardening.name == "Isotropic Hardening"
    assert isotropic_hardening.model_qualifiers[0].name == "Definition"
    assert isotropic_hardening.model_qualifiers[0].value == "Multilinear"
    assert isotropic_hardening.stress.value.tolist() == [
        29.52801806,
        30.93946596,
        31.56895322,
        32.83324607,
        34.28804632,
        35.45779394,
        36.7206105,
        37.86550163,
        38.9800331,
        40.37409873,
        41.70507301,
        42.87224516,
        43.84021506,
        44.94150614,
        45.83281545,
        46.81708774,
        47.66814815,
        48.32197593,
        49.03683773,
        49.69403185,
        50.38934957,
        50.9180887,
        51.42733217,
        52.07041013,
        52.53035234,
        52.99417352,
        53.42471716,
        54.00033621,
        54.36001955,
        54.71963936,
        55.13624926,
    ]
    assert isotropic_hardening.stress.unit == "Pa"
    assert isotropic_hardening.independent_parameters[0].name == "Plastic Strain"
    assert isotropic_hardening.independent_parameters[0].values.value.tolist() == [
        0,
        0.000175189,
        0.000257223,
        0.00043005,
        0.000643825,
        0.000828966,
        0.00104416,
        0.001255108,
        0.001477263,
        0.00178269,
        0.002108789,
        0.002428809,
        0.002723618,
        0.003098638,
        0.003439709,
        0.003864545,
        0.004281943,
        0.004640923,
        0.00507901,
        0.005531357,
        0.006070993,
        0.006529747,
        0.007015966,
        0.007698042,
        0.008235242,
        0.008819543,
        0.009399517,
        0.010228087,
        0.010773853,
        0.011338467,
        0.01201311,
    ]
    assert isotropic_hardening.independent_parameters[0].values.unit == "m m^-1"
    assert isotropic_hardening.independent_parameters[1].name == "Temperature"
    assert isotropic_hardening.independent_parameters[1].values.value.tolist() == [
        7.88860905221012e-31,
        7.88860905221012e-31,
        7.88860905221012e-31,
        7.88860905221012e-31,
        7.88860905221012e-31,
        7.88860905221012e-31,
        7.88860905221012e-31,
        7.88860905221012e-31,
        7.88860905221012e-31,
        7.88860905221012e-31,
        7.88860905221012e-31,
        7.88860905221012e-31,
        7.88860905221012e-31,
        7.88860905221012e-31,
        7.88860905221012e-31,
        7.88860905221012e-31,
        7.88860905221012e-31,
        7.88860905221012e-31,
        7.88860905221012e-31,
        7.88860905221012e-31,
        7.88860905221012e-31,
        7.88860905221012e-31,
        7.88860905221012e-31,
        7.88860905221012e-31,
        7.88860905221012e-31,
        7.88860905221012e-31,
        7.88860905221012e-31,
        7.88860905221012e-31,
        7.88860905221012e-31,
        7.88860905221012e-31,
        7.88860905221012e-31,
    ]
    isotropic_hardening.independent_parameters[1].values.unit == "C"


def test_read_variable_multilinear_isotropic_hardening_material():
    material_dic = read_matml_file(MULTILINEAR_XML_FILE_PATH)
    assert "SFRP Temp Dependent" in material_dic.keys()
    assert len(material_dic["SFRP Temp Dependent"].models) == 2
    isotropic_hardening = material_dic["SFRP Temp Dependent"].models[1]
    assert isotropic_hardening.name == "Isotropic Hardening"
    assert isotropic_hardening.model_qualifiers[0].name == "Definition"
    assert isotropic_hardening.model_qualifiers[0].value == "Multilinear"
    assert isotropic_hardening.stress.value.tolist() == [
        29.52801806,
        30.93946596,
        31.56895322,
        32.83324607,
        34.28804632,
        35.45779394,
        36.7206105,
        37.86550163,
        38.9800331,
        40.37409873,
        41.70507301,
        42.87224516,
        43.84021506,
        44.94150614,
        45.83281545,
        46.81708774,
        47.66814815,
        48.32197593,
        49.03683773,
        49.69403185,
        50.38934957,
        50.9180887,
        51.42733217,
        52.07041013,
        52.53035234,
        52.99417352,
        53.42471716,
        54.00033621,
        54.36001955,
        54.71963936,
        55.13624926,
        43.48448168,
        45.56305263,
        46.49006801,
        48.35193084,
        50.4943447,
        52.21697535,
        54.07666411,
        55.76268982,
        57.40400632,
        59.45697923,
        61.41704058,
        63.13587846,
        64.56136083,
        66.18317886,
        67.4957669,
        68.94525701,
    ]
    assert isotropic_hardening.stress.unit == "Pa"
    assert isotropic_hardening.independent_parameters[0].name == "Plastic Strain"
    assert isotropic_hardening.independent_parameters[0].values.value.tolist() == [
        0,
        0.000175189,
        0.000257223,
        0.00043005,
        0.000643825,
        0.000828966,
        0.00104416,
        0.001255108,
        0.001477263,
        0.00178269,
        0.002108789,
        0.002428809,
        0.002723618,
        0.003098638,
        0.003439709,
        0.003864545,
        0.004281943,
        0.004640923,
        0.00507901,
        0.005531357,
        0.006070993,
        0.006529747,
        0.007015966,
        0.007698042,
        0.008235242,
        0.008819543,
        0.009399517,
        0.010228087,
        0.010773853,
        0.011338467,
        0.01201311,
        0,
        0.000175189,
        0.000257223,
        0.00043005,
        0.000643825,
        0.000828966,
        0.00104416,
        0.001255108,
        0.001477263,
        0.00178269,
        0.002108789,
        0.002428809,
        0.002723618,
        0.003098638,
        0.003439709,
        0.003864545,
    ]
    isotropic_hardening.independent_parameters[0].values.unit == "m m^-1"
    assert isotropic_hardening.independent_parameters[1].name == "Temperature"
    assert isotropic_hardening.independent_parameters[1].values.value.tolist() == [
        22,
        22,
        22,
        22,
        22,
        22,
        22,
        22,
        22,
        22,
        22,
        22,
        22,
        22,
        22,
        22,
        22,
        22,
        22,
        22,
        22,
        22,
        22,
        22,
        22,
        22,
        22,
        22,
        22,
        22,
        22,
        45,
        45,
        45,
        45,
        45,
        45,
        45,
        45,
        45,
        45,
        45,
        45,
        45,
        45,
        45,
        45,
    ]
    isotropic_hardening.independent_parameters[1].values.unit == "C"


def test_write_constant_multilinear_isotropic_hardening():
    materials = [
        Material(
            name="SFRP",
            models=[
                IsotropicHardening(
                    stress=[
                        29.52801806,
                        30.93946596,
                        31.56895322,
                        32.83324607,
                        34.28804632,
                        35.45779394,
                        36.7206105,
                        37.86550163,
                        38.9800331,
                        40.37409873,
                        41.70507301,
                        42.87224516,
                        43.84021506,
                        44.94150614,
                        45.83281545,
                        46.81708774,
                        47.66814815,
                        48.32197593,
                        49.03683773,
                        49.69403185,
                        50.38934957,
                        50.9180887,
                        51.42733217,
                        52.07041013,
                        52.53035234,
                        52.99417352,
                        53.42471716,
                        54.00033621,
                        54.36001955,
                        54.71963936,
                        55.13624926,
                    ],
                    independent_parameters=[
                        IndependentParameter(
                            name="Plastic Strain",
                            values=[
                                0.0,
                                0.000175189,
                                0.000257223,
                                0.00043005,
                                0.000643825,
                                0.000828966,
                                0.00104416,
                                0.001255108,
                                0.001477263,
                                0.00178269,
                                0.002108789,
                                0.002428809,
                                0.002723618,
                                0.003098638,
                                0.003439709,
                                0.003864545,
                                0.004281943,
                                0.004640923,
                                0.00507901,
                                0.005531357,
                                0.006070993,
                                0.006529747,
                                0.007015966,
                                0.007698042,
                                0.008235242,
                                0.008819543,
                                0.009399517,
                                0.010228087,
                                0.010773853,
                                0.011338467,
                                0.01201311,
                            ],
                        ),
                        IndependentParameter(
                            name="Temperature",
                            values=[
                                7.88860905221012e-31,
                                7.88860905221012e-31,
                                7.88860905221012e-31,
                                7.88860905221012e-31,
                                7.88860905221012e-31,
                                7.88860905221012e-31,
                                7.88860905221012e-31,
                                7.88860905221012e-31,
                                7.88860905221012e-31,
                                7.88860905221012e-31,
                                7.88860905221012e-31,
                                7.88860905221012e-31,
                                7.88860905221012e-31,
                                7.88860905221012e-31,
                                7.88860905221012e-31,
                                7.88860905221012e-31,
                                7.88860905221012e-31,
                                7.88860905221012e-31,
                                7.88860905221012e-31,
                                7.88860905221012e-31,
                                7.88860905221012e-31,
                                7.88860905221012e-31,
                                7.88860905221012e-31,
                                7.88860905221012e-31,
                                7.88860905221012e-31,
                                7.88860905221012e-31,
                                7.88860905221012e-31,
                                7.88860905221012e-31,
                                7.88860905221012e-31,
                                7.88860905221012e-31,
                                7.88860905221012e-31,
                            ],
                        ),
                    ],
                ),
            ],
        )
    ]

    writer = MatmlWriter(materials)
    tree = writer._to_etree()
    material_string, metadata_string = get_material_and_metadata_from_xml(tree)
    assert material_string == MULTILINEAR
    assert metadata_string == MULTILINEAR_METADATA


def test_write_variable_mutilinear_isotropic_hadening():
    materials = [
        Material(
            name="SFRP Temp Dependent",
            models=[
                IsotropicHardening(
                    stress=[
                        29.52801806,
                        30.93946596,
                        31.56895322,
                        32.83324607,
                        34.28804632,
                        35.45779394,
                        36.7206105,
                        37.86550163,
                        38.9800331,
                        40.37409873,
                    ],
                    independent_parameters=[
                        IndependentParameter(
                            name="Plastic Strain",
                            values=[
                                0.0,
                                0.000175189,
                                0.000257223,
                                0.00043005,
                                0.000643825,
                                0.000828966,
                                0.00104416,
                                0.001255108,
                                0.001477263,
                                0.00178269,
                            ],
                        ),
                        IndependentParameter(
                            name="Temperature", values=[22, 22, 22, 22, 22, 45, 45, 45, 45, 45]
                        ),
                    ],
                ),
            ],
        )
    ]

    writer = MatmlWriter(materials)
    tree = writer._to_etree()
    material_string, metadata_string = get_material_and_metadata_from_xml(tree)
    assert material_string == MULTILINEAR_VARIABLE
    assert metadata_string == MULTILINEAR_METADATA


def test_write_constant_voce_isotropic_hardening():
    materials = [
        Material(
            name="SFRP",
            models=[
                IsotropicHardeningVoceLaw(
                    initial_yield_stress=[28264641.0],
                    linear_coefficient=[526886855.0],
                    exponential_coefficient=[18328164.0],
                    exponential_saturation_parameter=[406.479025],
                    independent_parameters=[
                        IndependentParameter(name="Temperature", values=[7.88860905221012e-31])
                    ],
                ),
            ],
        )
    ]

    writer = MatmlWriter(materials)
    tree = writer._to_etree()
    material_string, metadata_string = get_material_and_metadata_from_xml(tree)
    assert material_string == VOCE
    assert metadata_string == VOCE_METADATA


def test_read_variable_voce_isotropic_hardening():
    materials = [
        Material(
            name="SFRP Temp Dependent",
            models=[
                IsotropicHardeningVoceLaw(
                    initial_yield_stress=[28264641, 34264641, 39264641],
                    linear_coefficient=[526886855, 670000000, 870000000],
                    exponential_coefficient=[18328164, 15000000, 15347000],
                    exponential_saturation_parameter=[406.479025, 387, 387],
                    independent_parameters=[
                        IndependentParameter(name="Temperature", values=[22, 112.4, 267])
                    ],
                ),
            ],
        )
    ]

    writer = MatmlWriter(materials)
    tree = writer._to_etree()
    material_string, metadata_string = get_material_and_metadata_from_xml(tree)
    assert material_string == VOCE_VARIABLE
    assert metadata_string == VOCE_METADATA
