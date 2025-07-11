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


from typing import Any, Dict, Literal

from ansys.units import Quantity
import numpy as np
from pydantic import Field, model_validator

from ansys.materials.manager._models._common import (
    MaterialModel,
    ParameterField,
    QualifierType,
    validate_and_initialize_model_qualifiers,
)
from ansys.materials.manager._models._common._base import _MapdlCore
from ansys.materials.manager.util.mapdl.mapdl_writer import write_table_dep_values


class ElasticityAnisotropic(MaterialModel):
    """Represents an isotropic elasticity material model."""

    name: Literal["Elasticity"] = Field(default="Elasticity", repr=False, frozen=True)
    column_1: Quantity | None = ParameterField(
        default=None, description="The first column of the elasticity matrix.", matml_name="D[*,1]"
    )
    column_2: Quantity | None = ParameterField(
        default=None, description="The second column of the elasticity matrix.", matml_name="D[*,2]"
    )
    column_3: Quantity | None = ParameterField(
        default=None, description="The third column of the elasticity matrix.", matml_name="D[*,3]"
    )
    column_4: Quantity | None = ParameterField(
        default=None, description="The fourth column of the elasticity matrix.", matml_name="D[*,4]"
    )
    column_5: Quantity | None = ParameterField(
        default=None, description="The fifth column of the elasticity matrix.", matml_name="D[*,5]"
    )
    column_6: Quantity | None = ParameterField(
        default=None, description="The sixth column of the elasticity matrix.", matml_name="D[*,6]"
    )

    @model_validator(mode="before")
    def _initialize_qualifiers(cls, values) -> Dict:
        expected_qualifiers = {"Behavior": ["Anisotropic", QualifierType.STRICT]}
        values["model_qualifiers"] = validate_and_initialize_model_qualifiers(
            values, expected_qualifiers
        )
        return values

    def _write_mapdl(self, material_id: int) -> str:
        d = np.column_stack(
            (
                self.column_1.value,
                self.column_2.value,
                self.column_3.value,
                self.column_4.value,
                self.column_5.value,
                self.column_6.value,
            )
        )
        # extract the lower triangular elements column-wise
        dependent_values = []
        for j in range(6):
            dependent_values.extend(d[j:, j])

        material_string = write_table_dep_values(
            material_id=material_id,
            label="ELASTIC",
            dependent_values=dependent_values,
            tb_opt="AELS",
        )
        return material_string

    def write_model(self, material_id: int, pyansys_session: Any) -> None:
        """Write the anisotropic elasticity model to the pyansys session."""
        self.validate_model()
        if isinstance(pyansys_session, _MapdlCore):
            material_string = self._write_mapdl(material_id)
        else:
            raise Exception("The session is not supported.")
        return material_string

    def validate_model(self) -> None:
        """Validate anisotropic elasticity."""
        if self.independent_parameters:
            raise Exception("Variable anisotropic elasticity is currently not supported.")
        if not all(
            [
                isinstance(self.column_1.value, np.ndarray),
                isinstance(self.column_2.value, np.ndarray),
                isinstance(self.column_3.value, np.ndarray),
                isinstance(self.column_4.value, np.ndarray),
                isinstance(self.column_5.value, np.ndarray),
                isinstance(self.column_6.value, np.ndarray),
            ]
        ):
            raise Exception("At least one of the columns is not defined as an array")
        if not all(
            [
                len(self.column_1.value) == 6,
                len(self.column_2.value) == 6,
                len(self.column_3.value) == 6,
                len(self.column_4.value) == 6,
                len(self.column_5.value) == 6,
                len(self.column_6.value) == 6,
            ]
        ):
            raise Exception("At least one of the columns has not length equal 6")
