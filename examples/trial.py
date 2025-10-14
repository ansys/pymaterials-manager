from ansys.mapdl.core import launch_mapdl
from ansys.units import Quantity

from ansys.materials.manager._models._material_models.cofficient_of_thermal_expansion_isotropic import (  # noqa: E501
    CoefficientofThermalExpansionIsotropic,
)
from ansys.materials.manager._models._material_models.elasticity_isotropic import (
    ElasticityIsotropic,
)
from ansys.materials.manager._models.material import Material
from ansys.materials.manager.material_manager import MaterialManager
from ansys.materials.manager.util.mapdl.writer_mapdl import WriterMapdl

mapdl_client = launch_mapdl(
    version=252,
    override=True,
)

model_1 = ElasticityIsotropic(
    youngs_modulus=Quantity(value=[5], units="Pa"), poissons_ratio=Quantity(value=[0.1], units="")
)
writer = WriterMapdl()._write_material_model(model_1, 1)
model_2 = CoefficientofThermalExpansionIsotropic(
    coefficient_of_thermal_expansion=Quantity(value=[1e-6], units="C^-1")
)
elastic_material = Material(name="Elastic Material", models=[model_1, model_2])

manager = MaterialManager(client=mapdl_client)
manager.add_material(elastic_material)
manager.write_material("Elastic Material", 1)
