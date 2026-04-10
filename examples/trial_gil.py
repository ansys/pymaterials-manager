from pathlib import Path

from ansys.materials.manager.parsers.matml.matml_reader import MatmlReader

XML_FILE_PATH = Path(r"D:\AnsysDev\pymaterials-manager\examples\data").joinpath(
    "material_isotropic_GIL.xml"
)

matml_reader = MatmlReader(XML_FILE_PATH)
materials = matml_reader.convert_matml_materials()
variable_material = materials["Isotropic Test Material"]
elasticity = variable_material.get_model_by_name("Elasticity")
results = elasticity.query([0.25, 0.28, 0.4, 0.5])
print(results)
