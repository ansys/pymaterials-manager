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

from ansys.materials.manager._models._material_models.density import Density
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
