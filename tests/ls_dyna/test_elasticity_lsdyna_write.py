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

from ansys.units import Quantity
import numpy as np

from ansys.materials.manager._models._material_models.density import Density
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
from ansys.materials.manager.util.ls_dyna.writer_ls_dyna import WriterLsDyna


def test_write_constant_elasticity_isotropic():
    elasticity = ElasticityIsotropic(
        youngs_modulus=Quantity(value=[1000000], units="Pa"),
        poissons_ratio=Quantity(value=[0.3], units=""),
    )

    material = Material(name="Linear Elastic", models=[elasticity])

    material_id = 1
    lsdyna_material = WriterLsDyna().write_material(material, material_id)
    assert len(lsdyna_material) == 1
    assert lsdyna_material[0].e == elasticity.youngs_modulus.value[0]
    assert lsdyna_material[0].pr == elasticity.poissons_ratio.value[0]
    assert lsdyna_material[0].mid == material_id


def test_write_constant_elasticity_isotropic_with_density():
    density = Density(
        density=Quantity(value=[1.34], units="kg m^-3"),
    )

    elasticity = ElasticityIsotropic(
        youngs_modulus=Quantity(value=[1000000], units="Pa"),
        poissons_ratio=Quantity(value=[0.3], units=""),
    )

    material = Material(name="Isotropic Elastic", models=[density, elasticity])

    material_id = 2
    lsdyna_material = WriterLsDyna().write_material(material, material_id)
    assert len(lsdyna_material) == 1
    assert lsdyna_material[0].e == elasticity.youngs_modulus.value[0]
    assert lsdyna_material[0].pr == elasticity.poissons_ratio.value[0]
    assert lsdyna_material[0].ro == density.density.value[0]
    assert lsdyna_material[0].mid == material_id


def test_write_constant_elasticity_orthotropic():
    elasticity = ElasticityOrthotropic(
        youngs_modulus_x=Quantity(value=[1000000], units="Pa"),
        youngs_modulus_y=Quantity(value=[2000000], units="Pa"),
        youngs_modulus_z=Quantity(value=[3000000], units="Pa"),
        shear_modulus_xy=Quantity(value=[100000], units="Pa"),
        shear_modulus_yz=Quantity(value=[200000], units="Pa"),
        shear_modulus_xz=Quantity(value=[300000], units="Pa"),
        poissons_ratio_xy=Quantity(value=[0.1], units=""),
        poissons_ratio_yz=Quantity(value=[0.2], units=""),
        poissons_ratio_xz=Quantity(value=[0.3], units=""),
    )

    material = Material(name="Orthotropic Elastic", models=[elasticity])

    material_id = 3
    lsdyna_material = WriterLsDyna().write_material(material, material_id)
    assert len(lsdyna_material) == 1
    assert lsdyna_material[0].ea == elasticity.youngs_modulus_x.value[0]
    assert lsdyna_material[0].eb == elasticity.youngs_modulus_y.value[0]
    assert lsdyna_material[0].ec == elasticity.youngs_modulus_z.value[0]
    assert lsdyna_material[0].gab == elasticity.shear_modulus_xy.value[0]
    assert lsdyna_material[0].gbc == elasticity.shear_modulus_yz.value[0]
    assert lsdyna_material[0].gca == elasticity.shear_modulus_xz.value[0]
    assert lsdyna_material[0].prba == elasticity.poissons_ratio_xy.value[0]
    assert lsdyna_material[0].prcb == elasticity.poissons_ratio_yz.value[0]
    assert lsdyna_material[0].prca == elasticity.poissons_ratio_xz.value[0]
    assert lsdyna_material[0].mid == material_id


def test_write_constant_elasticity_orthotropic_with_density():
    density = Density(
        density=Quantity(value=[1.34], units="kg m^-3"),
    )

    elasticity = ElasticityOrthotropic(
        youngs_modulus_x=Quantity(value=[1000000], units="Pa"),
        youngs_modulus_y=Quantity(value=[2000000], units="Pa"),
        youngs_modulus_z=Quantity(value=[3000000], units="Pa"),
        shear_modulus_xy=Quantity(value=[100000], units="Pa"),
        shear_modulus_yz=Quantity(value=[200000], units="Pa"),
        shear_modulus_xz=Quantity(value=[300000], units="Pa"),
        poissons_ratio_xy=Quantity(value=[0.1], units=""),
        poissons_ratio_yz=Quantity(value=[0.2], units=""),
        poissons_ratio_xz=Quantity(value=[0.3], units=""),
    )

    material = Material(name="Orthotropic Elastic", models=[elasticity, density])

    material_id = 4
    lsdyna_material = WriterLsDyna().write_material(material, material_id)
    assert len(lsdyna_material) == 1
    assert lsdyna_material[0].ro == density.density.value[0]
    assert lsdyna_material[0].ea == elasticity.youngs_modulus_x.value[0]
    assert lsdyna_material[0].eb == elasticity.youngs_modulus_y.value[0]
    assert lsdyna_material[0].ec == elasticity.youngs_modulus_z.value[0]
    assert lsdyna_material[0].gab == elasticity.shear_modulus_xy.value[0]
    assert lsdyna_material[0].gbc == elasticity.shear_modulus_yz.value[0]
    assert lsdyna_material[0].gca == elasticity.shear_modulus_xz.value[0]
    assert lsdyna_material[0].prba == elasticity.poissons_ratio_xy.value[0]
    assert lsdyna_material[0].prcb == elasticity.poissons_ratio_yz.value[0]
    assert lsdyna_material[0].prca == elasticity.poissons_ratio_xz.value[0]
    assert lsdyna_material[0].mid == material_id


