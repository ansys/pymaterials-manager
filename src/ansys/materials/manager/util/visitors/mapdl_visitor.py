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
from ansys.materials.manager._models.material import Material
from ansys.materials.manager.util.mapdl.writer_mapdl_utils import (
    TABLE_LABELS,
    TABLE_TBOPT,
    get_table_label,
    get_tbopt,
    write_constant_properties,
    write_interpolation_options,
    write_table_dep_values,
    write_table_values,
    write_temperature_reference_value,
    write_temperature_table_values,
)
from ansys.materials.manager.util.visitors.base_visitor import BaseVisitor
from ansys.materials.manager.util.visitors.common import ModelInfo
from ansys.materials.manager.util.visitors.mapdl_utils import map_anisotropic_elasticity

MATERIAL_MODEL_MAP = {
    Density: ModelInfo(labels=["DENS"], attributes=["density"]),
    ElasticityIsotropic: ModelInfo(
        labels=["EX", "PRXY"], attributes=["youngs_modulus", "poissons_ratio"]
    ),
    ElasticityOrthotropic: ModelInfo(
        labels=[
            "EX",
            "EY",
            "EZ",
            "GXY",
            "GYZ",
            "GXZ",
            "PRXY",
            "PRYZ",
            "PRXZ",
        ],
        attributes=[
            "youngs_modulus_x",
            "youngs_modulus_y",
            "youngs_modulus_z",
            "shear_modulus_xy",
            "shear_modulus_yz",
            "shear_modulus_xz",
            "poissons_ratio_xy",
            "poissons_ratio_yz",
            "poissons_ratio_xz",
        ],
    ),
    ElasticityAnisotropic: ModelInfo(method=map_anisotropic_elasticity),
}


class MapdlVisitor(BaseVisitor):
    """Mapdl visitor."""

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

    def visit_standard(self, material_model: Density) -> str:
        """Visit standard."""
        material_string = ""
        material_string += self._write_standard(material_model)
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
            label=TABLE_LABELS[material_model.__class__.__name__],
            dependent_values=dependent_parameters_dict["lower_triangular"],
            tb_opt=TABLE_TBOPT[material_model.__class__.__name__],
        )
        return material_string

    def visit_material_model(self, material_name: str, material_model: MaterialModel) -> None:
        """Visit material model."""
        if isinstance(material_model, Density | ElasticityIsotropic | ElasticityOrthotropic):
            model = self.visit_standard(material_model)
        elif isinstance(material_model, ElasticityAnisotropic):
            model = self.visit_anisotropic(material_model)
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
            if reference_temperatures:
                material_string += write_temperature_reference_value(
                    material_ids[idx], reference_temperatures[idx]
                )
            models = self._material_repr[material_name]
            merged_models = " ".join(s.replace("None", str(material_ids[idx])) for s in models)
            materials.append(merged_models)

        if client is None:
            return materials
        else:
            client.prep7()
            for material in materials:
                client.input_strings(material)
        return
