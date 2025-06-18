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

from typing import Any, Literal

from pydantic import Field

from ansys.materials.manager._models._common._packages import SupportedPackage
from ansys.materials.manager._models._common.material_model import MaterialModel
from ansys.materials.manager._models._common.model_qualifier import ModelQualifier
from ansys.materials.manager.material import Material


class Viscosity(MaterialModel):
    """Represents a Viscosity material model."""

    name: Literal["Viscosity"] = Field(default="Viscosity", repr=False, frozen=True)
    supported_packages: SupportedPackage = Field(
        default=[SupportedPackage.MATML], repr=False, frozen=True
    )
    model_qualifiers: list[ModelQualifier] = Field(
        default=[
            ModelQualifier(name="BETA", value="Mechanical.ModalAcoustics"),
        ],
        title="Model Qualifiers",
        description="Qualifiers that describe the model.",
    )
    viscosity: list[float] = Field(
        default=[],
        title="Viscosity",
        description="The viscosity of the material.",
    )

    def write_model(self, material: Material, pyansys_session: Any) -> None:
        """Write the anisotropic elasticity model to the pyansys session."""
        pass

    def validate_model(self) -> tuple[bool, list[str]]:
        """Validate the anisotropic elasticity model."""
        pass
