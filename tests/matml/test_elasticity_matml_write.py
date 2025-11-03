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

from pathlib import Path

from ansys.units import Quantity
from utilities import get_material_and_metadata_from_xml

from ansys.materials.manager._models._common import IndependentParameter, InterpolationOptions
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
from ansys.materials.manager.util.visitors.matml_visitor import MatmlWriter

DIR_PATH = Path(__file__).resolve().parent
ISOTROPIC_ELASTICITY = DIR_PATH.joinpath("..", "data", "matml_isotropic_elasticity.txt")
ISOTROPIC_ELASTICITY_METADATA = DIR_PATH.joinpath(
    "..", "data", "matml_isotropic_elasticity_metadata.txt"
)
ORTHOTROPIC_ELASTICITY = DIR_PATH.joinpath("..", "data", "matml_orthotropic_elasticity.txt")
ORTHOTROPIC_ELASTICITY_METADATA = DIR_PATH.joinpath(
    "..", "data", "matml_orthotropic_elasticity_metadata.txt"
)
ANISOTROPIC_ELASTICITY = DIR_PATH.joinpath("..", "data", "matml_anisotropic_elasticity.txt")
ANISOTROPIC_ELASTICITY_METADATA = DIR_PATH.joinpath(
    "..", "data", "matml_anisotropic_elasticity_metadata.txt"
)
ORTHOTROPIC_ELASTICITY_VARIABLE = DIR_PATH.joinpath(
    "..", "data", "matml_orthotropic_elasticity_variable.txt"
)
ISOTROPIC_ELASTICITY_VARIABLE = DIR_PATH.joinpath(
    "..", "data", "matml_isotropic_elasticity_variable.txt"
)


