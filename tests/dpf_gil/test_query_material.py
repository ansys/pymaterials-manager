from ansys.dpf.core import connect_to_server
from ansys.units import Quantity
import numpy as np
import pytest

from ansys.materials.manager._models._common.independent_parameter import IndependentParameter
from ansys.materials.manager._models._common.interpolation_options import InterpolationOptions
from ansys.materials.manager._models._material_models.elasticity_isotropic import (
    ElasticityIsotropic,
)
from ansys.materials.manager._models.material import Material

pytestmark = pytest.mark.dpf_gil_integration


@pytest.fixture(scope="module")
def dpf_server():
    dpf_server = connect_to_server(ip="127.0.0.1", port="50054")
    yield dpf_server


def test_gil_query_linear_elastic(dpf_server):
    variable_material = Material(
        name="Elastic Material",
        models=[
            ElasticityIsotropic(
                youngs_modulus=Quantity([1000000000.0, 2000000000.0, 4000000000.0], "Pa"),
                poisson_ratio=Quantity([0.3, 0.28, 0.25], ""),
                independent_parameters=[
                    IndependentParameter(
                        name="Volume Fraction", values=Quantity(value=[0.2, 0.3, 0.5], units="")
                    )
                ],
                interpolation_options=InterpolationOptions(
                    algorithm_type="Linear Multivariate",
                    normalized=False,
                    Cached=True,
                ),
            )
        ],
    )
    elasticity = variable_material.get_model_by_name("Elasticity")
    assert elasticity is not None
    results = elasticity.query([0.25, 0.28, 0.4, 0.5])
    expected_results = [
        [1.50e09, 2.90e-01],
        [1.80e09, 2.84e-01],
        [3.00e09, 2.65e-01],
        [4.00e09, 2.50e-01],
    ]
    for i in range(len(results)):
        assert np.isclose(results[i][0], expected_results[i][0], rtol=1e-4)
        assert np.isclose(results[i][1], expected_results[i][1], rtol=1e-4)
