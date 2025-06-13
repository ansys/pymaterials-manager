from pathlib import Path

from ansys.materials.manager._models.material import Material
from ansys.materials.manager.util.matml.matml_from_material import MatmlWriter
from ansys.materials.manager.util.matml.matml_parser import MatmlReader
from ansys.materials.manager.util.matml.matml_to_material import convert_matml_materials


def _add_library(materials_database: dict[str, Material], material_dic: dict[str, Material]):
    for material in material_dic.values():
        if material.name in materials_database:
            raise Exception(
                (
                    f"The materials were not added to the library as {material.name}",
                    "is already present.",
                )
            )
    materials_database |= material_dic
    return materials_database


material_database = {}
parsed_data = MatmlReader.parse_from_file(
    str(Path.cwd() / "examples" / "data" / "MatML_unittest_density.xml")
)
materials = convert_matml_materials(
    {k: v["material"] for k, v in parsed_data.items()},
    {k: v["transfer_id"] for k, v in parsed_data.items()},
    0,
)
material_dic = {material.name: material for material in materials}
material_database = _add_library(material_database, material_dic)
print(material_database)
export_data = Path.cwd() / "examples" / "data" / "test_export.xml"
writer = MatmlWriter(material_database.values())
writer.export(str(export_data), indent=True)
