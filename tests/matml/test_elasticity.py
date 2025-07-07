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

from ansys.units import Quantity
from utilities import get_material_and_metadata_from_xml, read_specific_material

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
from ansys.materials.manager.util.matml.matml_from_material import MatmlWriter

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
XML_FILE_PATH = os.path.join(DIR_PATH, "..", "data", "matml_unittest_elasticity.xml")
ISOTROPIC_ELASTICITY = os.path.join(DIR_PATH, "..", "data", "matml_isotropic_elasticity.txt")
ISOTROPIC_ELASTICITY_METADATA = os.path.join(
    DIR_PATH, "..", "data", "matml_isotropic_elasticity_metadata.txt"
)
ORTHOTROPIC_ELASTICITY = os.path.join(DIR_PATH, "..", "data", "matml_orthotropic_elasticity.txt")
ORTHOTROPIC_ELASTICITY_METADATA = os.path.join(
    DIR_PATH, "..", "data", "matml_orthotropic_elasticity_metadata.txt"
)
ANISOTROPIC_ELASTICITY = os.path.join(DIR_PATH, "..", "data", "matml_anisotropic_elasticity.txt")
ANISOTROPIC_ELASTICITY_METADATA = os.path.join(
    DIR_PATH, "..", "data", "matml_anisotropic_elasticity_metadata.txt"
)
ORTHOTROPIC_ELASTICITY_VARIABLE = os.path.join(
    DIR_PATH, "..", "data", "matml_orthotropic_elasticity_variable.txt"
)
ISOTROPIC_ELASTICITY_VARIABLE = os.path.join(
    DIR_PATH, "..", "data", "matml_isotropic_elasticity_variable.txt"
)


def test_read_constant_elastic_isotropic_material():
    material = read_specific_material(XML_FILE_PATH, "Isotropic Test Material")
    assert len(material.models) == 2
    isotropic_elasticity = material.models[1]
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
    assert isotropic_elasticity.independent_parameters[0].values.value == [7.88860905221012e-31]
    assert isotropic_elasticity.independent_parameters[0].values.unit == "C"
    assert isotropic_elasticity.independent_parameters[0].field_units == "C"
    assert isotropic_elasticity.independent_parameters[0].upper_limit == 1.18329135783152e-30
    assert isotropic_elasticity.independent_parameters[0].lower_limit == 3.94430452610506e-31
    assert isotropic_elasticity.independent_parameters[0].default_value == 22.0
    assert isotropic_elasticity.youngs_modulus.value == [1000000.0]
    assert isotropic_elasticity.youngs_modulus.unit == "Pa"
    assert isotropic_elasticity.poissons_ratio.value == [0.3]
    assert isotropic_elasticity.poissons_ratio.unit == ""


