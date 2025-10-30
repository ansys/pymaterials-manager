from ansys.units import Quantity

from ansys.materials.manager._models._material_models.density import Density
from ansys.materials.manager._models._material_models.elasticity_isotropic import (
    ElasticityIsotropic,
)
from ansys.materials.manager._models._material_models.elasticity_orthotropic import (
    ElasticityOrthotropic,
)
from ansys.materials.manager._models.material import Material
from ansys.materials.manager.util.visitors.fluent_visitor import FluentVisitor
from ansys.materials.manager.util.visitors.lsdyna_visitor import LsDynaVisitor
from ansys.materials.manager.util.visitors.mapdl_visitor import MapdlVisitor
from ansys.materials.manager.util.visitors.matml_visitor import MatmlVisitor

material_1 = Material(
    name="Isotropic Test Material",
    material_id=1,
    models=[
        Density(density=Quantity(value=[3.0], units="kg m^-3")),
        ElasticityIsotropic(
            youngs_modulus=Quantity(value=[1000000], units="Pa"),
            poissons_ratio=Quantity(value=[0.3], units=""),
        ),
    ],
)

material_2 = [
    Material(
        name="Orthotropic Test Material",
        material_id=2,
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
            )
        ],
    )
]

materials = [material_1] + material_2
visitor_matml = MatmlVisitor(materials=materials)
visitor_matml.write("trial.xml", True)
visitor_mapdl = MapdlVisitor(materials=materials)
mapdl = visitor_mapdl.write()
print(mapdl)
visitor_dyna = LsDynaVisitor(materials=materials)
dyna = visitor_dyna.write()
print(dyna)
visitor_fluent = FluentVisitor(materials=materials)
fluent = visitor_fluent.write()
print(fluent)
