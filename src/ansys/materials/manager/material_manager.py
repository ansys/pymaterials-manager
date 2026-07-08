# Copyright (C) 2022 - 2026 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Provides the ``MaterialManager`` class."""

import logging
from pathlib import Path
from typing import Any, Sequence

from ansys.dyna.core import Deck
from ansys.dyna.core.lib.keyword_base import KeywordBase

from .integrations import (
    FluentWriter,
    LsDynaWriter,
    MapdlWriter,
    MatmlReader,
    MatmlWriter,
    read_mapdl,
)
from .models import Material, MaterialModel
from .models._common import _FluentCore, _MapdlCore


class MaterialManager:
    """
    Manage material creation, assignment, and other management tasks.

    This class is the main entry point for the Pythonic material management interface.
    """

    _materials: dict[str, Material]
    _logger = logging.getLogger(__name__)

    def __init__(self):
        """Initialize the material manager instance."""
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

    def _get_materials_to_write(self, material_names: Sequence[str] | None) -> dict[str, Material]:
        """Return the materials to be written."""
        if self.materials is None or len(self.materials) == 0:
            raise Exception("No materials found in the library.")
        if not material_names:
            materials = self.materials
        else:
            materials = [
                self.get_material(name)
                for name in material_names
                if self.get_material(name) is not None
            ]
        return materials

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

    def write_to_matml(self, path: str | Path, material_names: list[str] | None = None) -> None:
        """Write the materials in the library to a MatML file."""
        materials = self._get_materials_to_write(material_names)
        writer = MatmlWriter(materials)
        writer.write(path, indent=True)

    def read_from_matml(self, path: str | Path) -> None:
        """Read materials from a MatML file and add them to the library."""
        matml_reader = MatmlReader(path)
        material_dic = matml_reader.convert_matml_materials()
        if not self.materials:
            self._materials = material_dic
        else:
            self._add_library(material_dic)
        print("The materials were correctly read from the provided xml file.")

    def write_to_mapdl(
        self,
        mapdl_client: _MapdlCore | None = None,
        material_names: list[str] | None = None,
        material_ids: list[int] | None = None,
        reference_temperatures: list[float] | None = None,
    ) -> list[str] | None:
        """Write a material to the connected MAPDL session."""
        materials = self._get_materials_to_write(material_names)
        writer = MapdlWriter(materials)
        return writer.write(mapdl_client, material_names, material_ids, reference_temperatures)

    def read_from_mapdl_session(self, mapdl_client: _MapdlCore) -> None:
        """Read material from the pyansys client session."""
        materials = read_mapdl(mapdl_client)
        self._add_library(materials)

    def write_to_ls_dyna(
        self, deck: Deck | None = None, material_names: list[str] | None = None
    ) -> list[KeywordBase] | None:
        """Write the materials in the library to a LS-DYNA keyword file."""
        materials = self._get_materials_to_write(material_names)
        writer = LsDynaWriter(materials)
        return writer.write(deck)

    def write_to_fluent(
        self, fluent_client: _FluentCore, material_names: list[str] | None = None
    ) -> list[dict]:
        """Write a material to the connected Fluent session."""
        materials = self._get_materials_to_write(material_names)
        writer = FluentWriter(materials)
        return writer.write(material_names)

    @classmethod
    def from_grantami(
        cls,
        granta_mi_url: str,
        package_name: str | None = None,
        verify_ssl: bool = True,
        oidc_config=None,
    ) -> "MaterialManager":
        """
        Create a :class:`MaterialManager` pre-populated from a Granta MI REST session.

        Opens the Granta Material Picker in the default browser, waits for the user
        to select a material, then converts the response into ``Material`` objects.

        Requires the ``grantami`` extra::

            pip install ansys-materials-manager[grantami]

        Parameters
        ----------
        granta_mi_url : str
            Base URL of the Granta MI instance, e.g. ``"https://my_granta_mi_server.com"``.
        package_name : str, optional
            The package name used to define which material models are exported from
            Granta MI.
        verify_ssl : bool
            Whether to verify SSL certificates.  Defaults to ``True``.
        oidc_config : MSALOIDCConfiguration | None
            OIDC configuration used to authenticate with the identity provider. Required if
            connecting to an on-premises Granta MI deployment.

        Returns
        -------
        MaterialManager
            A new ``MaterialManager`` instance populated with the selected materials.

        Raises
        ------
        ImportError
            If the required Granta MI REST client dependencies are not installed.
        """
        manager = cls()
        manager.read_from_grantami(
            granta_mi_url=granta_mi_url,
            package_name=package_name,
            verify_ssl=verify_ssl,
            oidc_config=oidc_config,
        )
        return manager

    def read_from_grantami(
        self,
        granta_mi_url: str,
        package_name: str | None = None,
        verify_ssl: bool = True,
        oidc_config=None,
    ) -> None:
        """
        Fetch materials from Granta MI and add them to the library.

        Opens the Granta Material Picker in the default browser, waits for a selection, then merges
        the returned materials into this manager's library.

        Requires the ``grantami`` extra::

            pip install ansys-materials-manager[grantami]

        Parameters
        ----------
        granta_mi_url : str
            Base URL of the Granta MI instance, e.g. ``"https://my_granta_mi_server.com"``.
        package_name : str, optional
            The package name used to define which material models are exported from
            Granta MI.
        verify_ssl : bool
            Whether to verify SSL certificates. Defaults to ``True``.
        oidc_config : MSALOIDCConfiguration | None
            OIDC configuration used to authenticate with the identity provider. Required if
            connecting to an on-premises Granta MI deployment.

        Raises
        ------
        ImportError
            If the required Granta MI REST client dependencies are not installed.
        """
        import webbrowser

        from .integrations.rest.rest_material_reader import RestMaterialReader
        from .integrations.rest.rest_session_client import RestSessionClient

        with RestSessionClient(
            base_url=granta_mi_url,
            package_name=package_name,
            verify_ssl=verify_ssl,
            oidc_config=oidc_config,
        ) as client:
            picker_url = client.granta_material_picker_url
            self._logger.info("Opening Granta Material Picker in browser: %s", picker_url)
            webbrowser.open(picker_url)
            raw_data = client.fetch_data()

        material_dict = RestMaterialReader(raw_data).convert_materials()
        self._add_library(material_dict)
        self._logger.info("Added %d material(s) from Granta MI.", len(material_dict))
