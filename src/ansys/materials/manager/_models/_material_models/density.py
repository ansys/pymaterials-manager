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

from pydantic import Field

from ansys.materials.manager._models._common._exceptions import ModelValidationException
from ansys.materials.manager._models._common._packages import SupportedPackage
from ansys.materials.manager._models._common.common import ParameterField
from ansys.materials.manager._models._common.material_model import MaterialModel
from ansys.materials.manager._models._mapdl.mapdl_constant_material_strings import CONSTANT_DENSITY
from ansys.units import Quantity
from ansys.materials.manager._models._common._base import _MapdlCore
from ansys.materials.manager._models._mapdl.mapdl_temperature_strings import TEMP_DATA
from ansys.materials.manager._models._mapdl.mapdl_variable_material_strings import VARIABLE_DENSITY

class Density(MaterialModel):
    """Represents an isotropic density material model."""

    name: Literal["Density"] = Field(default="Density", repr=False, frozen=True)
    supported_packages: SupportedPackage = Field(
        default=[SupportedPackage.MAPDL], repr=False, frozen=True
    )
    density: Quantity | None = ParameterField(
        default=None,
        description="The density of the material.",
        matml_name="Density",
    )

    def write_model(self, material_id: int, pyansys_session: Any) -> str:
        """Write this model to the specified session."""
        is_ok, issues = self.validate_model()
        if not is_ok:
            raise ModelValidationException("\n".join(issues))
        material_string = ""
        if self.independent_parameters is None:
            if isinstance(pyansys_session, _MapdlCore):
                material_string += CONSTANT_DENSITY.format(
                    material_id=material_id, 
                    density=str(self.density.value).strip("[]"),
                    unit=self.density.unit
                )
        else:
            if isinstance(pyansys_session, _MapdlCore):
                density_string = ", ".join(f"{v}" for v in self.density.value)
                for independent_parameter in self.independent_parameters:
                    if independent_parameter.name == "Temperature":
                        for i in range(len(independent_parameter.values.value)):
                            material_string += TEMP_DATA.format(
                                value_id=i + 1,
                                temperature_value=independent_parameter.values.value[i]
                            )
                material_string += VARIABLE_DENSITY.format(
                    material_id=material_id,
                    density=density_string,
                    unit=self.density.unit
                )
        return material_string


    def validate_model(self) -> tuple[bool, list[str]]:
        """Validate the model."""
        failures = []
        is_ok = True
        if self.density is None:
            failures.append("Value cannot be None")
            is_ok = False
            return is_ok, failures
        if isinstance(self.density, Sequence):
            if self.independent_parameters == None and len(self.density.value) > 1:
                failures.append("Multiple value of density have been defined but independent paramters are None")
                is_ok = False
                return is_ok, failures
            for independent_parameter in self.independent_parameters:
                if len(independent_parameter.values.value) != len(self.density.value):
                    failures.append(f"The number of defined indepedentent parameter is not equal to the number of densities defined for {independent_parameter.name}")
                is_ok = False
                return is_ok, failures
        return is_ok, failures
