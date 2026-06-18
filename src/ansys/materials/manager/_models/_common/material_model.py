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

import abc

from ansys.units import Quantity
import numpy as np
from pydantic import BaseModel, Field

from ._packages import SupportedPackage  # noqa: F401
from .common import validate_parameters
from .independent_parameter import IndependentParameter
from .interpolation_options import InterpolationOptions
from .model_qualifier import ModelQualifier
from .tabular_quantity import TabularQuantity


class MaterialModel(BaseModel, abc.ABC):
    """A base class for representing a material model."""

    name: str = Field(default="", title="Name", description="The name of the material model.")
    supported_packages: list[SupportedPackage] = Field(
        default=[],
        title="Supported Packages",
        description="The supported packages for this material model. Currently, only PyMAPDL and PyFluent are supported.",  # noqa: E501
        frozen=True,
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
    model_qualifiers: list[ModelQualifier] = Field(
        default=[],
        title="Model Qualifier",
        description="List of qualifiers for the model. This is used to determine the type of model and its applicability.",  # noqa: E501
        frozen=True,
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
        return cls(**value)

    def validate_model(self) -> None:
        """
        Perform pre-flight validation of the model setup.

        This method should not perform any calls to other processes.
        """
        model = self.model_dump()
        for field_name, field_value in model.items():
            if field_name in MaterialModel.model_fields.keys():
                continue
            actual_value = getattr(self, field_name)
            if isinstance(actual_value, TabularQuantity):
                continue
            if field_value is None:
                raise Exception(f"the value of {field_name} cannot be None, please update it.")
            validate_parameters(field_name, field_value["value"], self.independent_parameters)

    def flatten_parameter_grids(self, atol: float = 1e-6) -> "MaterialModel":
        """
        Return a copy of this model with a single set of parameter values.

        Finds all :class:`~.TabularQuantity` fields, validates that they all carry the same
        set of independent parameter names, then computes the row-wise intersection of their
        grids and returns a new model instance where:

        * every :class:`~.TabularQuantity` field is replaced by a plain
          :class:`~ansys.units.Quantity` containing only the dependent values at the common
          grid points, and
        * :attr:`independent_parameters` is set to the shared
          :class:`~.IndependentParameter` list covering the common grid.

        Parameters
        ----------
        atol : float, optional
            Absolute tolerance for float comparisons. Defaults to ``1e-6``.

        Returns
        -------
        MaterialModel
            A new instance of the same model class. If no :class:`~.TabularQuantity`
            fields are present, a plain copy of the model is returned unchanged.

        Raises
        ------
        ValueError
            If the :class:`~.TabularQuantity` fields do not all carry the same set of
            independent parameter names.
        ValueError
            If the :class:`~.TabularQuantity` fields have completely disjoint grids with
            no common points.
        """
        tabular_fields: dict[str, TabularQuantity] = {
            name: getattr(self, name)
            for name in self.__class__.model_fields
            if isinstance(getattr(self, name, None), TabularQuantity)
        }

        if not tabular_fields:
            return self.model_copy()

        # --- validate that all fields share the same independent parameter names ---
        ip_name_sets = {
            label: tuple(ip.name for ip in tq.independent_parameters)
            for label, tq in tabular_fields.items()
        }
        reference_names = next(iter(ip_name_sets.values()))
        mismatched = {
            label: names for label, names in ip_name_sets.items() if names != reference_names
        }
        if mismatched:
            differences = ", ".join(f"'{k}': {list(v)}" for k, v in mismatched.items())
            raise ValueError(
                "All TabularQuantity fields must have the same independent parameter names. "
                f"Expected {list(reference_names)} (from '{next(iter(ip_name_sets))}'), "
                f"but found differences: {differences}"
            )

        # --- for each independent parameter, find the common values across all fields ---
        # Represent each row as a tuple of rounded IP values; intersect across all fields.
        def _round_to_atol(val: float) -> float:
            return round(val / atol) * atol

        # Build per-field row sets: each row is a tuple of rounded values across all IPs.
        field_rows: dict[str, list[tuple]] = {}
        for label, tq in tabular_fields.items():
            ip_arrays = [
                np.asarray(ip.values.value, dtype=float)
                for ip in tq.independent_parameters
                if ip.values is not None
            ]
            if not ip_arrays:
                n = len(np.asarray(tq.values.value, dtype=float))
                field_rows[label] = [() for _ in range(n)]
            else:
                field_rows[label] = [
                    tuple(_round_to_atol(ip_arrays[d][i]) for d in range(len(ip_arrays)))
                    for i in range(len(ip_arrays[0]))
                ]

        # Intersect: keep rows that appear in all fields, preserving order from first field.
        first_label = next(iter(field_rows))
        canonical_rows = [
            row
            for row in field_rows[first_label]
            if all(row in set(field_rows[lbl]) for lbl in field_rows)
        ]

        if not canonical_rows:
            raise ValueError(
                f"Cannot flatten parameter grids for {self.__class__.__name__}: "
                "the TabularQuantity fields have completely disjoint grids with no common points."
            )

        canonical_row_set = set(canonical_rows)

        # --- demote each TabularQuantity to a plain Quantity at the common rows ---
        # For each field, build a mapping from row-tuple → dependent value.
        # This ensures values are extracted in canonical (first-field) order.
        updates: dict[str, object] = {}
        common_ip_values: list[np.ndarray] | None = None

        for label, tq in tabular_fields.items():
            dep_arr = np.asarray(tq.values.value, dtype=float)
            rows = field_rows[label]
            row_to_index = {row: i for i, row in enumerate(rows) if row in canonical_row_set}
            canonical_indices = [row_to_index[row] for row in canonical_rows]
            if label == first_label:
                common_ip_values = [
                    np.asarray(ip.values.value, dtype=float)[canonical_indices]
                    for ip in tq.independent_parameters
                    if ip.values is not None
                ]
            updates[label] = Quantity(
                [float(dep_arr[i]) for i in canonical_indices], tq.values.unit
            )

        # --- build the shared IndependentParameter list ---
        first_tq = next(iter(tabular_fields.values()))
        shared_ips = []
        for k, ip in enumerate(first_tq.independent_parameters):
            ip_vals = (
                common_ip_values[k] if common_ip_values and k < len(common_ip_values) else None
            )
            if ip_vals is not None and ip.values is not None:
                shared_ips.append(
                    ip.model_copy(update={"values": Quantity(list(ip_vals), ip.values.unit)})
                )
            else:
                shared_ips.append(ip)
        updates["independent_parameters"] = shared_ips

        return self.model_copy(update=updates)