def test_read_constant_elastic_orthotropic_material():
    material = read_specific_material(XML_FILE_PATH, "Orthotropic Test Material")
    assert len(material.models) == 2
    orthotropic_elasticity = material.models[1]
    assert orthotropic_elasticity.name == "Elasticity"
    assert orthotropic_elasticity.model_qualifiers[0].name == "Behavior"
    assert orthotropic_elasticity.model_qualifiers[0].value == "Orthotropic"
    assert orthotropic_elasticity.model_qualifiers[1].name == "Field Variable Compatible"
    assert orthotropic_elasticity.model_qualifiers[1].value == "Temperature"
    assert orthotropic_elasticity.interpolation_options.algorithm_type == "Linear Multivariate"
    assert orthotropic_elasticity.interpolation_options.cached == True
    assert orthotropic_elasticity.interpolation_options.normalized == True
    assert orthotropic_elasticity.youngs_modulus_x.value == [10000000.0]
    assert orthotropic_elasticity.youngs_modulus_x.unit == "Pa"
    assert orthotropic_elasticity.youngs_modulus_y.value == [15000000.0]
    assert orthotropic_elasticity.youngs_modulus_y.unit == "Pa"
    assert orthotropic_elasticity.youngs_modulus_z.value == [20000000.0]
    assert orthotropic_elasticity.youngs_modulus_z.unit == "Pa"
    assert orthotropic_elasticity.poissons_ratio_xy.value == [0.2]
    assert orthotropic_elasticity.poissons_ratio_xy.unit == ""
    assert orthotropic_elasticity.poissons_ratio_yz.value == [0.3]
    assert orthotropic_elasticity.poissons_ratio_yz.unit == ""
    assert orthotropic_elasticity.poissons_ratio_xz.value == [0.4]
    assert orthotropic_elasticity.poissons_ratio_xz.unit == ""
    assert orthotropic_elasticity.shear_modulus_xy.value == [1000000.0]
    assert orthotropic_elasticity.shear_modulus_xy.unit == "Pa"
    assert orthotropic_elasticity.shear_modulus_yz.value == [2000000.0]
    assert orthotropic_elasticity.shear_modulus_yz.unit == "Pa"
    assert orthotropic_elasticity.shear_modulus_xz.value == [3000000.0]
    assert orthotropic_elasticity.shear_modulus_xz.unit == "Pa"
    assert orthotropic_elasticity.independent_parameters[0].name == "Temperature"
    assert orthotropic_elasticity.independent_parameters[0].values.value == [7.88860905221012e-31]
    assert orthotropic_elasticity.independent_parameters[0].values.unit == "C"
    assert orthotropic_elasticity.independent_parameters[0].field_variable == "Temperature"
    assert orthotropic_elasticity.independent_parameters[0].field_units == "C"
    assert orthotropic_elasticity.independent_parameters[0].upper_limit == 1.18329135783152e-30
    assert orthotropic_elasticity.independent_parameters[0].lower_limit == 3.94430452610506e-31
    assert orthotropic_elasticity.independent_parameters[0].default_value == 22.0


def test_read_constant_elastic_anisotropic_material():
    material = read_specific_material(XML_FILE_PATH, "Anisotropic Test Material")
    assert len(material.models) == 2
    anisotropic_elasticity = material.models[1]
    assert anisotropic_elasticity.name == "Elasticity"
    assert anisotropic_elasticity.model_qualifiers[0].name == "Behavior"
    assert anisotropic_elasticity.model_qualifiers[0].value == "Anisotropic"
    assert anisotropic_elasticity.column_1.value.tolist() == [
        100000000,
        1000000,
        2000000,
        3000000,
        4000000,
        5000000,
    ]
    assert anisotropic_elasticity.column_1.unit == "Pa"
    assert anisotropic_elasticity.column_2.value.tolist() == [
        7.88860905221012e-31,
        150000000,
        6000000,
        7000000,
        8000000,
        9000000,
    ]
    assert anisotropic_elasticity.column_2.unit == "Pa"
    assert anisotropic_elasticity.column_3.value.tolist() == [
        7.88860905221012e-31,
        7.88860905221012e-31,
        200000000,
        10000000,
        11000000,
        12000000,
    ]
    assert anisotropic_elasticity.column_3.unit == "Pa"
    assert anisotropic_elasticity.column_4.value.tolist() == [
        7.88860905221012e-31,
        7.88860905221012e-31,
        7.88860905221012e-31,
        50000000,
        13000000,
        14000000,
    ]
    assert anisotropic_elasticity.column_4.unit == "Pa"
    assert anisotropic_elasticity.column_5.value.tolist() == [
        7.88860905221012e-31,
        7.88860905221012e-31,
        7.88860905221012e-31,
        7.88860905221012e-31,
        60000000,
        15000000,
    ]
    assert anisotropic_elasticity.column_5.unit == "Pa"
    assert anisotropic_elasticity.column_6.value.tolist() == [
        7.88860905221012e-31,
        7.88860905221012e-31,
        7.88860905221012e-31,
        7.88860905221012e-31,
        7.88860905221012e-31,
        70000000,
    ]
    assert anisotropic_elasticity.column_6.unit == "Pa"