def test_write_constant_elastic_isotropic_material():
    materials = [
        Material(
            name="Isotropic Test Material",
            models=[
                ElasticityIsotropic(
                    youngs_modulus=Quantity(value=[1000000], units="Pa"),
                    poissons_ratio=Quantity(value=[0.3], unit=""),
                    independent_parameters=[
                        IndependentParameter(
                            name="Temperature",
                            default_value=22.0,
                            upper_limit=1.18329135783152e-30,
                            lower_limit=3.94430452610506e-31,
                            values=Quantity(value=[7.88860905221012e-31], units="C"),
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
    with open(ISOTROPIC_ELASTICITY, "r") as file:
        data = file.read()
        assert data == material_string
    with open(ISOTROPIC_ELASTICITY_METADATA, "r") as file:
        data = file.read()
        assert data == metadata_string


def test_write_constant_elastic_orthotropic_material():
    materials = [
        Material(
            name="Orthotropic Test Material",
            models=[
                ElasticityOrthotropic(
                    youngs_modulus_x=Quantity(value=[1000000], units="Pa"),
                    youngs_modulus_y=Quantity(value=[1500000], units="Pa"),
                    youngs_modulus_z=Quantity(value=[2000000], units="Pa"),
                    shear_modulus_xy=Quantity(value=[1000000], units="Pa"),
                    shear_modulus_yz=Quantity(value=[2000000], units="Pa"),
                    shear_modulus_xz=Quantity(value=[3000000], units="Pa"),
                    poissons_ratio_xy=Quantity(value=[0.2], units=""),
                    poissons_ratio_yz=Quantity(value=[0.3], units=""),
                    poissons_ratio_xz=Quantity(value=[0.4], units=""),
                    independent_parameters=[
                        IndependentParameter(
                            name="Temperature",
                            default_value=22.0,
                            upper_limit=1.18329135783152e-30,
                            lower_limit=3.94430452610506e-31,
                            values=Quantity(value=[7.88860905221012e-31], units="C"),
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
    with open(ORTHOTROPIC_ELASTICITY, "r") as file:
        data = file.read()
        assert data == material_string
    with open(ORTHOTROPIC_ELASTICITY_METADATA, "r") as file:
        data = file.read()
        assert data == metadata_string


def test_write_constant_elastic_anisotropic_material():
    materials = [
        Material(
            name="Anisotropic Test Material",
            models=[
                ElasticityAnisotropic(
                    c_11=Quantity(value=[100000000.0], units="Pa"),
                    c_12=Quantity(value=[1000000.0], units="Pa"),
                    c_13=Quantity(value=[2000000.0], units="Pa"),
                    c_14=Quantity(value=[0.0], units="Pa"),
                    c_15=Quantity(value=[0.0], units="Pa"),
                    c_16=Quantity(value=[0.0], units="Pa"),
                    c_22=Quantity(value=[150000000.0], units="Pa"),
                    c_23=Quantity(value=[3000000.0], units="Pa"),
                    c_24=Quantity(value=[0.0], units="Pa"),
                    c_25=Quantity(value=[0.0], units="Pa"),
                    c_26=Quantity(value=[0.0], units="Pa"),
                    c_33=Quantity(value=[200000000.0], units="Pa"),
                    c_34=Quantity(value=[0.0], units="Pa"),
                    c_35=Quantity(value=[0.0], units="Pa"),
                    c_36=Quantity(value=[0.0], units="Pa"),
                    c_44=Quantity(value=[50000000.0], units="Pa"),
                    c_45=Quantity(value=[0.0], units="Pa"),
                    c_46=Quantity(value=[0.0], units="Pa"),
                    c_55=Quantity(value=[60000000.0], units="Pa"),
                    c_56=Quantity(value=[0.0], units="Pa"),
                    c_66=Quantity(value=[70000000.0], units="Pa"),
                ),
            ],
        )
    ]

    writer = MatmlWriter(materials)
    tree = writer._to_etree()
    material_string, metadata_string = get_material_and_metadata_from_xml(tree)
    with open(ANISOTROPIC_ELASTICITY, "r") as file:
        data = file.read()
        assert data == material_string
    with open(ANISOTROPIC_ELASTICITY_METADATA, "r") as file:
        data = file.read()
        assert data == metadata_string


def test_write_variable_elastic_isotropic_material():
    materials = [
        Material(
            name="Variable Isotropic Test Material",
            models=[
                ElasticityIsotropic(
                    youngs_modulus=Quantity(value=[2000000, 1000000], units="Pa"),
                    poissons_ratio=Quantity(value=[0.35, 0.3], units=""),
                    independent_parameters=[
                        IndependentParameter(
                            name="Temperature",
                            default_value=22.0,
                            upper_limit=1.18329135783152e-30,
                            lower_limit=3.94430452610506e-31,
                            values=Quantity(value=[12.0, 21.0], units="C"),
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
    with open(ISOTROPIC_ELASTICITY_VARIABLE, "r") as file:
        data = file.read()
        assert data == material_string
    with open(ISOTROPIC_ELASTICITY_METADATA, "r") as file:
        data = file.read()
        assert data == metadata_string


def test_write_variable_elastic_orthotropic_material():
    materials = [
        Material(
            name="Variable Orthotropic Test Material",
            models=[
                ElasticityOrthotropic(
                    youngs_modulus_x=Quantity(value=[1000000, 11000000], units="Pa"),
                    youngs_modulus_y=Quantity(value=[1500000, 15100000], units="Pa"),
                    youngs_modulus_z=Quantity(value=[2000000, 21000000], units="Pa"),
                    shear_modulus_xy=Quantity(value=[1000000, 1100000], units="Pa"),
                    shear_modulus_yz=Quantity(value=[2000000, 2100000], units="Pa"),
                    shear_modulus_xz=Quantity(value=[3000000, 3100000], units="Pa"),
                    poissons_ratio_xy=Quantity(value=[0.2, 0.21], units=""),
                    poissons_ratio_yz=Quantity(value=[0.3, 0.31], units=""),
                    poissons_ratio_xz=Quantity(value=[0.4, 0.41], units=""),
                    independent_parameters=[
                        IndependentParameter(
                            name="Temperature",
                            default_value=22.0,
                            upper_limit=1.18329135783152e-30,
                            lower_limit=3.94430452610506e-31,
                            values=Quantity(value=[21.0, 22.0], units="C"),
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
    with open(ORTHOTROPIC_ELASTICITY_VARIABLE, "r") as file:
        data = file.read()
        assert data == material_string
    with open(ORTHOTROPIC_ELASTICITY_METADATA, "r") as file:
        data = file.read()
        assert data == metadata_string
