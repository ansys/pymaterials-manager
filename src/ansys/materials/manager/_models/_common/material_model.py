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
import functools
import re

from ansys.units import Quantity
import numpy as np
from pydantic import BaseModel, Field

from ._packages import SupportedPackage  # noqa: F401
from .common import MATML_TO_GIL_ALGORITHM_MAPPING, Interpolator, validate_parameters
from .independent_parameter import IndependentParameter
from .interpolation_options import InterpolationOptions
from .model_qualifier import ModelQualifier
from .tabular_quantity import TabularQuantity

try:
    import ansys.dpf.core as dpf
    from ansys.dpf.core import load_library
    from ansys.tools.common.path import get_available_ansys_installations

    HAS_DPF = True
    HAS_GIL = True
    _ansys_paths = get_available_ansys_installations()
    HAS_MINIMUM_271 = any(version >= 271 for version in _ansys_paths)
    if HAS_MINIMUM_271:
        load_library("Ans.Dpf.Gil")  # codespell:ignore Ans

except ImportError:
    HAS_DPF = False
    HAS_MINIMUM_271 = False


def requires_dpf_271(func):
    """Check DPF and Ansys 2027 R1 (v271) availability.

    When a ``dpf_server`` keyword argument is supplied, the local Ansys
    installation version check is skipped and the GIL library is loaded
    against that server instead. A ``RuntimeError`` is still raised if
    the server version is older than 2027 R1 (v271).

    When no ``dpf_server`` is provided, both ``ansys-dpf-core`` and a
    local Ansys 2027 R1 (v271) or later installation are required.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        dpf_server = kwargs.get("dpf_server", None)
        if dpf_server is not None:
            if int(re.search(r"\b(20\d{2})\b", dpf_server.version).group(1)) >= 2027:
                load_library("Ans.Dpf.Gil", server=dpf_server)  # codespell:ignore Ans
            else:
                raise RuntimeError(
                    f"'{func.__name__}' requires Ansys 2027 R1 (v271) or later. "
                    "Please update your Ansys installation."
                )
            return func(*args, **kwargs)

        if not HAS_DPF:
            raise ImportError(
                f"'{func.__name__}' requires ansys-dpf-core. "
                "Install it with: pip install ansys-dpf-core"
            )
        if dpf_server is None and not HAS_MINIMUM_271:
            raise RuntimeError(
                f"'{func.__name__}' requires Ansys 2027 R1 (v271) or later. "
                "Please update your Ansys installation."
            )
        return func(*args, **kwargs)

    return wrapper


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
    interpolator: Interpolator = Field(
        default=Interpolator.GIL_INTERPOLATOR,
        title="Interpolator",
        description="The interpolation method to use for this material model. Currently, only GIL is supported.",  # noqa: E501
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

    def query(
        self, values: list[float] | list[list[float]], **kwargs
    ) -> list[float] | list[list[float]]:
        """
        Query the material model with the given values.

        Parameters
        ----------
        values: list[float] | list[list[float]]
            The values to query the material model with. This can be a list of lists
            for multiple independent parameters or a list of floats
            for a single independent parameter.

        Returns
        -------
        list[float] | list[list[float]]
            The result of the query. This will be a list of floats for a single
            independent parameter or a list of lists for multiple independent parameters.
        """
        self.validate_model()
        if self.interpolator == Interpolator.GIL_INTERPOLATOR:
            dpf_server = kwargs.get("dpf_server", None)
            return self._query_with_gil(values, dpf_server=dpf_server)
        else:
            raise NotImplementedError(f"Interpolator {self.interpolator} is not implemented yet.")

    @requires_dpf_271
    def _query_with_gil(
        self, values: list[float] | list[list[float]], dpf_server=None
    ) -> list[float] | list[list[float]]:
        """
        Query the material model using GIL interpolation.

        Parameters
        ----------
        values: list[float] | list[list[float]]
            The values to query the material model with. This can be a list of lists for multiple
            independent parameters or a list of floats for a single independent parameter.

            from ansys.dpf.core.server_types import (
            GrpcServer,
            InProcessServer,
            LegacyGrpcServer,
        )
        dpf_server: GrpcServer | InProcessServer | LegacyGrpcServer | None, optional
            The DPF server to use for the query.
            If not provided, the global DPF server will be used.
            servers can be imported from ansys.dpf.core.server_types.

        Returns
        -------
        list[float] | list[list[float]]
             The result of the query. This will be a list of floats for a single
             independent parameter or a list of lists for multiple independent parameters.
        """
        if self.independent_parameters is None:
            raise ValueError("Querying a material model with no independent parameters.")
        indep_param_dim = len(self.independent_parameters)
        if indep_param_dim == 0:
            raise ValueError("Querying a material model with no independent parameters.")

        if self.independent_parameters[0].values is None:
            raise ValueError(
                "Querying a material model with independent parameters that have no values."
            )
        indep_param_ent = len(self.independent_parameters[0].values.value)

        excluded_fields = set(MaterialModel.model_fields.keys())
        dependant_parameters = [
            field for field in self.__class__.model_fields.keys() if field not in excluded_fields
        ]

        dep_param_dim = len(dependant_parameters)
        if dep_param_dim == 0:
            raise ValueError("No dependent parameters found for this material model.")
        dep_param_ent = (
            len(getattr(self, dependant_parameters[0]).value) if dep_param_dim > 0 else None
        )
        if dep_param_ent is None:
            raise ValueError(
                "Querying a material model with dependent parameters that have no values."
            )

        indep_values = [
            self.independent_parameters[i].values.value.tolist() for i in range(indep_param_dim)
        ]
        indep_values = list(map(list, zip(*indep_values)))
        indep_param_field = dpf.fields_factory.create_vector_field(
            num_entities=indep_param_ent, num_comp=indep_param_dim
        )
        for i in range(indep_param_ent):
            indep_param_field.append(indep_values[i], i)

        dep_values = [
            getattr(self, dependant_parameters[i]).value.tolist() for i in range(dep_param_dim)
        ]
        dep_values = list(map(list, zip(*dep_values)))
        dep_param_field = dpf.fields_factory.create_vector_field(
            num_entities=dep_param_ent, num_comp=dep_param_dim
        )
        for i in range(dep_param_ent):
            dep_param_field.append(dep_values[i], i)

        defaults = [
            (
                [self.independent_parameters[i].default_value]
                if self.independent_parameters[i].default_value is not None
                else [0.0]
            )
            for i in range(indep_param_dim)
        ]

        min_max = [
            (
                [
                    self.independent_parameters[i].lower_limit,
                    self.independent_parameters[i].upper_limit,
                ]
                if self.independent_parameters[i].lower_limit is not None
                and self.independent_parameters[i].upper_limit is not None
                else [0.0, 1.0]
            )
            for i in range(indep_param_dim)
        ]

        ind_parameter_defaults = dpf.fields_factory.create_vector_field(
            num_entities=indep_param_dim, num_comp=1
        )
        ind_parameter_ranges = dpf.fields_factory.create_vector_field(
            num_entities=indep_param_dim, num_comp=2
        )
        for i in range(indep_param_dim):
            ind_parameter_defaults.append(defaults[i], i)
            ind_parameter_ranges.append(min_max[i], i)

        if not self.interpolation_options:
            raise ValueError("Querying a material model with no interpolation options.")

        algorithm = MATML_TO_GIL_ALGORITHM_MAPPING.get(
            self.interpolation_options.algorithm_type, None
        )

        if algorithm is None:
            raise ValueError("Querying a material model with no interpolation options algorithm.")

        is_cached = self.interpolation_options.cached
        is_normalized = self.interpolation_options.normalized
        # TODO need to adapt algorithm options
        algorithm_options = None
        gil_interpolator = dpf.Operator("gil::interpolation_operator")
        gil_interpolator.inputs.independent_parameters.connect(indep_param_field)
        gil_interpolator.inputs.independent_parameters_ranges.connect(ind_parameter_ranges)
        gil_interpolator.inputs.independent_parameters_defaults.connect(ind_parameter_defaults)
        gil_interpolator.inputs.dependent_parameters.connect(dep_param_field)
        gil_interpolator.inputs.algorithm.connect(algorithm)
        gil_interpolator.inputs.is_normalized.connect(is_normalized)
        gil_interpolator.inputs.is_cached.connect(is_cached)
        if algorithm_options:
            gil_interpolator.inputs.algorithm_options.connect(algorithm_options)

        gil_interpolator.run()
        status_info = gil_interpolator.outputs.status_info.get_data()
        status_info_dict = status_info.to_dict()
        print("GIL interpolation status info:", status_info_dict)
        interpolator_instance = gil_interpolator.outputs.interpolator.get_data()
        query = dpf.Operator("gil::query_interpolation_operator")
        query.inputs.interpolator.connect(interpolator_instance)
        evaluation_points = dpf.fields_factory.create_vector_field(
            num_entities=len(values), num_comp=indep_param_dim
        )
        for value_idx, value in enumerate(values):
            evaluation_points.append(value if isinstance(value, list) else [value], value_idx)
        query.inputs.evaluation_points.connect(evaluation_points)
        query.run()
        return query.outputs.evaluation.get_data().data

    def get_independent_parameter_by_name(self, name: str) -> IndependentParameter | None:
        """Get the independent parameter with a given name."""
        if self.independent_parameters is None:
            return None
        for ip in self.independent_parameters:
            if ip.name.lower() == name.lower():
                return ip
        return None
