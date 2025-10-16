import os
from pathlib import Path

from ansys.mapdl.core import launch_mapdl

from ansys.materials.manager.material_manager import MaterialManager

matml_file_path = Path(os.getcwd()) / "examples" / "data" / "material_isotropic.xml"

mapdl_client = launch_mapdl(
    version=252,
    override=True,
)

material_manager = MaterialManager(client=mapdl_client)
material_manager.read_from_matml(matml_file_path)
material_manager.write_to_matml("trial.xml")
material_manager.write_material("Isotropic Test Material", 1)
mapdl_client.exit()
