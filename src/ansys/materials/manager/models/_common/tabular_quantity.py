# Copyright (C) 2022 - 2026 ANSYS, Inc. and/or its affiliates.
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

from ansys.units import Quantity
import numpy as np
from pydantic import BaseModel, Field, model_validator

from .independent_parameter import IndependentParameter


class TabularQuantity(BaseModel):
    """
    A quantity defined over one or more independent parameter grids.

    Unlike a plain :class:`~ansys.units.Quantity`, a ``TabularQuantity`` bundles
    its dependent values together with the independent parameter values (e.g.
    temperature) they were sampled at. This allows multiple properties on the same
    :class:`~ansys.materials.manager.models._common.material_model.MaterialModel`
    to carry different grids without ambiguity.
    """

    values: Quantity = Field(..., description="Dependent variable values.")
    independent_parameters: list[IndependentParameter] = Field(
        default_factory=list,
        description="Independent parameters (e.g. temperature) for these values.",
    )

    @model_validator(mode="after")
    def _check_lengths(self):
        # Quantity.value is a raw float for scalar quantities, not an array.
        # np.atleast_1d normalises both cases so len() always works.
        n_values = len(np.atleast_1d(self.values.value))
        for independent_parameter in self.independent_parameters:
            if independent_parameter.values is not None:
                n_ip = len(np.atleast_1d(independent_parameter.values.value))
                if n_ip != n_values:
                    raise ValueError(
                        f"Independent parameter '{independent_parameter.name}' has "
                        f"{n_ip} values but dependent quantity has {n_values}."
                    )
        return self

    def __repr__(self) -> str:
        """Return an unambiguous string representation."""
        ip_reprs = ", ".join(repr(ip) for ip in self.independent_parameters)
        return f"TabularQuantity(values={self.values!r}, independent_parameters=[{ip_reprs}])"

    @property
    def value(self):
        """Convenience accessor mirroring :attr:`ansys.units.Quantity.value`."""
        return self.values.value

    @property
    def unit(self):
        """Convenience accessor mirroring :attr:`ansys.units.Quantity.unit`."""
        return self.values.unit
