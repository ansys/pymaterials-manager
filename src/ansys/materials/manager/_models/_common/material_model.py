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

from ansys.materials.manager._models._common.independent_parameter import IndependentParameter
from ansys.materials.manager._models._common.interpolation_options import InterpolationOptions

from ._base import _BaseModel


class MaterialModel(_BaseModel):
    """A base class for representing a material models."""

    def __init__(
        self,
        name: str,
        independent_parameters: list[IndependentParameter] | None = None,
        interpolation_options: InterpolationOptions | None = None,
        definition: str | None = None,
        localized_name: str | None = None,
        source: str | None = None,
        type: str | None = None,
    ) -> None:
        """
        Initialize a MaterialModel instance.

        Parameters
        ----------
        name : str
            The name of the material model.
        independent_parameters : list[IndependentParameter]
            List of independent parameters for the model.
        dependent_parameters : list[DependentParameter]
            List of dependent parameters for the model.
        """
        self._name = name
        self.independent_parameters = independent_parameters
        self.interpolation_options = interpolation_options
        self.definition = definition
        self.localized_name = localized_name
        self.source = source
        self.type = type

    @property
    def name(self) -> str:
        """Name of the quantity modeled by the constant."""
        return self._name
