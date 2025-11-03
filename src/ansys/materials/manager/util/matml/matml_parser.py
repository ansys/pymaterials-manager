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

from dataclasses import dataclass
import os
from typing import Any, Dict, List, Optional, Union
import uuid
import warnings
import xml.etree.ElementTree as ET

from ansys.materials.manager.util.matml.utils import xml_to_unit

_PATH_TYPE = Union[str, os.PathLike]

MATERIALS_ELEMENT_KEY = "Materials"
MATML_DOC_KEY = "MatML_Doc"
METADATA_KEY = "Metadata"
BULKDATA_KEY = "BulkDetails"
UNITLESS_KEY = "Unitless"
BEHAVIOR_KEY = "Behavior"
WBTRANSFER_KEY = "ANSYSWBTransferData"
MAT_TRANSFER_ID = "DataTransferID"
QUALIFIER_KEY = "Qualifier"
PROPERTY_DATA_KEY = "PropertyData"
PARAMETER_VALUE_KEY = "ParameterValue"
# Todos:
#   version handling


@dataclass
class Parameter:
    """Define a parameter such as density or Young's Modulus."""

    # todo: units

    name: str
    data: Any
    qualifiers: Dict
    unit: str
    unit_name: str


@dataclass
class PropertySet:
    """Define a PropertySet which contains one or several parameters."""

    name: str
    parameters: Dict
    qualifiers: Dict
    unit: str
    unit_name: str


