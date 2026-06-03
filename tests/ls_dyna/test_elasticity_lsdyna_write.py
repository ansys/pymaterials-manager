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

from ansys.units import Quantity

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
from ansys.materials.manager.parsers.lsdyna.lsdyna_writer import LsDynaWriter


def test_constant_elasticity_isotropic_write():
    elasticity = ElasticityIsotropic(
        youngs_modulus=Quantity(value=[1000000], units="Pa"),
        poissons_ratio=Quantity(value=[0.3], units=""),
    )
    material_id = 1
    material = Material(name="Linear Elastic", material_id=material_id, models=[elasticity])
    lsdyna_writer = LsDynaWriter([material])
    lsdyna_material = lsdyna_writer.write()
    assert len(lsdyna_material) == 1
    assert lsdyna_material[0].e == elasticity.youngs_modulus.value[0]
    assert lsdyna_material[0].pr == elasticity.poissons_ratio.value[0]
    assert lsdyna_material[0].mid == material_id


def test_constant_elasticity_isotropic_with_density_write():
    density = Density(
        density=Quantity(value=[1.34], units="kg m^-3"),
    )

    elasticity = ElasticityIsotropic(
        youngs_modulus=Quantity(value=[1000000], units="Pa"),
        poissons_ratio=Quantity(value=[0.3], units=""),
    )
    material_id = 2
    material = Material(
        name="Isotropic Elastic", material_id=material_id, models=[density, elasticity]
    )

    lsdyna_writer = LsDynaWriter([material])
    lsdyna_material = lsdyna_writer.write()
    assert len(lsdyna_material) == 1
    assert lsdyna_material[0].e == elasticity.youngs_modulus.value[0]
    assert lsdyna_material[0].pr == elasticity.poissons_ratio.value[0]
    assert lsdyna_material[0].ro == density.density.value[0]
    assert lsdyna_material[0].mid == material_id


def test_constant_elasticity_orthotropic_write():
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
    material_id = 3
    material = Material(name="Orthotropic Elastic", material_id=material_id, models=[elasticity])
    lsdyna_writer = LsDynaWriter([material])
    lsdyna_material = lsdyna_writer.write()
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


def test_constant_elasticity_orthotropic_with_density_write():
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
    material_id = 4
    material = Material(
        name="Orthotropic Elastic", material_id=material_id, models=[elasticity, density]
    )
    lsdyna_writer = LsDynaWriter([material])
    lsdyna_material = lsdyna_writer.write()
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


def test_constant_elasticity_anisotropic_write():
    elasticity = ElasticityAnisotropic(
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
    )
    material_id = 5
    material = Material(
        name="Material 1",
        material_id=material_id,
        models=[elasticity],
    )

    lsdyna_writer = LsDynaWriter([material])
    lsdyna_material = lsdyna_writer.write()
    assert len(lsdyna_material) == 1
    assert lsdyna_material[0].c11 == elasticity.c_11.value[0]
    assert lsdyna_material[0].c12 == elasticity.c_12.value[0]
    assert lsdyna_material[0].c22 == elasticity.c_22.value[0]
    assert lsdyna_material[0].c13 == elasticity.c_13.value[0]
    assert lsdyna_material[0].c23 == elasticity.c_23.value[0]
    assert lsdyna_material[0].c33 == elasticity.c_33.value[0]
    assert lsdyna_material[0].c14 == elasticity.c_14.value[0]
    assert lsdyna_material[0].c24 == elasticity.c_24.value[0]
    assert lsdyna_material[0].c34 == elasticity.c_34.value[0]
    assert lsdyna_material[0].c44 == elasticity.c_44.value[0]
    assert lsdyna_material[0].c15 == elasticity.c_15.value[0]
    assert lsdyna_material[0].c25 == elasticity.c_25.value[0]
    assert lsdyna_material[0].c35 == elasticity.c_35.value[0]
    assert lsdyna_material[0].c45 == elasticity.c_45.value[0]
    assert lsdyna_material[0].c55 == elasticity.c_55.value[0]
    assert lsdyna_material[0].c16 == elasticity.c_16.value[0]
    assert lsdyna_material[0].c26 == elasticity.c_26.value[0]
    assert lsdyna_material[0].c36 == elasticity.c_36.value[0]
    assert lsdyna_material[0].c46 == elasticity.c_46.value[0]
    assert lsdyna_material[0].c56 == elasticity.c_56.value[0]
    assert lsdyna_material[0].c66 == elasticity.c_66.value[0]


def test_constant_elasticity_anisotropic_with_density_write():

    density = Density(
        density=Quantity(value=[1.34], units="kg m^-3"),
    )

    elasticity = ElasticityAnisotropic(
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
    )
    material_id = 5
    material = Material(
        name="Material 1",
        material_id=material_id,
        models=[density, elasticity],
    )

    lsdyna_writer = LsDynaWriter([material])
    lsdyna_material = lsdyna_writer.write()
    assert len(lsdyna_material) == 1

    assert lsdyna_material[0].c11 == elasticity.c_11.value[0]
    assert lsdyna_material[0].c12 == elasticity.c_12.value[0]
    assert lsdyna_material[0].c22 == elasticity.c_22.value[0]
    assert lsdyna_material[0].c13 == elasticity.c_13.value[0]
    assert lsdyna_material[0].c23 == elasticity.c_23.value[0]
    assert lsdyna_material[0].c33 == elasticity.c_33.value[0]
    assert lsdyna_material[0].c14 == elasticity.c_14.value[0]
    assert lsdyna_material[0].c24 == elasticity.c_24.value[0]
    assert lsdyna_material[0].c34 == elasticity.c_34.value[0]
    assert lsdyna_material[0].c44 == elasticity.c_44.value[0]
    assert lsdyna_material[0].c15 == elasticity.c_15.value[0]
    assert lsdyna_material[0].c25 == elasticity.c_25.value[0]
    assert lsdyna_material[0].c35 == elasticity.c_35.value[0]
    assert lsdyna_material[0].c45 == elasticity.c_45.value[0]
    assert lsdyna_material[0].c55 == elasticity.c_55.value[0]
    assert lsdyna_material[0].c16 == elasticity.c_16.value[0]
    assert lsdyna_material[0].c26 == elasticity.c_26.value[0]
    assert lsdyna_material[0].c36 == elasticity.c_36.value[0]
    assert lsdyna_material[0].c46 == elasticity.c_46.value[0]
    assert lsdyna_material[0].c56 == elasticity.c_56.value[0]
    assert lsdyna_material[0].c66 == elasticity.c_66.value[0]
    assert lsdyna_material[0].ro == density.density.value[0]
