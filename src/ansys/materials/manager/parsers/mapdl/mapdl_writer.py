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
from ansys.materials.manager._models._material_models.cofficient_of_thermal_expansion_isotropic import (  # noqa: E501
    CoefficientofThermalExpansionIsotropic,
)
from ansys.materials.manager._models._material_models.cofficient_of_thermal_expansion_orthotropic import (  # noqa: E501
    CoefficientofThermalExpansionOrthotropic,
)
from ansys.materials.manager._models._material_models.density import Density
from ansys.materials.manager._models._material_models.elasticity_anisotropic import (
    ElasticityAnisotropic,
)
from ansys.materials.manager._models._material_models.elasticity_isotropic import (
    ElasticityIsotropic,
)
from ansys.materials.manager._models._material_models.elasticity_orthotropic import (
    ElasticityOrthotropic,
)
from ansys.materials.manager._models._material_models.hill_yield_criterion import HillYieldCriterion
from ansys.materials.manager._models._material_models.isotropic_hardening import IsotropicHardening
from ansys.materials.manager._models.material import Material
from ansys.materials.manager.parsers.base_visitor import BaseVisitor
from ansys.materials.manager.parsers.mapdl._mapdl_commands_parser import (
    TABLE_LABELS,
    TABLE_TBOPT,
    get_table_label,
    get_tbopt,
    write_constant_properties,
    write_interpolation_options,
    write_table_dep_values,
    write_table_value_per_temperature,
    write_table_values,
    write_tb_points_for_temperature,
    write_temperature_reference_value,
    write_temperature_table_values,
)

from ._mapdl_model_map import MATERIAL_MODEL_MAP  # noqa: F401


