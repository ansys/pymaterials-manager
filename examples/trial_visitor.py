from ansys.units import Quantity

from ansys.materials.manager._models._material_models.elasticity_isotropic import (
    ElasticityIsotropic,
)
from ansys.materials.manager._models.material import Material
from ansys.materials.manager.util.visitors.lsdyna_visitor import LsDynaVisitor
from ansys.materials.manager.util.visitors.mapdl_visitor import MapdlVisitor
from ansys.materials.manager.util.visitors.matml_visitor import MatmlVisitor

linear_elastic_material = Material(
    name="Isotropic Test Material",
    models=[
        ElasticityIsotropic(
            youngs_modulus=Quantity(value=[1000000], units="Pa"),
            poissons_ratio=Quantity(value=[0.3], units=""),
        )
    ],
)

visitor_matml = MatmlVisitor(materials=[linear_elastic_material])
visitor_matml.write("trial.xml", True)
visitor_mapdl = MapdlVisitor(materials=[linear_elastic_material])
mapdl = visitor_mapdl.write()
print(mapdl)
visitor_dyna = LsDynaVisitor(materials=[linear_elastic_material])
dyna = visitor_dyna.write()
print(dyna)
