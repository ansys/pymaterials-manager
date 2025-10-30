from ansys.units import Quantity

from ansys.materials.manager._models._material_models.density import Density
from ansys.materials.manager._models._material_models.elasticity_isotropic import (
    ElasticityIsotropic,
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

visitor_matml = MatmlVisitor(materials=[material_1])
visitor_matml.write("trial.xml", True)
visitor_mapdl = MapdlVisitor(materials=[material_1])
mapdl = visitor_mapdl.write()
print(mapdl)
visitor_dyna = LsDynaVisitor(materials=[material_1])
dyna = visitor_dyna.write()
print(dyna)
visitor_fluent = FluentVisitor(materials=[material_1])
fluent = visitor_fluent.write()
print(fluent)
