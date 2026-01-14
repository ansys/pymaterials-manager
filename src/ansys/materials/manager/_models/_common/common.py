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

from enum import Enum

import numpy as np

from .independent_parameter import IndependentParameter
from .model_qualifier import ModelQualifier


class QualifierType(str, Enum):
    """Enum for qualifier types in material models."""

    STRICT = "strict"
    RANGE = "range"
    FREE = "free"


def validate_and_initialize_model_qualifiers(
    values: dict, expected_values: dict
) -> list[ModelQualifier]:
    """Validate and initialize model qualifiers based on expected values."""
    if "model_qualifiers" in values:
        inputed_qualifiers = values["model_qualifiers"]
    else:
        inputed_qualifiers = []
    if len(inputed_qualifiers) == 0:
        for key, value in expected_values.items():
            inputed_qualifiers.append(ModelQualifier(name=key, value=value[0]))
        return inputed_qualifiers

    qualifier_dict = {}
    for qualifier in values["model_qualifiers"]:
        if isinstance(qualifier, dict):
            qualifier_dict[qualifier["name"]] = qualifier["value"]
        else:
            qualifier_dict[qualifier.name] = qualifier.value

    missing_qualifiers = []

    for key, value in expected_values.items():
        if key in qualifier_dict.keys():
            if value[1] == QualifierType.STRICT:
                if not qualifier_dict[key] == value[0]:
                    raise ValueError(
                        f"{key} must be {value[0]}, "  # noqa: E501
                        f"but got {qualifier_dict[key]}."
                    )
            elif value[1] == QualifierType.RANGE:
                if not qualifier_dict[key] in value[2]:
                    raise ValueError(
                        f"{key} must be one of {value[2]}, "  # noqa: E501
                        f"but got {qualifier_dict[key]}."
                    )
            elif value[1] == QualifierType.FREE:
                pass
            else:
                raise ValueError(f"Unknown qualifier type: {value[1]}")
        else:
            missing_qualifiers.append(ModelQualifier(name=key, value=value[0]))

    return missing_qualifiers + inputed_qualifiers


def is_variable(value):
    """Check if variable."""
    if isinstance(value, (float, int)):
        return False
    if isinstance(value, np.ndarray):
        if len(value) < 1:
            return False
    return True


def validate_parameters(
    dependent_name: str,
    dependent_quantity: float | int | np.ndarray,
    independent_parameters: list[IndependentParameter] | None,
) -> None:
    """Validate the parameters."""
    if is_variable(dependent_quantity):
        if len(dependent_quantity) == 0:
            raise Exception(f"{dependent_name} has no values.")
        if len(dependent_quantity) > 1:
            if independent_parameters is None:
                raise Exception(
                    f"{dependent_name} is variable but no independent parameters have been defined."
                )
            if len(independent_parameters) == 0:
                raise Exception(
                    f"{dependent_name} is variable but no independent parameters have been defined."
                )
            n_dep_param = len(dependent_quantity)
            for independent_parameter in independent_parameters:
                if is_variable(independent_parameter.values.value):
                    if len(independent_parameter.values.value) != n_dep_param:
                        raise Exception(
                            f"The number independent parameters {independent_parameter.name} and dependent parameters {dependent_name} do not match."  # noqa: E501
                        )
                else:
                    if n_dep_param != 1:
                        raise Exception(
                            f"The number independent parameters {independent_parameter.name} and dependent parameters {dependent_name} do not match."  # noqa: E501
                        )
        if len(dependent_quantity) == 1 and not independent_parameters is None:
            for independent_parameter in independent_parameters:
                if is_variable(independent_parameter.values.value):
                    if len(independent_parameter.values.value) != 1:
                        raise Exception(
                            f"The number independent parameters {independent_parameter.name} and dependent parameters {dependent_name} do not match."  # noqa: E501
                        )
    else:
        if independent_parameters:
            for independent_parameter in independent_parameters:
                if isinstance(independent_parameter.values.value, np.ndarray):
                    if len(independent_parameter.values.value) != 1:
                        raise Exception(
                            f"The number independent parameters {independent_parameter.name} and dependent parameters {dependent_name} do not match."  # noqa: E501
                        )
