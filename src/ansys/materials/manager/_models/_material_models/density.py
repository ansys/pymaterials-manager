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

from typing import Any, Literal, Sequence

from ansys.units import Quantity
from pydantic import Field

from ansys.materials.manager._models._common import MaterialModel, ParameterField, SupportedPackage
from ansys.materials.manager._models._common._base import _FluentCore, _MapdlCore
from ansys.materials.manager.util.mapdl import (
    write_constant_property,
    write_interpolation_options,
    write_table_values,
)
from ansys.materials.manager.util.mapdl.mapdl_writer import write_temperature_table_values


class Density(MaterialModel):
    """Represents an isotropic density material model."""

    name: Literal["Density"] = Field(default="Density", repr=False, frozen=True)
    density: Quantity | None = ParameterField(
        default=None,
        description="The density of the material.",
        matml_name="Density",
    )
    supported_packages: list[SupportedPackage] = Field(
        default=[SupportedPackage.MAPDL, SupportedPackage.FLUENT],
        title="Supported Packages",
        description="The list of supported packages.",
        frozen=True,
    )

    def _write_mapdl(self, material_id: int) -> str:
        if self.independent_parameters is None:
            material_string = write_constant_property(
                label="DENS",
                property=self.density.value,
                material_id=material_id,
                unit=self.density.unit,
            )
            return material_string
        elif (
            len(self.independent_parameters) == 1
            and self.independent_parameters[0].name == "Temperature"
        ):
            if len(self.independent_parameters[0].values.value) == 1:
                material_string = write_constant_property(
                    label="DENS",
                    property=self.density.value,
                    material_id=material_id,
                    unit=self.density.unit,
                )
                return material_string
            else:
                material_string = write_temperature_table_values(
                    labels=["DENS"],
                    dependent_parameters=[self.density.value],
                    dependent_parameters_unit=[self.density.unit],
                    material_id=material_id,
                    temperature_parameter=self.independent_parameters[0],
                )
                return material_string
        else:
            parameters_str, table_str = write_table_values(
                label="DENS",
                dependent_parameters=[self.density.value],
                material_id=material_id,
                independent_parameters=self.independent_parameters,
            )
            material_string = parameters_str + "\n" + table_str

            if self.interpolation_options:
                interpolation_string = write_interpolation_options(
                    interpolation_options=self.interpolation_options,
                    independent_parameters=self.independent_parameters,
                )
                material_string += "\n" + interpolation_string

        return material_string

    def _write_fluent(self) -> dict:
        return {
            "density": {
                "option": "constant",
                "value": (
                    self.density.value[0]
                    if isinstance(self.density.value, Sequence)
                    else self.density.value
                ),
            }
        }

    def write_model(self, material_id: int, pyansys_session: Any) -> str | dict:
        """Write this model to the specified session."""
        self.validate_model()
        if isinstance(pyansys_session, _MapdlCore):
            material = self._write_mapdl(material_id)
        elif isinstance(pyansys_session, _FluentCore):
            material = self._write_fluent()
        else:
            raise Exception("The session is not supported.")
        return material
