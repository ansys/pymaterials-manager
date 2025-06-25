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

from ansys.units import Quantity
from pydantic.fields import FieldInfo
from pydantic_core import core_schema


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
