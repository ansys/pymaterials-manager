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

from ansys.materials.manager._models._common import _MapdlCore
from ansys.materials.manager._models._common.material_model import MaterialModel
from ansys.materials.manager._models.material import Material
from ansys.materials.manager.util.common_writer import register_writer
from ansys.materials.manager.util.mapdl.mapdl_writer import (
    write_constant_properties,
    write_interpolation_options,
    write_table_values,
    write_temperature_reference_value,
    write_temperature_table_values,
)

TABLE_LABELS = {
    "ElasticityIsotropic": "ELASTIC",
    "ElasticityOrthotropic": "ELASTIC",
    "CoefficientofThermalExpansionIsotropic": "CTE",
    "CoefficientofThermalExpansionOrthotropic": "CTE",
}

TABLE_TBOPT = {
    "ElasticityIsotropic": "ISOT",
    "ElasticityOrthotropic": "OELM",
    "CoefficientofThermalExpansionIsotropic": None,
    "CoefficientofThermalExpansionOrthotropic": None,
}


@register_writer("MapdlGrpc")
class WriterMapdl:
    """Class containing the methods for writing into a madpl session."""

    def _get_table_label(self, model_name: str) -> str | None:
        """Get table label string."""
        return TABLE_LABELS.get(model_name, None)

    def _get_tbopt(self, model_name: str) -> str | None:
        """Get table tbopt string."""
        return TABLE_TBOPT.get(model_name, None)

    def _get_labels(self, model: MaterialModel) -> list[str]:
        """Get mapdl property label string."""
        if model.name == "Coefficient of Thermal Expansion":
            for qualfier in model.model_qualifiers:
                if qualfier.name == "Definition":
                    if qualfier.value == "Instantaneous":
                        labels = [
                            field.mapdl_name[0]
                            for field in model.__class__.model_fields.values()
                            if hasattr(field, "mapdl_name") and field.mapdl_name
                        ]
                    else:
                        labels = [
                            field.mapdl_name[1]
                            for field in model.__class__.model_fields.values()
                            if hasattr(field, "mapdl_name") and field.mapdl_name
                        ]
        else:
            labels = [
                field.mapdl_name
                for field in model.__class__.model_fields.values()
                if hasattr(field, "mapdl_name") and field.mapdl_name
            ]
        return labels

    def _write_material_model(self, model: MaterialModel, material_id: int):
        """Write the material model string."""
        labels = self._get_labels(model)
        dependant_parameter_names = [
            model_name
            for model_name, field in model.__class__.model_fields.items()
            if hasattr(field, "mapdl_name") and field.mapdl_name
        ]
        dict_model = model.model_dump()
        dependent_parameters = []
        dependent_parameters_units = []
        material_string = ""
        for name in dependant_parameter_names:
            value = dict_model[name]["value"]
            units = dict_model[name]["units"]
            dependent_parameters.append(value.tolist())
            dependent_parameters_units.append(units)
        if not model.independent_parameters:
            material_string += write_constant_properties(
                labels=labels,
                properties=dependent_parameters,
                property_units=dependent_parameters_units,
                material_id=material_id,
            )
            return material_string
        else:
            if (
                len(model.independent_parameters) == 1
                and model.independent_parameters[0].name.lower() == "temperature"
            ):
                if len(model.independent_parameters[0].values.value) == 1:
                    material_string += write_constant_properties(
                        labels=labels,
                        properties=dependent_parameters,
                        property_units=dependent_parameters_units,
                        material_id=material_id,
                    )
                    return material_string
                else:
                    material_string += write_temperature_table_values(
                        labels=labels,
                        dependent_parameters=dependent_parameters,
                        dependent_parameters_unit=dependent_parameters_units,
                        material_id=material_id,
                        temperature_parameter=model.independent_parameters[0],
                    )
                    return material_string
            else:
                table_label = self._get_table_label(model.__class__.__name__)
                tb_opt = self._get_tbopt(model.__class__.__name__)
                parameters_str, table_str = write_table_values(
                    label=table_label,
                    dependent_parameters=dependent_parameters,
                    material_id=material_id,
                    independent_parameters=model.independent_parameters,
                    tb_opt=tb_opt,
                )
                material_string += parameters_str + "\n" + table_str

            if model.interpolation_options:
                interpolation_string += write_interpolation_options(
                    interpolation_options=model.interpolation_options,
                    independent_parameters=model.independent_parameters,
                )
                material_string += "\n" + interpolation_string
        return material_string

    def write_material(
        self, material: Material, material_id: int, client: _MapdlCore, **kwargs
    ) -> str:
        """Write the material into Mapdl."""
        reference_temperature = kwargs.get("reference_temperature", None)
        material_model_string = ""
        if reference_temperature:
            material_model_string += write_temperature_reference_value(
                material_id, reference_temperature
            )
        for model in material.models:
            model.validate_model()
            material_model_string += self._write_material_model(model, material_id)
        if material_model_string:
            client.prep7()
            client.input_strings(material_model_string)
