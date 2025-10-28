from unittest.mock import MagicMock

from ansys.units import Quantity

from ansys.materials.manager._models._common import _MapdlCore
from ansys.materials.manager._models._common.independent_parameter import IndependentParameter
from ansys.materials.manager._models._material_models.elasticity_isotropic import (
    ElasticityIsotropic,
)
from ansys.materials.manager._models.material import Material
from ansys.materials.manager.util.matml.matml_parser import MatmlReader
from ansys.materials.manager.util.matml.writer_matml import WriterMatml

# Create a linear elastic material model in pyMaterials-Manager
linear_elastic_material = Material(
    name="Isotropic Test Material",
    models=[
        ElasticityIsotropic(
            youngs_modulus=Quantity(value=[1000000], units="Pa"),
            poissons_ratio=Quantity(value=[0.3], units=""),
            independent_parameters=[
                IndependentParameter(
                    name="Temperature",
                    values=Quantity(value=[7.88860905221012e-31], units="C"),
                    default_value=22.0,
                )
            ],
        )
    ],
)


# Write MAPDL string using pyMaterials-Manager
mock_mapdl = MagicMock(spec=_MapdlCore)
material_string = linear_elastic_material.models[0].write_model(
    material_id=2, pyansys_session=mock_mapdl
)
print("MAPDL string:")
print(material_string)

# Write a MATML file using pyMaterials-Manager
writer = WriterMatml([linear_elastic_material])
writer.export("linear_elastic_material.xml", indent=True)

# Read a MATML file using pyMaterials-Manager
parsed_data = MatmlReader.parse_from_file(".\\linear_elastic_material.xml")
print("Read from MATML:")
print(parsed_data)

# Dump a material model into Json using pyMaterials-Manager
json = linear_elastic_material.models[0].model_dump()
print("Json dump:")
print(json)

# Load a material model from Json using pyMaterials-Manager
elasticity = ElasticityIsotropic.load(json)
print("Json load:")
print(elasticity)
