# Copyright (C) 2022 - 2025 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
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

"""Provides the ``matml_parser`` module."""

import os
from pydoc import locate
from typing import Optional, Sequence, Union
import warnings
import xml.etree.ElementTree as ET

from ansys.units import Quantity

from ansys.materials.manager._models._common.material_model import MaterialModel
from ansys.materials.manager._models.material import Material
from ansys.materials.manager.util.visitors import _matml_strings as matml_strings
from ansys.materials.manager.util.visitors._matml_model_map import MATERIAL_MODEL_MAP
from ansys.materials.manager.util.visitors._matml_parser import (
    fill_independent_parameter,
    fill_interpolation_options,
    get_data_and_unit,
    get_material_model_name_and_qualifiers,
    read_materials,
    read_metadata,
    read_transfer_ids,
)

_PATH_TYPE = Union[str, os.PathLike]
MODEL_NAMESPACE = "ansys.materials.manager._models._material_models."


class MatmlReader:
    """
    Parse a MatML (engineering data xml) file.

    Fills a nested dict with all the materials and their properties.
    The key of the first layer are the material names.
    The conversion into a specific format/object representation is implemented separately.

    The data can be accessed via matml_reader.materials
    """

    _materials: dict
    _transfer_ids = dict
    _matml_file_path: _PATH_TYPE

    def __init__(self, file_path: _PATH_TYPE):
        """
        Create a new MatML reader object.

        Parameters
        ----------
        file_path :
            MatML (engineering data xml) file path
        """
        self._matml_file_path = file_path
        self._materials = {}
        self._transfer_ids = {}
        if not os.path.exists(file_path):
            raise RuntimeError(f"Cannot initialize MatmlReader {file_path}. File does not exist!")
        self.parse_from_file()

    def _parse_text(self, matml_content: str) -> dict[str, Union[str, dict]]:
        """Read MatML (engineering data XML) data from a string.

        Returns the material information and the workbench transfer identities (if present).

        Parameters
        ----------
        matml_content: str
            MatML content in text form

        Returns
        -------
        dict[str, Union[str, dict]]
        """
        tree = ET.ElementTree(ET.fromstring(matml_content))
        root = tree.getroot()
        materials_node = root.find(matml_strings.MATERIALS_ELEMENT_KEY)
        if not materials_node:
            raise RuntimeError(
                "Materials node not found. Please check if this is a valid MATML file."
            )

        matml_doc_node = materials_node.find(matml_strings.MATML_DOC_KEY)
        if not matml_doc_node:
            raise RuntimeError("MATML node not found. Please check if this is a valid MATML file.")

        metadata_node = matml_doc_node.find(matml_strings.METADATA_KEY)
        if not metadata_node:
            raise RuntimeError(
                "Metadata node not found. Please check if this is a valid MATML file."
            )
        metadata_dict = read_metadata(metadata_node)

        materials = read_materials(matml_doc_node, metadata_dict)
        transfer_ids = read_transfer_ids(root, materials)
        return {
            material_id: {
                "material": materials[material_id],
                "transfer_id": transfer_ids[material_id],
            }
            for material_id in materials
        }

    def parse_from_file(self) -> None:
        """Read MatML (engineering data XML) data from a file.

        Returns the material information and the workbench transfer identities (if present).

        Parameters
        ----------
        file_path: Union[str, Path]
            Path to MatML file on disk

        Returns
        -------
        dict[str, Union[str, dict]]
        """
        file_path = self._matml_file_path

        with open(file_path, "r", encoding="utf8") as fp:
            file_content = fp.read()

        parsed_data = self._parse_text(file_content)
        self._materials = {k: v["material"] for k, v in parsed_data.items()}
        self._transfer_ids = {k: v["transfer_id"] for k, v in parsed_data.items()}

    @property
    def materials(self) -> Optional[dict]:
        """Return the parsed material data from the MatML file.

        Property will be None unless the parser has successfully parsed a MatML file.

        Returns
        -------
        Dict: Material data from the MatML file

        .. deprecated:: 0.2.3
           `materials` will be removed in version 0.3.0, instead use the static methods
           `parse_from_file` and `parse_from_text` to parse the MatML file and
           obtain the parsed material dictionary.
        """
        warnings.warn(
            "materials will be removed in version 0.3.0, instead use the static methods "
            "`parse_from_file` and `parse_from_text` to parse the MatML file.",
            DeprecationWarning,
        )
        return self._materials

    @property
    def transfer_ids(self) -> Optional[dict[str, str]]:
        """Return the parsed Workbench Transfer IDs from the MatML file.

        Property will be None unless the parser has successfully parsed a MatML file.

        Returns
        -------
        Dict: Workbench transfer IDs from the MatML file

        .. deprecated:: 0.2.3
           `transfer_ids` will be removed in version 0.3.0, instead use the static methods
           `parse_from_file` and `parse_from_text` to parse the MatML file and
           obtain the Workbench transfer IDs.
        """
        warnings.warn(
            "transfer_ids will be removed in version 0.3.0, instead use the static methods "
            "`parse_from_file` and `parse_from_text` to parse the MatML file.",
            DeprecationWarning,
        )
        return self._transfer_ids

    @property
    def matml_file_path(self) -> str:
        """Return the path to the target MatML file.

        .. deprecated:: 0.2.3
           `matml_file_path` will be removed in version 0.3.0, instead use the static methods
           `parse_from_file` and `parse_from_text` to parse the MatML file and
           obtain the parsed material dictionary and the Workbench transfer IDs.
        """
        warnings.warn(
            "matml_file_path will be removed in version 0.3.0, instead use the static methods "
            "`parse_from_file` and `parse_from_text` to parse the MatML file.",
            DeprecationWarning,
        )
        return self._matml_file_path

    def get_material(self, name: str) -> dict:
        """Return a certain material.

        .. deprecated:: 0.2.3
          `get_material` will be removed in version 0.3.0, instead use the static methods
          `parse_from_file` and `parse_from_text` to parse the MatML file and
          obtain the parsed material dictionary and the Workbench transfer ID.
        """
        warnings.warn(
            "get_material will be removed in version 0.3.0, instead use the static methods "
            "`parse_from_file` and `parse_from_text` to parse the MatML file.",
            DeprecationWarning,
        )

        if name not in self._materials.keys():
            available_keys = ", ".join(self._materials.keys())
            raise RuntimeError(
                f"Material {name} does not exist. Available materials are {available_keys}"
            )

        return self._materials[name]

    def map_to_material_attributes(self, material_model: MaterialModel, property_set: dict) -> dict:
        """
        Map MatML property set to material model attributes.

        Parameters
        ----------
        material_model : MaterialModel
            The material model to map the properties to.
        property_set : dict
            The property set containing the MatML properties.
        Returns
        -------
        dict
            A dictionary mapping material model attributes to their corresponding quantities.
        """
        mapping = MATERIAL_MODEL_MAP[material_model.__class__]
        if mapping.method_read:
            attributes, quantities = mapping.method_read(property_set)
        else:
            attributes = []
            quantities = []
            if mapping.labels:
                for i in range(len(mapping.labels)):
                    label = mapping.labels[i]
                    attribute = mapping.attributes[i]
                    if label in property_set.parameters.keys():
                        param = property_set.parameters[label]
                        data, units = get_data_and_unit(param)
                        attributes.append(attribute)
                        quantities.append(Quantity(value=data, units=units))
        return dict(zip(attributes, quantities))

    def is_supported(self, material_model: MaterialModel) -> bool:
        """
        Check if the material model is supported.

        Parameters
        ----------
        material_model : MaterialModel
            Material model to check.

        Returns
        -------
        bool
            True if the material model is supported, False otherwise.
        """
        if material_model.__class__ in MATERIAL_MODEL_MAP.keys():
            return True
        else:
            return False

    def convert_matml_materials(self) -> dict[str, Sequence[Material]]:
        """
        Convert MatML materials to the internal material representation.

        Returns
        -------
        dict[str, Sequence[Material]]
            A dictionary mapping material names to their Material objects.
        """
        # int to offset the material id (number) to avoid
        # conflicts with already existing materials
        index_offset = 0
        global_material_index = 1 + index_offset
        materials = {}
        for mat_id, material_data in self._materials.items():
            models = []
            for propset_name, property_set in material_data.items():
                cls_target, qualifiers = get_material_model_name_and_qualifiers(
                    propset_name, property_set
                )
                class_located = locate(cls_target)
                supported = False
                if class_located:
                    cls = class_located(model_qualifiers=qualifiers)
                    if self.is_supported(cls):
                        supported = True
                        attributes_map = self.map_to_material_attributes(cls, property_set)
                        for attribute, quantity in attributes_map.items():
                            setattr(cls, attribute, quantity)
                        independent_parameters = []
                        for param_value in property_set.parameters.values():
                            ind_param = param_value.qualifiers.get(matml_strings.VARIABLE_TYPE_KEY)
                            if (
                                ind_param
                                and ind_param.split(",")[0] == matml_strings.INDEPENDENT_KEY
                            ):
                                independent_param = fill_independent_parameter(param_value)
                                independent_parameters.append(independent_param)
                        if len(independent_parameters) > 0:
                            setattr(cls, "independent_parameters", independent_parameters)
                        if matml_strings.OPTIONS_VARIABLE_KEY in property_set.parameters.keys():
                            variable_options = property_set.parameters[
                                matml_strings.OPTIONS_VARIABLE_KEY
                            ].qualifiers
                            interpolation_options = fill_interpolation_options(variable_options)
                            setattr(cls, "interpolation_options", interpolation_options)

                        models.append(cls)
                if not supported:
                    print(f"Could not find a material model for: {cls_target.split('.')[-1]}")
            matml_material = Material(name=mat_id, material_id=global_material_index, models=models)
            if mat_id in self.transfer_ids.keys():
                matml_material.guid = self.transfer_ids[mat_id]
            materials[mat_id] = matml_material
            global_material_index += 1

        return materials
