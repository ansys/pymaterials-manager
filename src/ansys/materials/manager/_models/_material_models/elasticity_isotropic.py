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

from ansys.materials.manager._models._common._base import _MapdlCore
from ansys.materials.manager._models._common._exceptions import ModelValidationException
from ansys.materials.manager._models._common._packages import SupportedPackage
from ansys.materials.manager._models._common.material_model import MaterialModel
from ansys.materials.manager._models._common.model_qualifier import ModelQualifier
from ansys.materials.manager.material import Material


class ElasticityIsotropic(MaterialModel):
    """Represents an isotropic elasticity material model."""

    name: Literal["Elasticity"] = Field(default="Elasticity", repr=False, frozen=True)
    supported_packages: SupportedPackage = Field(
        default=[SupportedPackage.MAPDL], repr=False, frozen=True
    )
    youngs_modulus: list[float] = Field(
        default=[],
        title="Young's modulus",
        description="The Young's modulus of the material.",
    )
    poissons_ratio: list[float] = Field(
        default=[],
        title="Poisson's ratio",
        description="The Poisson's ratio of the material.",
    )
    model_qualifiers: list[ModelQualifier] = Field(
        default=[ModelQualifier(name="Behavior", value="Isotropic")],
        title="Model Qualifiers",
        description="Model qualifiers for the isotropic elasticity model.",
    )

    def _write_mapdl(self, mapdl: _MapdlCore, material: "Material") -> None:
        if (
            not self.independent_parameters
            and len(self.youngs_modulus) == 1
            and len(self.poissons_ratio) == 1
        ):
            mapdl.mp("EX", material.material_id, self.youngs_modulus[0])
            mapdl.mp("PRXY", material.material_id, self.poissons_ratio[0])
        ### add variable cases

    def write_model(self, material: Material, pyansys_session: Any) -> None:
        """
        Write this model to the specified session.

        Parameters
        ----------
        material : Material
            The material to which this model belongs.
        pyansys_session : Any
            The session to write the model to.
        """
        is_ok, issues = self.validate_model()
        if not is_ok:
            raise ModelValidationException("\n".join(issues))

        if isinstance(pyansys_session, _MapdlCore):
            self._write_mapdl(pyansys_session, material)
        else:
            raise TypeError(
                "This model is only supported by MAPDL. Ensure that you have the correct"
                "type of the PyAnsys session."
            )

    def validate_model(self) -> tuple[bool, list[str]]:
        """
        Perform pre-flight validation of the model setup.

        Returns
        -------
        Tuple
            First element is Boolean. ``True`` if validation is successful. If ``False``,
            the second element contains a list of strings with more information.
        """
        failures = []
        is_ok = True

        if self.name is None or self.name == "":
            failures.append("Invalid materisl model name")
            is_ok = False
        if len(self.youngs_modulus) < 1:
            failures.append("Young's modulus value is not defined.")
            is_ok = False
        if len(self.poissons_ratio) < 1:
            failures.append("Poisson's ratio value is not defined.")
            is_ok = False
        if len(self.youngs_modulus) != len(self.poissons_ratio):
            failures.append(
                "The number of Young's modulus values must match the number of Poisson's ratio values."  # noqa: E501
            )
            is_ok = False
        return is_ok, failures
