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
import numpy as np

from ansys.materials.manager._models._common import _MapdlCore
from ansys.materials.manager._models._common.material_model import MaterialModel
from ansys.materials.manager._models._material_models.elasticity_anisotropic import (
    ElasticityAnisotropic,
)
from ansys.materials.manager._models._material_models.hill_yield_criterion import HillYieldCriterion
from ansys.materials.manager._models._material_models.isotropic_hardening import IsotropicHardening
from ansys.materials.manager._models._material_models.zero_thermal_strain_reference_temperature_isotropic import (  # noqa: E501
    ZeroThermalStrainReferenceTemperatureIsotropic,
)
from ansys.materials.manager._models._material_models.zero_thermal_strain_reference_temperature_orthotropic import (  # noqa: E501
    ZeroThermalStrainReferenceTemperatureOrthotropic,
)
from ansys.materials.manager._models.material import Material
from ansys.materials.manager.util.common_writer import register_writer
from ansys.materials.manager.util.mapdl.writer_mapdl_utils import (
    write_constant_properties,
    write_interpolation_options,
    write_table_dep_values,
    write_table_value_per_temperature,
    write_table_values,
    write_tb_points_for_temperature,
    write_temperature_reference_value,
    write_temperature_table_values,
)

TABLE_LABELS = {
    "ElasticityIsotropic": "ELASTIC",
    "ElasticityOrthotropic": "ELASTIC",
    "ElasticityAnisotropic": "ELASTIC",
    "CoefficientofThermalExpansionIsotropic": "CTE",
    "CoefficientofThermalExpansionOrthotropic": "CTE",
    "Density": "DENS",
    "ThermalConductivityIsotropic": "THERM",
    "ThermalConductivityOrthotropic": "THERM",
    "IsotropicHardening": "PLASTIC",
    "HillYieldCriterion": "HILL",
}

