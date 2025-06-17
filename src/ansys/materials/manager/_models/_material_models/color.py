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


class Color(MaterialModel):
    """Represents a Color material model."""

    name: Literal["Color"] = Field(default="Color", repr=False, frozen=True)
    supported_packages: SupportedPackage = Field(
        default=[SupportedPackage.MATML], repr=False, frozen=True
    )
    red: int | None = Field(default=None, title="Red", description="Red component of the color.")
    green: int | None = Field(
        default=None, title="Green", description="Green component of the color."
    )
    blue: int | None = Field(default=None, title="Blue", description="Blue component of the color.")

    material_property: str = Field(
        default="Appearance",
        title="Material Property",
        description="The material property associated with this model.",
        frozen=True,
    )

    def write_model(self, material: Material, pyansys_session: Any) -> None:
        """Write the anisotropic elasticity model to the pyansys session."""
        pass

    def validate_model(self) -> tuple[bool, list[str]]:
        """Validate the anisotropic elasticity model."""
        pass
