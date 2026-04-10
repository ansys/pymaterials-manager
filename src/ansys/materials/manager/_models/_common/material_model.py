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

from pydantic import BaseModel, Field

from ._packages import SupportedPackage  # noqa: F401
from .common import MATML_TO_GIL_ALGORITHM_MAPPING, Interpolator, validate_parameters
from .independent_parameter import IndependentParameter
from .interpolation_options import InterpolationOptions
from .model_qualifier import ModelQualifier

try:
    import ansys.dpf.core as dpf
    from ansys.dpf.core import load_library
    from ansys.tools.path import get_available_ansys_installations

    HAS_DPF = True
    _ansys_paths = get_available_ansys_installations()
    if all(version >= 271 for version in _ansys_paths):
        load_library("Ans.Dpf.Gil")  # codespell:ignore Ans
        HAS_MINIMUM_271 = True
except ImportError:
    HAS_DPF = False
    HAS_MINIMUM_271 = False


def requires_dpf_271(func):
    """Check DPF and Ansys 2027 R1 (v271) availability."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not HAS_DPF:
            raise ImportError(
                f"'{func.__name__}' requires ansys-dpf-core. "
                "Install it with: pip install ansys-dpf-core"
            )
        if not HAS_MINIMUM_271:
            raise RuntimeError(
                f"'{func.__name__}' requires Ansys 2027 R1 (v271) or later. "
                "Please update your Ansys installation."
            )
        return func(*args, **kwargs)

    return wrapper


class MaterialModel(BaseModel, abc.ABC):
    """A base class for representing a material models."""

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
            if field_name not in MaterialModel.model_fields.keys():
                if field_value is None:
                    raise Exception(f"the value of {field_name} cannot be None, please update it.")
                validate_parameters(field_name, field_value["value"], self.independent_parameters)

    @requires_dpf_271
    def query(self, values: list[float] | list[list[float]]) -> list[float] | list[list[float]]:
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
            return self._query_with_gil(values)
        else:
            raise NotImplementedError(f"Interpolator {self.interpolator} is not implemented yet.")

    def _query_with_gil(
        self, values: list[float] | list[list[float]]
    ) -> list[float] | list[list[float]]:
        """
        Query the material model using GIL interpolation.

        Parameters
        ----------
        values: list[float] | list[list[float]]
            The values to query the material model with. This can be a list of lists for multiple
            independent parameters or a list of floats for a single independent parameter.

        Returns
        -------
        list[float] | list[list[float]]
             The result of the query. This will be a list of floats for a single
             independent parameter or a list of lists for multiple independent parameters.
        """
        indep_param_dim = (
            len(self.independent_parameters) if self.independent_parameters is not None else None
        )
        if self.independent_parameters is None:
            print("Querying a material model with no independent parameters.")
            return
        if indep_param_dim > 0:
            indep_param_dim = len(self.independent_parameters)
        if indep_param_dim == 0:
            print("Querying a material model with no independent parameters.")
            return
        indep_param_ent = len(self.independent_parameters[0].values.value)

        excluded_fields = list(MaterialModel.model_fields.keys())
        dependant_parameters = [
            field for field in self.__class__.model_fields.keys() if field not in excluded_fields
        ]
        dep_param_dim = len(dependant_parameters)
        if dep_param_dim == 0:
            print("Querying a material model with no dependent parameters.")
            return
        dep_param_ent = (
            len(getattr(self, dependant_parameters[0]).value) if dep_param_dim > 0 else None
        )
        if dep_param_ent is None:
            print("Querying a material model with dependent parameters that have no values.")
            return

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
            num_entities=1, num_comp=indep_param_dim
        )
        ind_parameter_ranges = dpf.fields_factory.create_vector_field(
            num_entities=indep_param_dim, num_comp=2
        )
        for i in range(indep_param_dim):
            ind_parameter_defaults.append(defaults[i], i)
            ind_parameter_ranges.append(min_max[i], i)

        if not self.interpolation_options:
            print("Querying a material model with no interpolation options")
            return

        algorithm = MATML_TO_GIL_ALGORITHM_MAPPING.get(
            self.interpolation_options.algorithm_type, None
        )

        if algorithm is None:
            print("Querying a material model with no interpolation options algorithm.")
            return
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
        for i in range(len(values)):
            evaluation_points.append(values[i] if isinstance(values[i], list) else [values[i]], i)
        query.inputs.evaluation_points.connect(evaluation_points)
        query.run()
        return query.outputs.evaluation.get_data().data
