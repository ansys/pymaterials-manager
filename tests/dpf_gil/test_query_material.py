# Copyright (C) 2022 - 2026 ANSYS, Inc. and/or its affiliates.
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

from ansys.dpf.core import connect_to_server
from ansys.dpf.core.server_factory import CommunicationProtocols, GrpcMode, ServerConfig
from ansys.units import Quantity
import numpy as np
import pytest

from ansys.materials.manager._models._common.independent_parameter import IndependentParameter
from ansys.materials.manager._models._common.interpolation_options import InterpolationOptions
from ansys.materials.manager._models._material_models.elasticity_isotropic import (
    ElasticityIsotropic,
)
from ansys.materials.manager._models._material_models.stress_limits_orthotropic import (
    StressLimitsOrthotropic,
)
from ansys.materials.manager._models.material import Material

pytestmark = pytest.mark.dpf_gil_integration


@pytest.fixture(scope="module")
def dpf_server():
    dpf_server = connect_to_server(
        ip="127.0.0.1",
        port="50054",
        as_global=True,
        config=ServerConfig(protocol=CommunicationProtocols.gRPC, grpc_mode=GrpcMode.Insecure),
    )
    yield dpf_server


def test_gil_query_linear_elastic(dpf_server):
    variable_material = Material(
        name="Elastic Material",
        models=[
            ElasticityIsotropic(
                youngs_modulus=Quantity([1000000000.0, 2000000000.0, 4000000000.0], "Pa"),
                poissons_ratio=Quantity([0.3, 0.28, 0.25], ""),
                independent_parameters=[
                    IndependentParameter(
                        name="Volume Fraction", values=Quantity(value=[0.2, 0.3, 0.5], units="")
                    )
                ],
                interpolation_options=InterpolationOptions(
                    algorithm_type="Linear Multivariate",
                    normalized=False,
                    cached=True,
                ),
            )
        ],
    )
    elasticity = variable_material.get_model_by_name("Elasticity")
    assert elasticity is not None
    results = elasticity.query([0.25, 0.28, 0.4, 0.5], dpf_server=dpf_server)
    expected_results = [
        [1.50e09, 2.90e-01],
        [1.80e09, 2.84e-01],
        [3.00e09, 2.65e-01],
        [4.00e09, 2.50e-01],
    ]
    for i in range(len(results)):
        assert np.isclose(results[i][0], expected_results[i][0], rtol=1e-4)
        assert np.isclose(results[i][1], expected_results[i][1], rtol=1e-4)


