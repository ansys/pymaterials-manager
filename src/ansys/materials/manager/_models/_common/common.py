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

from enum import Enum

from pydantic.fields import FieldInfo

from .model_qualifier import ModelQualifier


class QualifierType(str, Enum):
    """Enum for qualifier types in material models."""

    STRICT = "strict"
    RANGE = "range"
    FREE = "free"


class ParameterFieldInfo(FieldInfo):
    """FieldInfo for dependent parameters in material models."""

    def __init__(self, *, matml_name=None, **kwargs):
        """Initialize the ParameterFieldInfo with a matml_name."""
        super().__init__(**kwargs)
        if self.title is None:
            self.title = matml_name
        self.matml_name = matml_name


def ParameterField(*, matml_name=None, **kwargs):
    """Create a ParameterField with a specific matml_name."""
    return ParameterFieldInfo(matml_name=matml_name, **kwargs)


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
            missing_qualifiers.append(ModelQualifier(name=key, value=value))

    return missing_qualifiers + inputed_qualifiers