class MatmlReader:
    """
    Parse a MatML (engineering data xml) file.

    Fills a nested dict with all the materials and their properties.
    The key of the first layer are the material names.
    The conversion into a specific format/object representation is implemented separately.

    The data can be accessed via matml_reader.materials
    """

    _materials: Dict
    _transfer_ids = Dict
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

    @staticmethod
    def _convert(data: str, target: str) -> Union[str, float, List[float]]:
        # convert a string into a certain format (e.g. float)

        if target == "string":
            return data

        if target != "float":
            raise RuntimeError(f"unsupported format {target}. Skipped formatting {data}")

        if not data or not data.strip():
            return 0.0

        if data.count(",") > 0:
            data = data.split(",")
            return [float(v) for v in data]
        else:
            return float(data)

    @staticmethod
    def _read_metadata(metadata_node: Any) -> Dict:
        # Read the metadata

        data = {}
        for item in metadata_node.iter("ParameterDetails"):
            id, entry = xml_to_unit(item)
            data[id] = entry

        for item in metadata_node.iter("PropertyDetails"):
            id, entry = xml_to_unit(item)
            data[id] = entry
        return data

    @staticmethod
    def _read_qualifiers(property_node: Any) -> Dict:
        # returns the qualifiers such as behavior, interpolation options etc.
        qualifiers = {}
        for item in property_node.findall(QUALIFIER_KEY):
            qualifiers[item.attrib["name"]] = item.text
        return qualifiers

    @staticmethod
    def _read_property_sets_and_parameters(bulkdata: Any, metadata_dict: Dict) -> Dict:
        prop_dict = {}

        # iterate over the property sets
        for prop_data in bulkdata.findall(PROPERTY_DATA_KEY):
            property_key = prop_data.attrib["property"]
            property_name = metadata_dict[property_key]["Name"]
            property_unit = metadata_dict[property_key].get("Units", "")
            property_unit_name = metadata_dict[property_key].get("UnitsName", "")
            prop_set_qualifiers = MatmlReader._read_qualifiers(prop_data)

            parameters = {}

            # iterate over each parameter
            for parameter in prop_data.findall(PARAMETER_VALUE_KEY):
                parameter_key = parameter.attrib["parameter"]
                parameter_name = metadata_dict[parameter_key]["Name"]
                parameter_format = parameter.attrib["format"]
                param_qualifiers = MatmlReader._read_qualifiers(parameter)
                param_units = metadata_dict[parameter_key].get("Units", "")
                param_units_name = metadata_dict[parameter_key].get("UnitsName", "")
                data = MatmlReader._convert(parameter.find("Data").text, parameter_format)

                parameters[parameter_name] = Parameter(
                    name=parameter_name,
                    data=data,
                    qualifiers=param_qualifiers,
                    unit=param_units,
                    unit_name=param_units_name,
                )

            prop_dict[property_name] = PropertySet(
                name=property_name,
                qualifiers=prop_set_qualifiers,
                parameters=parameters,
                unit=property_unit,
                unit_name=property_unit_name,
            )

        return prop_dict

    @staticmethod
    def _read_materials(matml_doc_node: Any, metadata_dict: Dict) -> Dict:
        materials = {}
        for material in matml_doc_node.findall("Material"):
            bulkdata = material.find(BULKDATA_KEY)
            name = bulkdata.find("Name").text
            data = MatmlReader._read_property_sets_and_parameters(bulkdata, metadata_dict)
            materials[name] = data

        return materials

    @staticmethod
    def _read_transfer_ids(root: ET.Element, materials: Dict[str, Dict]) -> Dict[str, str]:
        transfer_ids = {}
        wb_transfer_element = root.find(WBTRANSFER_KEY)
        if wb_transfer_element:
            materials_element = wb_transfer_element.find(MATERIALS_ELEMENT_KEY)
            for mat in materials_element.findall("Material"):
                mat_name = mat.find("Name").text
                transfer_id_element = mat.find(MAT_TRANSFER_ID)

                if not mat_name in materials.keys():
                    raise RuntimeError(f"Transfer ID could not be set for material {mat_name}")
                if not transfer_id_element:
                    transfer_ids[mat_name] = str(uuid.uuid4())
                transfer_ids[mat_name] = transfer_id_element.text
        else:
            for material in materials.keys():
                transfer_ids[material] = str(uuid.uuid4())
        return transfer_ids

    @staticmethod
    def parse_from_file(file_path: _PATH_TYPE) -> Dict[str, Union[str, Dict]]:
        """Read MatML (engineering data XML) data from a file.

        Returns the material information and the workbench transfer identities (if present).

        Parameters
        ----------
        file_path: Union[str, Path]
            Path to MatML file on disk

        Returns
        -------
        Dict[str, Union[str, Dict]]
        """
        with open(file_path, "r", encoding="utf8") as fp:
            file_content = fp.read()
        return MatmlReader.parse_text(file_content)

    @staticmethod
    def parse_text(matml_content: str) -> Dict[str, Union[str, Dict]]:
        """Read MatML (engineering data XML) data from a string.

        Returns the material information and the workbench transfer identities (if present).

        Parameters
        ----------
        matml_content: str
            MatML content in text form

        Returns
        -------
        Dict[str, Union[str, Dict]]
        """
        tree = ET.ElementTree(ET.fromstring(matml_content))
        root = tree.getroot()
        materials_node = root.find(MATERIALS_ELEMENT_KEY)
        if not materials_node:
            raise RuntimeError(
                "Materials node not found. Please check if this is a valid MATML file."
            )

        matml_doc_node = materials_node.find(MATML_DOC_KEY)
        if not matml_doc_node:
            raise RuntimeError("MATML node not found. Please check if this is a valid MATML file.")

        metadata_node = matml_doc_node.find(METADATA_KEY)
        if not metadata_node:
            raise RuntimeError(
                "Metadata node not found. Please check if this is a valid MATML file."
            )
        metadata_dict = MatmlReader._read_metadata(metadata_node)

        materials = MatmlReader._read_materials(matml_doc_node, metadata_dict)
        transfer_ids = MatmlReader._read_transfer_ids(root, materials)
        return {
            material_id: {
                "material": materials[material_id],
                "transfer_id": transfer_ids[material_id],
            }
            for material_id in materials
        }

    def parse_matml(self) -> int:
        """Read MATML (engineering data XML) file.

        Output can be consumed via matml_reader.materials or
        matml_reader.get_material(name).

        Returns
        -------
        int: Number of imported materials.

        .. deprecated:: 0.2.3
          `parse_matml` will be removed in version 0.3.0, it is replaced by
          `parse_from_file` and `parse_from_text`.
        """
        warnings.warn(
            "parse_matml will be removed in version 0.3.0, use the static methods "
            "`parse_from_file` and `parse_from_text` instead",
            DeprecationWarning,
        )

        parsed_data = MatmlReader.parse_from_file(self._matml_file_path)
        self._materials = {k: v["material"] for k, v in parsed_data.items()}
        self._transfer_ids = {k: v["transfer_id"] for k, v in parsed_data.items()}
        return len(self._materials)

    @property
    def materials(self) -> Optional[Dict]:
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
    def transfer_ids(self) -> Optional[Dict[str, str]]:
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

    def get_material(self, name: str) -> Dict:
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


MODEL_NAMESPACE = "ansys.materials.manager._models._material_models."


# def convert_matml_materials(
#     materials_dict: Dict, transfer_ids: Dict, index_offset: int
# ) -> Sequence[Material]:
#     """
#     Convert a list of materials into Material objects.