def test_gil_query_md_stress_limits(dpf_server):
    variable_material = Material(
        name="Stress Limits Material",
        models=[
            StressLimitsOrthotropic(
                tensile_x_direction=Quantity(
                    value=[
                        104.41558825,
                        110.09023848,
                        110.09023848,
                        94.64803438,
                        116.42324362,
                        116.42324362,
                        87.01743783,
                        123.54698066,
                        123.54698066,
                        81.86506326,
                        131.63356576,
                        94.64803438,
                        94.64803438,
                        140.9114338,
                        99.2956553,
                        140.9114338,
                        99.2956553,
                        87.01743783,
                        87.01743783,
                        151.69115942,
                        104.41558825,
                        151.69115942,
                        104.41558825,
                        81.86506326,
                        81.86506326,
                        179.68900353,
                        87.01743783,
                        87.01743783,
                        196.38148742,
                        90.40630247,
                        196.38148742,
                        90.40630247,
                        81.86506326,
                        81.86506326,
                        281.7365426,
                        81.86506326,
                        81.86506326,
                    ],
                    units="MPa",
                ),
                tensile_y_direction=Quantity(
                    value=[
                        104.41558825,
                        110.09023848,
                        94.64803438,
                        110.09023848,
                        116.42324362,
                        87.01743783,
                        116.42324362,
                        123.54698066,
                        81.86506326,
                        123.54698066,
                        94.64803438,
                        131.63356576,
                        94.64803438,
                        99.2956553,
                        140.9114338,
                        87.01743783,
                        87.01743783,
                        140.9114338,
                        99.2956553,
                        104.41558825,
                        151.69115942,
                        81.86506326,
                        81.86506326,
                        151.69115942,
                        104.41558825,
                        87.01743783,
                        179.68900353,
                        87.01743783,
                        90.40630247,
                        196.38148742,
                        81.86506326,
                        81.86506326,
                        196.38148742,
                        90.40630247,
                        81.86506326,
                        281.7365426,
                        81.86506326,
                    ],
                    units="MPa",
                ),
                tensile_z_direction=Quantity(
                    value=[
                        104.41558826,
                        94.64803438,
                        110.09023848,
                        110.09023848,
                        87.01743784,
                        116.42324364,
                        116.42324364,
                        81.86506326,
                        123.54698066,
                        123.54698066,
                        94.64803438,
                        94.64803438,
                        131.63356576,
                        87.01743783,
                        87.01743783,
                        99.2956553,
                        140.9114338,
                        99.2956553,
                        140.9114338,
                        81.86506326,
                        81.86506326,
                        104.41558825,
                        151.69115942,
                        104.41558825,
                        151.69115942,
                        87.01743783,
                        87.01743783,
                        179.68900353,
                        81.86506326,
                        81.86506326,
                        90.40630247,
                        196.38148742,
                        90.40630247,
                        196.38148742,
                        81.86506326,
                        81.86506326,
                        281.7365426,
                    ],
                    units="MPa",
                ),
                compressive_x_direction=Quantity(
                    value=[
                        104.41558825,
                        110.09023848,
                        110.09023848,
                        94.64803438,
                        116.42324362,
                        116.42324362,
                        87.01743783,
                        123.54698066,
                        123.54698066,
                        81.86506326,
                        131.63356576,
                        94.64803438,
                        94.64803438,
                        140.9114338,
                        99.2956553,
                        140.9114338,
                        99.2956553,
                        87.01743783,
                        87.01743783,
                        151.69115942,
                        104.41558825,
                        151.69115942,
                        104.41558825,
                        81.86506326,
                        81.86506326,
                        179.68900353,
                        87.01743783,
                        87.01743783,
                        196.38148742,
                        90.40630247,
                        196.38148742,
                        90.40630247,
                        81.86506326,
                        81.86506326,
                        281.7365426,
                        81.86506326,
                        81.86506326,
                    ],
                    units="MPa",
                ),
                compressive_y_direction=Quantity(
                    value=[
                        104.41558825,
                        110.09023848,
                        94.64803438,
                        110.09023848,
                        116.42324362,
                        87.01743783,
                        116.42324362,
                        123.54698066,
                        81.86506326,
                        123.54698066,
                        94.64803438,
                        131.63356576,
                        94.64803438,
                        99.2956553,
                        140.9114338,
                        87.01743783,
                        87.01743783,
                        140.9114338,
                        99.2956553,
                        104.41558825,
                        151.69115942,
                        81.86506326,
                        81.86506326,
                        151.69115942,
                        104.41558825,
                        87.01743783,
                        179.68900353,
                        87.01743783,
                        90.40630247,
                        196.38148742,
                        81.86506326,
                        81.86506326,
                        196.38148742,
                        90.40630247,
                        81.86506326,
                        281.7365426,
                        81.86506326,
                    ],
                    units="MPa",
                ),
                compressive_z_direction=Quantity(
                    value=[
                        104.41558826,
                        94.64803438,
                        110.09023848,
                        110.09023848,
                        87.01743784,
                        116.42324364,
                        116.42324364,
                        81.86506326,
                        123.54698066,
                        123.54698066,
                        94.64803438,
                        94.64803438,
                        131.63356576,
                        87.01743783,
                        87.01743783,
                        99.2956553,
                        140.9114338,
                        99.2956553,
                        140.9114338,
                        81.86506326,
                        81.86506326,
                        104.41558825,
                        151.69115942,
                        104.41558825,
                        151.69115942,
                        87.01743783,
                        87.01743783,
                        179.68900353,
                        81.86506326,
                        81.86506326,
                        90.40630247,
                        196.38148742,
                        90.40630247,
                        196.38148742,
                        81.86506326,
                        81.86506326,
                        281.7365426,
                    ],
                    units="MPa",
                ),
                shear_xy=Quantity(
                    value=[
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                    ],
                    units="MPa",
                ),
                shear_yz=Quantity(
                    value=[
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                    ],
                    units="MPa",
                ),
                shear_xz=Quantity(
                    value=[
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                        61.24119871,
                    ],
                    units="MPa",
                ),
                independent_parameters=[
                    IndependentParameter(
                        name="Orientation Tensor A11",
                        values=Quantity(
                            value=[
                                0.33333333,
                                0.38888889,
                                0.38888889,
                                0.22222222,
                                0.44444444,
                                0.44444444,
                                0.11111111,
                                0.5,
                                0.5,
                                0.0,
                                0.55555556,
                                0.22222222,
                                0.22222222,
                                0.61111111,
                                0.27777778,
                                0.61111111,
                                0.27777778,
                                0.11111111,
                                0.11111111,
                                0.66666667,
                                0.33333333,
                                0.66666667,
                                0.33333333,
                                -0.0,
                                -0.0,
                                0.77777778,
                                0.11111111,
                                0.11111111,
                                0.83333333,
                                0.16666667,
                                0.83333333,
                                0.16666667,
                                0.0,
                                0.0,
                                1.0,
                                0.0,
                                0.0,
                            ],
                            units="",
                        ),
                    ),
                    IndependentParameter(
                        name="Orientation Tensor A22",
                        values=Quantity(
                            value=[
                                0.33333333,
                                0.38888889,
                                0.22222222,
                                0.38888889,
                                0.44444444,
                                0.11111111,
                                0.44444444,
                                0.5,
                                0.0,
                                0.5,
                                0.22222222,
                                0.55555556,
                                0.22222222,
                                0.27777778,
                                0.61111111,
                                0.11111111,
                                0.11111111,
                                0.61111111,
                                0.27777778,
                                0.33333333,
                                0.66666667,
                                -0.0,
                                -0.0,
                                0.66666667,
                                0.33333333,
                                0.11111111,
                                0.77777778,
                                0.11111111,
                                0.16666667,
                                0.83333333,
                                0.0,
                                0.0,
                                0.83333333,
                                0.16666667,
                                0.0,
                                1.0,
                                0.0,
                            ],
                            units="",
                        ),
                    ),
                    IndependentParameter(
                        name="Temperature",
                        values=Quantity(
                            value=[
                                22.0,
                                22.0,
                                22.0,
                                22.0,
                                22.0,
                                22.0,
                                22.0,
                                22.0,
                                22.0,
                                22.0,
                                22.0,
                                22.0,
                                22.0,
                                22.0,
                                22.0,
                                22.0,
                                22.0,
                                22.0,
                                22.0,
                                22.0,
                                22.0,
                                22.0,
                                22.0,
                                22.0,
                                22.0,
                                22.0,
                                22.0,
                                22.0,
                                22.0,
                                22.0,
                                22.0,
                                22.0,
                                22.0,
                                22.0,
                                22.0,
                                22.0,
                                22.0,
                            ],
                            units="C",
                        ),
                    ),
                ],
                interpolation_options=InterpolationOptions(
                    algorithm_type="Linear Multivariate",
                    normalized=False,
                    cached=True,
                ),
            )
        ],
    )
    stress_limits = variable_material.get_model_by_name("Stress Limits")
    assert stress_limits is not None
    stress_results = stress_limits.query([[0.79, 0.14, 22.0]], dpf_server=dpf_server)
    expected_stress_results = [
        [
            183.6307060239161,
            88.97178202705851,
            85.11105927155995,
            183.6307060239161,
            88.97178202705851,
            85.11105927155995,
            61.24119870999999,
            61.24119870999999,
            61.24119870999999,
        ]
    ]
    for i in range(len(stress_results[0])):
        assert np.isclose(stress_results[0][i], expected_stress_results[0][i], rtol=1e-4)


