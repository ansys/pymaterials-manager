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

from ansys.units import Quantity
from pydantic.fields import FieldInfo
from pydantic_core import core_schema

from ansys.materials.manager._models._common.model_qualifier import ModelQualifier


class QualifierType(str, Enum):
    """Enum for qualifier types in material models."""

    STRICT = "strict"
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
    found_values = []
    for inputed_qualifier in inputed_qualifiers:
        if inputed_qualifier.name in expected_values.keys():
            if expected_values[inputed_qualifier.name][1] == QualifierType.STRICT:
                if not inputed_qualifier.value == expected_values[inputed_qualifier.name][0]:
                    raise ValueError(
                        f"{inputed_qualifier.name} must be {expected_values[inputed_qualifier.name]}, "  # noqa: E501
                        f"but got {inputed_qualifier.value}."
                    )
            elif expected_values[inputed_qualifier.name][1] == QualifierType.FREE:
                if inputed_qualifier.value not in expected_values[inputed_qualifier.name][2]:
                    raise ValueError(
                        f"{inputed_qualifier.name} must be one of {expected_values[inputed_qualifier.name][2]}, "  # noqa: E501
                        f"but got {inputed_qualifier.value}."
                    )
            else:
                raise ValueError(
                    f"Unknown qualifier type: {expected_values[inputed_qualifier.name][1]}"
                )
            found_values.append(True)
        else:
            found_values.append(False)
    missing_qualifiers = []
    if not all(found_values):
        false_indices = [i for i, val in enumerate(found_values) if not val]
        expected_names = list(expected_values.keys())
        false_names = [expected_names[index] for index in false_indices if not found_values[index]]
        for false_name in false_names:
            missing_qualifiers.append(
                ModelQualifier(name=false_name, value=expected_values[false_name][0])
            )
    return missing_qualifiers + inputed_qualifiers


class QuantityWrapper(Quantity):
    """A wrapper for Quantity that allows for pydantic representation."""

    def __init__(self, value: list[float], units: str, **kwargs):
        """Initialize the QuantityWrapper."""
        super().__init__(value=value, units=units)
        self.extra_fields = kwargs

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        """Define the pydantic core schema for QuantityWrapper."""

        def validate_quantity_type(obj):
            if isinstance(obj, cls):
                return obj
            if isinstance(obj, Quantity):
                return cls(value=obj.value, b=obj.units)
            raise TypeError("Expected Quantity or QuantityWrapper instance.")

        def serialize(instance):
            base = {"value": instance.value, "units": instance.units.name}
            return {**base, **instance.extra_fields}

        return core_schema.no_info_plain_validator_function(
            validate_quantity_type,
            json_schema_input_schema=core_schema.model_fields_schema(
                {
                    "value": core_schema.list_schema(items_schema=core_schema.float_schema()),
                    "units": core_schema.str_schema(),
                },
                extras_schema=core_schema.any_schema(),
            ),
            serialization=core_schema.plain_serializer_function_ser_schema(
                serialize, return_schema=core_schema.dict_schema()
            ),
        )
