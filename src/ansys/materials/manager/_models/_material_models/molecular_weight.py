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

from typing import Literal, Sequence

from ansys.units import Quantity
from pydantic import Field

from ansys.materials.manager._models._common import MaterialModel, ParameterField, SupportedPackage
from ansys.materials.manager._models._common._base import _FluentCore


class MolecularWeight(MaterialModel):
    """Represents a molecular weight material model."""

    name: Literal["Molecular Weight"] = Field(default="Molecular Weight", repr=False, frozen=True)
    molecular_weight: Quantity | None = ParameterField(
        default=None,
        description="The molecular weight of the material.",
        matml_name="Molecular Weight",
    )
    supported_packages: list[SupportedPackage] = Field(
        default=[SupportedPackage.FLUENT],
        title="Supported Packages",
        description="The list of supported packages",
        frozen=True,
    )

    def _write_fluent(self) -> dict:
        return {
            "molecular_weight": {
                "option": "constant",
                "value": (
                    self.molecular_weight.value[0]
                    if isinstance(self.molecular_weight.value, Sequence)
                    else self.molecular_weight.value
                ),
            }
        }

    def write_model(self, material_id, pyansys_session):
        """Write molecular weight model."""
        self.validate_model()
        if isinstance(pyansys_session, _FluentCore):
            molecular_weight = self._write_fluent()
            return molecular_weight