class MapdlWriter(BaseVisitor):
    """Mapdl writer."""

    def __init__(self, materials: list[Material]):
        """Initialize the Mapdl visitor."""
        super().__init__(materials=materials)
        self.visit_materials()

    def _write_standard(self, material_model: MaterialModel) -> str:
        """Write standard properties."""
        dependent_parameters_dict = self._populate_dependent_parameters(material_model)
        dependent_parameters_labels = list(dependent_parameters_dict.keys())
        dependent_parameters_value = []
        dependent_parameters_units = []
        for quantity in dependent_parameters_dict.values():
            dependent_parameters_value.append(quantity.value.tolist())
            dependent_parameters_units.append(quantity.unit)
        material_string = ""
        if not material_model.independent_parameters:
            material_string += write_constant_properties(
                labels=dependent_parameters_labels,
                properties=dependent_parameters_value,
                property_units=dependent_parameters_units,
                material_id=None,
            )
            return material_string
        else:
            if (
                len(material_model.independent_parameters) == 1
                and material_model.independent_parameters[0].name.lower() == "temperature"
            ):
                if len(material_model.independent_parameters[0].values.value) == 1:
                    material_string += write_constant_properties(
                        labels=dependent_parameters_labels,
                        properties=dependent_parameters_value,
                        property_units=dependent_parameters_units,
                        material_id=None,
                    )
                    return material_string
                else:
                    material_string += write_temperature_table_values(
                        labels=dependent_parameters_labels,
                        dependent_parameters=dependent_parameters_value,
                        dependent_parameters_unit=dependent_parameters_units,
                        material_id=None,
                        temperature_parameter=material_model.independent_parameters[0],
                    )
                    return material_string
            else:
                table_label = get_table_label(material_model.__class__.__name__)
                tb_opt = get_tbopt(material_model.__class__.__name__)
                parameters_str, table_str = write_table_values(
                    label=table_label,
                    dependent_parameters=dependent_parameters_value,
                    material_id=None,
                    independent_parameters=material_model.independent_parameters,
                    tb_opt=tb_opt,
                )
                material_string += parameters_str + "\n" + table_str
                return material_string

    def visit_standard(self, material_model: Density) -> str:
        """Visit standard."""
        material_string = self._write_standard(material_model)
        if material_model.interpolation_options:
            interpolation_string = write_interpolation_options(
                interpolation_options=material_model.interpolation_options,
                independent_parameters=material_model.independent_parameters,
            )
            material_string += "\n" + interpolation_string
        return material_string

    def visit_anisotropic(self, material_model: ElasticityAnisotropic) -> str:
        """Visit anisotropic."""
        dependent_parameters_dict = self._populate_dependent_parameters(material_model)
        material_string = write_table_dep_values(
            material_id=None,
            label="ELASTIC",
            dependent_values=dependent_parameters_dict["lower_triangular"],
            tb_opt="AELS",
        )
        return material_string

    def visit_hill_yield_criterion(self, material_model: HillYieldCriterion) -> str:
        """Visit hill yield criterion."""
        label = "HILL"
        dependent_parameters_dict = self._populate_dependent_parameters(material_model)
        dependent_values = list(dependent_parameters_dict.values())[0]
        tb_opt = list(dependent_parameters_dict.keys())[0]
        if not material_model.independent_parameters:
            dependent_values = [
                dep_val[0] for dep_val in dependent_values if isinstance(dep_val, np.ndarray)
            ]
            material_string = write_table_dep_values(
                material_id=None,
                label=label,
                dependent_values=dependent_values,
                tb_opt=tb_opt,
            )
            return material_string
        elif (
            len(material_model.independent_parameters) == 1
            and material_model.independent_parameters[0].name == "Temperature"
        ):
            if len(material_model.independent_parameters[0].values.value) == 1:
                material_string = write_table_dep_values(
                    material_id=None,
                    label=label,
                    dependent_values=dependent_values,
                    tb_opt=tb_opt,
                )
            else:
                material_string = write_table_value_per_temperature(
                    label=label,
                    material_id=None,
                    dependent_parameters=dependent_values,
                    temperature_parameter=material_model.independent_parameters[0],
                    tb_opt=tb_opt,
                )
            return material_string
        else:
            parameters_str, table_str = write_table_values(
                label=label,
                dependent_parameters=dependent_values,
                material_id=None,
                independent_parameters=material_model.independent_parameters,
                tb_opt=tb_opt,
            )
            material_string = parameters_str + "\n" + table_str

        if material_model.interpolation_options:
            interpolation_string = write_interpolation_options(
                interpolation_options=material_model.interpolation_options,
                independent_parameters=material_model.independent_parameters,
            )
            material_string += "\n" + interpolation_string

        return material_string

    def visit_isotropic_harderning(self, material_model: IsotropicHardening) -> str:
        """Write isotropic hardening."""
        plastic_strain = [
            ind_param.values.value.tolist()
            for ind_param in material_model.independent_parameters
            if ind_param.name == "Plastic Strain"
        ][0]
        temperature = [
            ind_param.values.value.tolist()
            for ind_param in material_model.independent_parameters
            if ind_param.name == "Temperature"
        ]
        table_parameters = [
            plastic_strain,
            material_model.stress.value.tolist(),
        ]
        table_label = TABLE_LABELS[material_model.__class__.__name__]
        table_tbopt = TABLE_TBOPT[material_model.__class__.__name__]
        if len(material_model.independent_parameters) == 1:
            temperature_parameter = len(table_parameters[0]) * [0]
            material_string = write_tb_points_for_temperature(
                label=table_label,
                table_parameters=table_parameters,
                material_id=None,
                temperature_parameter=temperature_parameter,
                tb_opt=table_tbopt,
            )

        elif len(material_model.independent_parameters) == 2 and len(temperature) == 1:
            material_string = write_tb_points_for_temperature(
                label=table_label,
                table_parameters=table_parameters,
                material_id=None,
                temperature_parameter=temperature[0],
                tb_opt=table_tbopt,
            )
        else:
            raise Exception("Only variable supported at the moment is temperature")

        if material_model.interpolation_options:
            interpolation_string = write_interpolation_options(
                interpolation_options=material_model.interpolation_options,
                independent_parameters=material_model.independent_parameters,
            )
            material_string += "\n" + interpolation_string

        return material_string

    def visit_material_model(self, material_name: str, material_model: MaterialModel) -> None:
        """Visit material model."""
        standard_models = (
            Density,
            ElasticityIsotropic,
            ElasticityOrthotropic,
            CoefficientofThermalExpansionIsotropic,
            CoefficientofThermalExpansionOrthotropic,
        )
        if isinstance(material_model, standard_models):
            model = self.visit_standard(material_model)
        elif isinstance(material_model, ElasticityAnisotropic):
            model = self.visit_anisotropic(material_model)
        elif isinstance(material_model, HillYieldCriterion):
            model = self.visit_hill_yield_criterion(material_model)
        elif isinstance(material_model, IsotropicHardening):
            model = self.visit_isotropic_harderning(material_model)
        else:
            return
        self._material_repr[material_name].append(model)

    def write(
        self,
        client: _MapdlCore | None = None,
        material_names: list[str] | None = None,
        material_ids: list[int] | None = None,
        reference_temperatures: list[float] | None = None,
    ) -> list[str] | None:
        """
        Write the materials into MAPDL representation.

        Parameters
        ----------
        client : _MapdlCore | None
            MAPDL client to write to. If None, return the material strings.
        material_names : list[str] | None
            List of material names to write. If None, write all materials.
        material_ids : list[int] | None
            List of material ids to write. If None, get the ids from the materials.
        reference_temperatures : list[float] | None
            List of reference temperatures to write. If None, use default values.

        Returns
        -------
        list[str] | None
            List of material strings if client is None, else None.
        """
        if material_names is None:
            material_names = []
            for material in self._materials:
                material_names.append(material.name)
        if material_ids is None:
            material_ids = []
            for material in material_names:
                material_ids.append(self.get_material_id(material))

        materials = []
        for idx, material_name in enumerate(material_names):
            ref_temp_string = None
            if reference_temperatures:
                ref_temp_string = write_temperature_reference_value(
                    material_ids[idx], reference_temperatures[idx]
                )
            if ref_temp_string is None:
                models = self._material_repr[material_name]
            else:
                models = [ref_temp_string] + self._material_repr[material_name]

            merged_models = "".join(s.replace("None", str(material_ids[idx])) for s in models)
            materials.append(merged_models)

        if client is None:
            return materials
        else:
            client.prep7()
            for material in materials:
                client.input_strings(material)
        return
