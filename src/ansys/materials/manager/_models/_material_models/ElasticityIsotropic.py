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

from typing import Any

from ansys.materials.manager._models._common._base import _MapdlCore
from ansys.materials.manager._models._common._exceptions import ModelValidationException
from ansys.materials.manager._models._common._packages import SupportedPackage
from ansys.materials.manager._models._common.dependent_parameter import DependentParameter
from ansys.materials.manager._models._common.independent_parameter import IndependentParameter
from ansys.materials.manager._models._common.material_model import MaterialModel
from ansys.materials.manager.material import Material


class ElasticityIsotropic(MaterialModel):
    """Represents an isotropic elasticity material model."""

    youngs_modulus: DependentParameter
    poisson_ratio: DependentParameter
    applicable_packages: SupportedPackage.MAPDL
    behavior: str = "Isotropic"

    def __init__(
        self,
        youngs_modulus: DependentParameter,
        poisson_ratio: DependentParameter,
        independent_parameter: list[IndependentParameter] | None = None,
        definition: str | None = None,
        localized_name: str | None = None,
        source: str | None = None,
        type: str | None = None,
    ) -> None:
        """
        Initialize an ElasticityIsotropic material model.

        Parameters
        ----------
        youngs_modulus : DependentParameter
            The Young's modulus of the material.
        poisson_ratio : DependentParameter
            The Poisson's ratio of the material.
        independent_parameter : list[IndependentParameter]
            List of independent parameters for the model.
        definition : str | None
            Definition of the material model.
        localized_name : str | None
            Localized name for the material model.
        source : str | None
            Source of the material model.
        type : str | None
            Type of the material model.
        """
        super().__init__(
            name="Elasticity Isotropic",
            independent_parameters=independent_parameter,
            definition=definition,
            localized_name=localized_name,
            source=source,
            type=type,
        )
        self.youngs_modulus = youngs_modulus
        self.poisson_ratio = poisson_ratio

    def _write_mapdl(self, mapdl: "_MapdlCore", material: "Material") -> None:
        if (
            not self.independent_parameters
            and len(self.youngs_modulus.values) == 0
            and len(self.poisson_ratio.values) == 0
        ):
            mapdl.mp("EX", material.material_id, self.youngs_modulus.values[0])
            mapdl.mp("PRXY", material.material_id, self.poisson_ratio.values[0])
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
            failures.append("Invalid property name")
            is_ok = False
        if self.youngs_modulus.values is None:
            failures.append("Young's modulus value cannot be None")
            is_ok = False
        if self.poisson_ratio.values is None:
            failures.append("Poisson's ratio value cannot be None")
            is_ok = False
        return is_ok, failures