def test_write_constant_elasticity_anisotropic():
    elasticity = ElasticityAnisotropic(
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
    )

    material = Material(name="Anisotropic Elastic", models=[elasticity])

    material_id = 5
    lsdyna_material = WriterLsDyna().write_material(material, material_id)
    d = np.column_stack(
        (
            elasticity.column_1.value,
            elasticity.column_2.value,
            elasticity.column_3.value,
            elasticity.column_4.value,
            elasticity.column_5.value,
            elasticity.column_6.value,
        )
    ).tolist()

    lsdyna_material[0].c11 == d[0][0]
    lsdyna_material[0].c12 == d[0][1]
    lsdyna_material[0].c22 == d[1][1]
    lsdyna_material[0].c13 == d[0][2]
    lsdyna_material[0].c23 == d[1][2]
    lsdyna_material[0].c33 == d[2][2]
    lsdyna_material[0].c14 == d[0][3]
    lsdyna_material[0].c24 == d[1][3]
    lsdyna_material[0].c34 == d[2][3]
    lsdyna_material[0].c44 == d[3][3]
    lsdyna_material[0].c15 == d[0][4]
    lsdyna_material[0].c25 == d[1][4]
    lsdyna_material[0].c35 == d[2][4]
    lsdyna_material[0].c45 == d[3][4]
    lsdyna_material[0].c55 == d[4][4]
    lsdyna_material[0].c16 == d[0][5]
    lsdyna_material[0].c26 == d[1][5]
    lsdyna_material[0].c36 == d[2][5]
    lsdyna_material[0].c46 == d[3][5]
    lsdyna_material[0].c56 == d[4][5]
    lsdyna_material[0].c66 == d[5][5]


def test_write_constant_elasticity_anisotropic_with_density():

    density = Density(
        density=Quantity(value=[1.34], units="kg m^-3"),
    )

    elasticity = ElasticityAnisotropic(
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
    )

    material = Material(name="Anisotropic Elastic", models=[elasticity, density])

    material_id = 5
    lsdyna_material = WriterLsDyna().write_material(material, material_id)
    d = np.column_stack(
        (
            elasticity.column_1.value,
            elasticity.column_2.value,
            elasticity.column_3.value,
            elasticity.column_4.value,
            elasticity.column_5.value,
            elasticity.column_6.value,
        )
    ).tolist()
    assert lsdyna_material[0].ro == density.density.value[0]
    assert lsdyna_material[0].c11 == d[0][0]
    assert lsdyna_material[0].c12 == d[0][1]
    assert lsdyna_material[0].c22 == d[1][1]
    assert lsdyna_material[0].c13 == d[0][2]
    assert lsdyna_material[0].c23 == d[1][2]
    assert lsdyna_material[0].c33 == d[2][2]
    assert lsdyna_material[0].c14 == d[0][3]
    assert lsdyna_material[0].c24 == d[1][3]
    assert lsdyna_material[0].c34 == d[2][3]
    assert lsdyna_material[0].c44 == d[3][3]
    assert lsdyna_material[0].c15 == d[0][4]
    assert lsdyna_material[0].c25 == d[1][4]
    assert lsdyna_material[0].c35 == d[2][4]
    assert lsdyna_material[0].c45 == d[3][4]
    assert lsdyna_material[0].c55 == d[4][4]
    assert lsdyna_material[0].c16 == d[0][5]
    assert lsdyna_material[0].c26 == d[1][5]
    assert lsdyna_material[0].c36 == d[2][5]
    assert lsdyna_material[0].c46 == d[3][5]
    assert lsdyna_material[0].c56 == d[4][5]
    assert lsdyna_material[0].c66 == d[5][5]