TABLE_TBOPT = {
    "ElasticityIsotropic": "ISOT",
    "ElasticityOrthotropic": "OELM",
    "ElasticityAnisotropic": "AELS",
    "CoefficientofThermalExpansionIsotropic": None,
    "CoefficientofThermalExpansionOrthotropic": None,
    "Density": None,
    "ThermalConductivityIsotropic": "COND",
    "ThermalConductivityOrthotropic": "COND",
    "IsotropicHardening": "MISO",
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

    def _write_anisotropic_elasticity(self, model: ElasticityAnisotropic, material_id: int):
        d = np.column_stack(
            (
                model.column_1.value,
                model.column_2.value,
                model.column_3.value,
                model.column_4.value,
                model.column_5.value,
                model.column_6.value,
            )
        )
        # extract the lower triangular elements column-wise
        dependent_values = []
        for j in range(6):
            dependent_values.extend(d[j:, j])

        material_string = write_table_dep_values(
            material_id=material_id,
            label=TABLE_LABELS[model.__class__.__name__],
            dependent_values=dependent_values,
            tb_opt=TABLE_TBOPT[model.__class__.__name__],
        )
        return material_string

    def _write_isotropic_hardening(self, model: IsotropicHardening, material_id: int):
        plastic_strain = [
            ind_param.values.value.tolist()
            for ind_param in model.independent_parameters
            if ind_param.name == "Plastic Strain"
        ][0]
        temperature = [
            ind_param.values.value.tolist()
            for ind_param in model.independent_parameters
            if ind_param.name == "Temperature"
        ]
        table_parameters = [
            plastic_strain,
            model.stress.value.tolist(),
        ]
        table_label = TABLE_LABELS[model.__class__.__name__]
        table_tbopt = TABLE_TBOPT[model.__class__.__name__]
        if len(model.independent_parameters) == 1:
            temperature_parameter = len(table_parameters[0]) * [0]
            material_string = write_tb_points_for_temperature(
                label=table_label,
                table_parameters=table_parameters,
                material_id=material_id,
                temperature_parameter=temperature_parameter,
                tb_opt=table_tbopt,
            )

        elif len(model.independent_parameters) == 2 and len(temperature) == 1:
            material_string = write_tb_points_for_temperature(
                label=table_label,
                table_parameters=table_parameters,
                material_id=material_id,
                temperature_parameter=temperature[0],
                tb_opt=table_tbopt,
            )
        else:
            raise Exception("Only variable supported at the moment is temperature")
        return material_string

    def _write_hill_yield(self, model: HillYieldCriterion, material_id: int):
        label = TABLE_LABELS[model.__class__.__name__]
        for qualifier in model.model_qualifiers:
            if qualifier.name == "Separated Hill Potentials for Plasticity and Creep":
                creep = True if qualifier.value == "Yes" else False

        if not creep:
            dependent_values = [
                model.yield_stress_ratio_x.value,
                model.yield_stress_ratio_y.value,
                model.yield_stress_ratio_z.value,
                model.yield_stress_ratio_xy.value,
                model.yield_stress_ratio_yz.value,
                model.yield_stress_ratio_xz.value,
            ]
            tb_opt = ""
        else:
            dependent_values = [
                model.yield_stress_ratio_x_for_plasticity.value,
                model.yield_stress_ratio_y_for_plasticity.value,
                model.yield_stress_ratio_z_for_plasticity.value,
                model.yield_stress_ratio_xy_for_plasticity.value,
                model.yield_stress_ratio_yz_for_plasticity.value,
                model.yield_stress_ratio_xz_for_plasticity.value,
                model.yield_stress_ratio_x_for_creep.value,
                model.yield_stress_ratio_y_for_creep.value,
                model.yield_stress_ratio_z_for_creep.value,
                model.yield_stress_ratio_xy_for_creep.value,
                model.yield_stress_ratio_yz_for_creep.value,
                model.yield_stress_ratio_xz_for_creep.value,
            ]
            tb_opt = "PC"

        if not model.independent_parameters:
            dependent_values = [
                dep_val[0] for dep_val in dependent_values if isinstance(dep_val, np.ndarray)
            ]
            material_string = write_table_dep_values(
                material_id=material_id,
                label=label,
                dependent_values=dependent_values,
                tb_opt=tb_opt,
            )
            return material_string
        elif (
            len(model.independent_parameters) == 1
            and model.independent_parameters[0].name == "Temperature"
        ):
            if len(model.independent_parameters[0].values.value) == 1:
                material_string = write_table_dep_values(
                    material_id=material_id,
                    label=label,
                    dependent_values=dependent_values,
                    tb_opt=tb_opt,
                )
            else:
                material_string = write_table_value_per_temperature(
                    label=label,
                    material_id=material_id,
                    dependent_parameters=dependent_values,
                    temperature_parameter=model.independent_parameters[0],
                    tb_opt=tb_opt,
                )
            return material_string
        else:
            parameters_str, table_str = write_table_values(
                label=label,
                dependent_parameters=dependent_values,
                material_id=material_id,
                independent_parameters=model.independent_parameters,
                tb_opt=tb_opt,
            )
            material_string = parameters_str + "\n" + table_str
            return material_string

    def _write_material_model(
        self, model: MaterialModel, material_id: int, reference_temperature: float | None = None
    ):
        """Write the material model string."""
        material_string = ""
        if reference_temperature:
            material_string += write_temperature_reference_value(material_id, reference_temperature)
        if isinstance(model, ZeroThermalStrainReferenceTemperatureIsotropic) or isinstance(
            model, ZeroThermalStrainReferenceTemperatureOrthotropic
        ):
            material_string += (
                ""
                f"MPAMOD,{material_id},{model.zero_thermal_strain_reference_temperature.value[0]}\n"
            )
        elif isinstance(model, ElasticityAnisotropic):
            material_string += self._write_anisotropic_elasticity(model, material_id)
            return material_string
        elif isinstance(model, IsotropicHardening):
            material_string += self._write_isotropic_hardening(model, material_id)
            return material_string
        elif isinstance(model, HillYieldCriterion):
            material_string += self._write_hill_yield(model, material_id)
        else:
            labels = self._get_labels(model)
            dependant_parameter_names = [
                model_name
                for model_name, field in model.__class__.model_fields.items()
                if hasattr(field, "mapdl_name") and field.mapdl_name
            ]
            dict_model = model.model_dump()
            dependent_parameters = []
            dependent_parameters_units = []
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
            interpolation_string = write_interpolation_options(
                interpolation_options=model.interpolation_options,
                independent_parameters=model.independent_parameters,
            )
            material_string += "\n" + interpolation_string
        return material_string

    def write_material(self, material: Material, material_id: int, **kwargs) -> str:
        """Write the material into Mapdl."""
        client = kwargs.get("client", None)
        if not client or not isinstance(client, _MapdlCore):
            raise Exception("client not provided correctly")
        reference_temperature = kwargs.get("reference_temperature", None)
        for model in material.models:
            model.validate_model()
            material_model_string += self._write_material_model(
                model, material_id, reference_temperature
            )
        if material_model_string:
            client.prep7()
            client.input_strings(material_model_string)
