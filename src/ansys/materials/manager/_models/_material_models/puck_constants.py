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
from ansys.materials.manager.material import Material


class PuckConstants(MaterialModel):
    """Represents a Puck constants material model for composite materials."""

    name: Literal["Puck Constants"] = Field(default="Puck Constants", repr=False, frozen=True)
    supported_packages: SupportedPackage = Field(
        default=[SupportedPackage.MAPDL], repr=False, frozen=True
    )
    compressive_inclination_xz: list[float] = Field(
        default=[],
        title="Compressive Inclination XZ",
        description="The compressive inclination in the XZ plane for the Puck constants model.",
    )
    compressive_inclination_yz: list[float] = Field(
        default=[],
        title="Compressive Inclination YZ",
        description="The compressive inclination in the YZ plane for the Puck constants model.",
    )
    tensile_inclination_xz: list[float] = Field(
        default=[],
        title="Tensile Inclination XZ",
        description="The tensile inclination in the XZ plane for the Puck constants model.",
    )
    tensile_inclination_yz: list[float] = Field(
        default=[],
        title="Tensile Inclination YZ",
        description="The tensile inclination in the YZ plane for the Puck constants model.",
    )
    material_property: str = Field(
        default="",
        title="Material Property",
        description="The material property for the Puck constants model.",
    )

    def write_model(self, material: Material, pyansys_session: Any) -> None:
        """Write this model to the specified session."""
        pass

    def validate_model(self) -> tuple[bool, list[str]]:
        """Validate the model."""
        pass