#     Parameters
#     ----------
#     materials_dict:
#         dict of raw material data from a matml import
#     transfer_ids:
#         dict of material names and unique transfer ids
#     index_offset:
#         int to offset the material id (number) to avoid conflicts with already existing materials
#     Returns a list of Material objects
#     """
#     materials = []

#     global_material_index = 1 + index_offset
#     # loop over the materials
#     for mat_id, material_data in materials_dict.items():
#         models = []
#         # loop over the defined property sets
#         for propset_name, property_set in material_data.items():
#             cls_name = MODEL_NAMESPACE + parse_property_set_name(propset_name)
#             property_map = []
#             arguments = {}
#             qualifiers = []
#             for qualifier in property_set.qualifiers.keys():
#                 if qualifier == BEHAVIOR_KEY:
#                     cls_name += property_set.qualifiers[qualifier].replace(" ", "")
#                 qualifiers.append(
#                     ModelQualifier(name=qualifier, value=property_set.qualifiers[qualifier])
#                 )
#             cls = locate(cls_name)
#             if cls:
#                 property_map += list(cls.model_fields.keys())
#                 titles = {
#                     name: field_info.matml_name
#                     for name, field_info in cls.__fields__.items()
#                     if hasattr(field_info, "matml_name")  # noqa: E501
#                 }
#                 independent_parameters = []
#                 for name in property_map:
#                     if name == "independent_parameters":
#                         for param_value in property_set.parameters.values():
#                             ind_param = param_value.qualifiers.get("Variable Type")
#                             if ind_param and ind_param.split(",")[0] == "Independent":
#                                 data, units = get_data_and_unit(param_value)
#                                 independent_param = IndependentParameter(
#                                     name=param_value.name,
#                                     values=Quantity(value=data, units=units),
#                                     default_value=convert_to_float_or_keep(
#                                         param_value.qualifiers.get("Default Data", None)
#                                     ),
#                                     upper_limit=convert_to_float_or_keep(
#                                         param_value.qualifiers.get("Upper Limit", None)
#                                     ),
#                                     lower_limit=convert_to_float_or_keep(
#                                         param_value.qualifiers.get("Lower Limit", None)
#                                     ),
#                                 )
#                                 independent_parameters.append(independent_param)
#                     if name in titles.keys() and cls.__class__.__name__ != "ModelCoefficients":
#                         param_name = titles[name]
#                         if param_name in property_set.parameters.keys():
#                             param = property_set.parameters[param_name]
#                             if name not in ["red", "green", "blue", "material_property"]:
#                                 data, units = get_data_and_unit(param)
#                                 arguments[name] = Quantity(value=data, units=units)
#                             else:
#                                 data = param.data
#                                 if isinstance(data, float):
#                                     data = int(data)
#                                 arguments[name] = data

#                     if name == "model_qualifiers":
#                         arguments["model_qualifiers"] = qualifiers

#                 arguments["independent_parameters"] = independent_parameters
#                 if "Options Variable" in property_set.parameters.keys():
#                     variable_options = property_set.parameters["Options Variable"].qualifiers
#                     interpolation_options = InterpolationOptions(
#                         algorithm_type=variable_options.get("AlgorithmType", ""),
#                         normalized=variable_options.get("Normalized", True),
#                         cached=variable_options.get("Cached", True),
#                         quantized=variable_options.get("Quantized", None),
#                         extrapolation_type=variable_options.get("ExtrapolationType", "None"),
#                     )
#                     arguments["interpolation_options"] = interpolation_options
#                 if cls_name.split(".")[-1] == "ModelCoefficients":
#                     user_parameters = []
#                     for key_param, value_param in property_set.parameters.items():
#                         if value_param.qualifiers.get("UserMat Constant", None):
#                             data, units = get_data_and_unit(value_param)
#                             user_param = UserParameter(
#                                 name=key_param,
#                                 values=Quantity(value=data, units=units),
#                                 user_mat_constant=value_param.qualifiers["UserMat Constant"],
#                             )
#                             user_parameters.append(user_param)
#                     arguments["user_parameters"] = user_parameters

#                 obj = cls.load(arguments)
#                 models.append(obj)
#             else:
#                 print(f"Could not find a material model for: {cls_name.split('.')[-1]}")

#         mapdl_material = Material(name=mat_id, material_id=global_material_index, models=models)

#         if mat_id in transfer_ids.keys():
#             mapdl_material.guid = transfer_ids[mat_id]

#         materials.append(mapdl_material)

#         global_material_index += 1

#     return materials
