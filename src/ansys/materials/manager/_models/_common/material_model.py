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

import abc

from pydantic import BaseModel, Field
from pyparsing import Any

from ansys.materials.manager._models._common._packages import SupportedPackage  # noqa: F401
from ansys.materials.manager._models._common.independent_parameter import IndependentParameter
from ansys.materials.manager._models._common.interpolation_options import InterpolationOptions
from ansys.materials.manager.material import Material


class MaterialModel(BaseModel, abc.ABC):
    """A base class for representing a material models."""

    name: str = Field(default="", title="Name", description="The name of the material model.")
    supported_packages: list[SupportedPackage] | None = Field(
        default=None,
        title="Supported Packages",
        description="The supported packages for this material model. Currently, only PyMAPDL and PyFluent are supported.",  # noqa: E501
    )
    independent_parameters: list[IndependentParameter] | None = Field(
        default=None,
        title="Independent Parameters",
        description="List of independent parameters for the model.",
    )
    interpolation_options: InterpolationOptions | None = Field(
        default=None,
        title="Interpolation Options",
        description="Options for interpolation of the material model data.",
    )

    @classmethod
    def load(cls, value: dict | None):
        """
        Load a material model from a dictionary.

        Parameters
        ----------
        value: dict | None
            Dictionary containing the material model data. If `None`, returns `None`.
        """
        if value is None:
            return None
        return cls(**value)

    @abc.abstractmethod
    def write_model(self, material: Material, pyansys_session: Any) -> None:
        """
        Write the model to the given PyAnsys session.

        This method should make some effort to validate the model state before writing.

        Parameters
        ----------
        material: Material
            Material object to associate this model with.
        pyansys_session: Any
            Supported PyAnsys product session. Only PyMAPDL and PyFluent are
            supported currently.
        """
        ...

    @abc.abstractmethod
    def validate_model(self) -> tuple[bool, list[str]]:
        """
        Perform pre-flight validation of the model setup.

        This method should not perform any calls to the MAPDL process.

        Returns
        -------
        Tuple
            First element is Boolean. ``True`` if validation is successful. If ``False``,
            the second element contains a list of strings with more information.
        """
        ...