def test_gil_import_error():
    variable_material = Material(
        name="Elastic Material",
        models=[
            ElasticityIsotropic(
                youngs_modulus=Quantity([1000000000.0, 2000000000.0, 4000000000.0], "Pa"),
                poissons_ratio=Quantity([0.3, 0.28, 0.25], ""),
                independent_parameters=[
                    IndependentParameter(
                        name="Volume Fraction", values=Quantity(value=[0.2, 0.3, 0.5], units="")
                    )
                ],
                interpolation_options=InterpolationOptions(
                    algorithm_type="Linear Multivariate",
                    normalized=False,
                    cached=True,
                ),
            )
        ],
    )
    elasticity = variable_material.get_model_by_name("Elasticity")
    assert elasticity is not None
    with pytest.raises(
        RuntimeError,
        match="'_query_with_gil' requires Ansys 2027 R1 (v271) or later. Please update your Ansys installation.",  # noqa: E501
    ):
        elasticity.query([0.25, 0.28, 0.4, 0.5])


def test_gil_no_interpolation_options(dpf_server):
    variable_material = Material(
        name="Elastic Material",
        models=[
            ElasticityIsotropic(
                youngs_modulus=Quantity([1000000000.0, 2000000000.0, 4000000000.0], "Pa"),
                poissons_ratio=Quantity([0.3, 0.28, 0.25], ""),
                independent_parameters=[
                    IndependentParameter(
                        name="Volume Fraction", values=Quantity(value=[0.2, 0.3, 0.5], units="")
                    )
                ],
            )
        ],
    )
    elasticity = variable_material.get_model_by_name("Elasticity")
    assert elasticity is not None
    with pytest.raises(
        ValueError, match="Querying a material model with no interpolation options."
    ):
        elasticity.query([0.25, 0.28, 0.4, 0.5], dpf_server=dpf_server)