def test_read_variable_elastic_isotropic_material():
    material = read_specific_material(XML_FILE_PATH, "Variable Isotropic Test Material")
    assert len(material.models) == 2
    isotropic_elasticity = material.models[1]
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
    assert isotropic_elasticity.independent_parameters[0].values.value.tolist() == [12, 21]
    assert isotropic_elasticity.independent_parameters[0].values.unit == "C"
    assert isotropic_elasticity.independent_parameters[0].field_variable == "Temperature"
    assert isotropic_elasticity.independent_parameters[0].field_units == "C"
    assert isotropic_elasticity.independent_parameters[0].upper_limit == 1.18329135783152e-30
    assert isotropic_elasticity.independent_parameters[0].lower_limit == 3.94430452610506e-31
    assert isotropic_elasticity.independent_parameters[0].default_value == 22.0
    assert isotropic_elasticity.youngs_modulus.value.tolist() == [2000000, 1000000]
    assert isotropic_elasticity.youngs_modulus.unit == "Pa"
    assert isotropic_elasticity.poissons_ratio.value.tolist() == [0.35, 0.3]
    assert isotropic_elasticity.poissons_ratio.unit == ""


def test_read_variable_elastic_orthotropic_material():
    material = read_specific_material(XML_FILE_PATH, "Variable Orthotropic Test Material")
    assert len(material.models) == 2
    orthotropic_elasticity = material.models[1]
    assert orthotropic_elasticity.name == "Elasticity"
    assert orthotropic_elasticity.model_qualifiers[0].name == "Behavior"
    assert orthotropic_elasticity.model_qualifiers[0].value == "Orthotropic"
    assert orthotropic_elasticity.model_qualifiers[1].name == "Field Variable Compatible"
    assert orthotropic_elasticity.model_qualifiers[1].value == "Temperature"
    assert orthotropic_elasticity.interpolation_options.algorithm_type == "Linear Multivariate"
    assert orthotropic_elasticity.interpolation_options.cached == True
    assert orthotropic_elasticity.interpolation_options.normalized == True
    assert orthotropic_elasticity.youngs_modulus_x.value.tolist() == [10000000.0, 11000000.0]
    assert orthotropic_elasticity.youngs_modulus_x.unit == "Pa"
    assert orthotropic_elasticity.youngs_modulus_y.value.tolist() == [15000000.0, 15100000]
    assert orthotropic_elasticity.youngs_modulus_y.unit == "Pa"
    assert orthotropic_elasticity.youngs_modulus_z.value.tolist() == [20000000.0, 21000000]
    assert orthotropic_elasticity.youngs_modulus_z.unit == "Pa"
    assert orthotropic_elasticity.poissons_ratio_xy.value.tolist() == [0.2, 0.21]
    assert orthotropic_elasticity.poissons_ratio_xy.unit == ""
    assert orthotropic_elasticity.poissons_ratio_yz.value.tolist() == [0.3, 0.31]
    assert orthotropic_elasticity.poissons_ratio_yz.unit == ""
    assert orthotropic_elasticity.poissons_ratio_xz.value.tolist() == [0.4, 0.41]
    assert orthotropic_elasticity.poissons_ratio_xz.unit == ""
    assert orthotropic_elasticity.shear_modulus_xy.value.tolist() == [1000000.0, 1100000]
    assert orthotropic_elasticity.shear_modulus_xy.unit == "Pa"
    assert orthotropic_elasticity.shear_modulus_yz.value.tolist() == [2000000.0, 2100000]
    assert orthotropic_elasticity.shear_modulus_yz.unit == "Pa"
    assert orthotropic_elasticity.shear_modulus_xz.value.tolist() == [3000000.0, 3100000]
    assert orthotropic_elasticity.shear_modulus_xz.unit == "Pa"
    assert orthotropic_elasticity.independent_parameters[0].name == "Temperature"
    assert orthotropic_elasticity.independent_parameters[0].values.value.tolist() == [21, 22]
    assert orthotropic_elasticity.independent_parameters[0].values.unit == "C"
    assert orthotropic_elasticity.independent_parameters[0].field_variable == "Temperature"
    assert orthotropic_elasticity.independent_parameters[0].field_units == "C"
    assert orthotropic_elasticity.independent_parameters[0].upper_limit == 1.18329135783152e-30
    assert orthotropic_elasticity.independent_parameters[0].lower_limit == 3.94430452610506e-31
    assert orthotropic_elasticity.independent_parameters[0].default_value == 22.0


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
                            field_variable="Temperarture",
                            field_units="C",
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
                    poissons_ratio_xy=Quantity(value=[0.2], units=""),
                    poissons_ratio_yz=Quantity(value=[0.3], units=""),
                    poissons_ratio_xz=Quantity(value=[0.4], units=""),
                    shear_modulus_xy=Quantity(value=[1000000], units="Pa"),
                    shear_modulus_yz=Quantity(value=[2000000], units="Pa"),
                    shear_modulus_xz=Quantity(value=[3000000], units="Pa"),
                    independent_parameters=[
                        IndependentParameter(
                            name="Temperature",
                            default_value=22.0,
                            upper_limit=1.18329135783152e-30,
                            lower_limit=3.94430452610506e-31,
                            values=Quantity(value=[7.88860905221012e-31], units="C"),
                            field_variable="Temperature",
                            field_units="C",
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
                    column_1=Quantity(
                        value=[100000000, 1000000, 2000000, 3000000, 4000000, 5000000], units="Pa"
                    ),
                    column_2=Quantity(
                        value=[7.88860905221012e-31, 150000000, 6000000, 7000000, 8000000, 9000000],
                        units="Pa",
                    ),
                    column_3=Quantity(
                        value=[
                            7.88860905221012e-31,
                            7.88860905221012e-31,
                            200000000,
                            10000000,
                            11000000,
                            12000000,
                        ],
                        units="Pa",
                    ),
                    column_4=Quantity(
                        value=[
                            7.88860905221012e-31,
                            7.88860905221012e-31,
                            7.88860905221012e-31,
                            50000000,
                            13000000,
                            14000000,
                        ],
                        units="Pa",
                    ),
                    column_5=Quantity(
                        value=[
                            7.88860905221012e-31,
                            7.88860905221012e-31,
                            7.88860905221012e-31,
                            7.88860905221012e-31,
                            60000000,
                            15000000,
                        ],
                        units="Pa",
                    ),
                    column_6=Quantity(
                        value=[
                            7.88860905221012e-31,
                            7.88860905221012e-31,
                            7.88860905221012e-31,
                            7.88860905221012e-31,
                            7.88860905221012e-31,
                            70000000,
                        ],
                        units="Pa",
                    ),
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
                            field_variable="Temperarture",
                            field_units="C",
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
                    poissons_ratio_xy=Quantity(value=[0.2, 0.21], units=""),
                    poissons_ratio_yz=Quantity(value=[0.3, 0.31], units=""),
                    poissons_ratio_xz=Quantity(value=[0.4, 0.41], units=""),
                    shear_modulus_xy=Quantity(value=[1000000, 1100000], units="Pa"),
                    shear_modulus_yz=Quantity(value=[2000000, 2100000], units="Pa"),
                    shear_modulus_xz=Quantity(value=[3000000, 3100000], units="Pa"),
                    independent_parameters=[
                        IndependentParameter(
                            name="Temperature",
                            default_value=22.0,
                            upper_limit=1.18329135783152e-30,
                            lower_limit=3.94430452610506e-31,
                            values=Quantity(value=[21.0, 22.0], units="C"),
                            field_variable="Temperarture",
                            field_units="C",
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
