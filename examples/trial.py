from ansys.dyna.core import Deck
from ansys.units import Quantity

from ansys.materials.manager._models._material_models.cofficient_of_thermal_expansion_isotropic import (  # noqa: E501
    CoefficientofThermalExpansionIsotropic,
)
from ansys.materials.manager._models._material_models.density import Density
from ansys.materials.manager._models._material_models.elasticity_isotropic import (  # noqa: E501
    ElasticityIsotropic,
)
from ansys.materials.manager._models.material import Material
from ansys.materials.manager.material_manager import MaterialManager

model_1 = ElasticityIsotropic(
    youngs_modulus=Quantity(value=[5], units="Pa"), poissons_ratio=Quantity(value=[0.1], units="")
)
model_2 = Density(density=Quantity(value=[1], units=""))

model_3 = CoefficientofThermalExpansionIsotropic(
    coefficient_of_thermal_expansion=Quantity(value=[1], units="")
)

elastic_material = Material(name="Elastic Material", models=[model_1, model_2, model_3])
deck = Deck()
manager = MaterialManager(client=deck)
manager.add_material(elastic_material)
ls_dyna_material = manager.write_material("Elastic Material", 57, client=deck)
print(ls_dyna_material)
