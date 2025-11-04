# Copyright (C) 2022 - 2025 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
# #
# #
# # Permission is hereby granted, free of charge, to any person obtaining a copy
# # of this software and associated documentation files (the "Software"), to deal
# # in the Software without restriction, including without limitation the rights
# # to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# # copies of the Software, and to permit persons to whom the Software is
# # furnished to do so, subject to the following conditions:
# #
# # The above copyright notice and this permission notice shall be included in all
# # copies or substantial portions of the Software.
# #
# # THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# # IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# # FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# # AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# # LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# # OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# # SOFTWARE.

"""Provides the ``MaterialManager`` class."""

from pathlib import Path
from typing import Any, Sequence

from ansys.materials.manager._models._common import _FluentCore, _MapdlCore
from ansys.materials.manager._models._common.material_model import MaterialModel
from ansys.materials.manager._models.material import Material
from ansys.materials.manager.util.mapdl.mapdl_reader import read_mapdl
from ansys.materials.manager.util.matml.matml_parser import MatmlReader
from ansys.materials.manager.util.matml.matml_to_material import convert_matml_materials
from ansys.materials.manager.util.matml.writer_matml import WriterMatml
from ansys.materials.manager.util.writer import get_writer


class MaterialManager:
    """
    Manage material creation, assignment, and other management tasks.

    This class is the main entry point for the Pythonic material management interface.
    """

    _materials: dict[str, Material]
    _client: Any | None

    def __init__(self, client: Any | None = None):
        """Initialize the material manager instance."""
        self._client = client
        self._materials = {}

    @property
    def materials(self) -> dict[str, Material]:
        """The material models."""
        return self._materials

    @property
    def client(self) -> Any:
        """The provided client."""
        return self._client

    @client.setter
    def client(self, value: Any) -> None:
        self._client = value

    def add_material(self, material: Material) -> None:
        """Add a material into the library."""
        material_found = self.materials.get(material.name, None)
        if material_found is None:
            self.materials[material.name] = material
            print(f"The material with name {material.name} was added to the library.")
            # TODO: we might need to consider taking care of the ids and uids probably
        else:
            raise Exception(
                f"The material with name {material.name} is already present in the library."
            )

    def extend_material(self, material_name: str, material_models: list[MaterialModel]) -> None:
        """Extend the models defined within a specific material."""
        material = self.materials.get(material_name, None)
        if material is not None:
            material.append_models(material_models)
        else:
            print(f"The material with name {material_name} was not found.")

    def delete_material(self, material_name: str):
        """Delete a material from the library."""
        material = self.materials.pop(material_name, None)
        if material is None:
            print(f"The material with name {material_name} was not found.")

    def read_from_matml(self, path: str | Path) -> None:
        """Read materials from a MatML file and add them to the library."""
        parsed_data = MatmlReader.parse_from_file(path)
        materials = convert_matml_materials(
            {k: v["material"] for k, v in parsed_data.items()},
            {k: v["transfer_id"] for k, v in parsed_data.items()},
            0,
        )
        material_dic = {material.name: material for material in materials}
        if not self.materials:
            self._materials = material_dic
        else:
            self._add_library(material_dic)
        print("The materials were correctly read from the provided xml file.")

    def write_to_matml(self, path: str | Path, materials: Sequence[Material] | None = None) -> None:
        """Write the materials in the library to a MatML file."""
        if not materials:
            materials = list(self.materials.values())
        writer = get_writer("Matml")
        writer.materials = materials
        assert isinstance(writer, WriterMatml)
        writer.export(str(path), indent=True)
        print(f"{len(self.materials)} materials written to {path}.")

    def get_material(self, material_name) -> Material | None:
        """Return a material from the library."""
        material = self.materials.get(material_name, None)
        if material is None:
            print(f"The material with name {material_name} was not found in the library.")
        return material

    def _add_library(self, material_dic: dict[str, Material]):
        """Add a material dictionary to the library."""
        for material in material_dic.values():
            if material.name in self.materials:
                raise Exception(
                    (
                        f"The materials were not added to the library as {material.name}",
                        "is already present.",
                    )
                )
        self._materials |= material_dic

    def write_material(self, material_name: str, material_id: int | None = None, **kwargs) -> None:
        """Write material to the pyansys session."""
        material = self._materials.get(material_name, None)
        if not material:
            print(f"Material with name {material_name} has not been found in the library.")
            return
        if material_id is None:
            material_id = material.mat_id
        if not self.client:
            print("The pyansys session has not been defined.")
            return
        writer = get_writer(self.client)
        writer.write_material(
            material=material, material_id=material_id, client=self.client, **kwargs
        )

    def read_from_client_session(self) -> None:
        """Read material from the pyansys client session."""
        if isinstance(self._client, _MapdlCore):
            materials = read_mapdl(self._client)
            self._add_library(materials)
        elif isinstance(self._client, _FluentCore):
            raise NotImplementedError("The method has not been implemented yet.")
        else:
            print("Not valid pyansys session.")
