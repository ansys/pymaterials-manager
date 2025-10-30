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

from dataclasses import dataclass
from typing import Any, Callable, Optional

from ansys.materials.manager._models._common.model_qualifier import ModelQualifier


@dataclass
class ModelInfo:
    """Model Info class."""

    labels: Optional[list[str] | list[list[str]]] = None
    attributes: Optional[list[str]] = None
    method: Optional[Callable[..., Any]] = None


def normalize_key(classes: tuple[type]) -> tuple[type]:
    """Normalize the mat card registry key."""
    return tuple(sorted(classes, key=lambda cls: cls.__name__))


def get_model_attributes(model):
    """Get model attributes."""
    return [
        a
        for a in dir(model)
        if not callable(getattr(model, a)) and not a.startswith("__") and not a.startswith("_")
    ]


def get_name_idx(qualifiers: list[ModelQualifier]) -> int:
    """Get name index."""
    for qualfier in qualifiers:
        if qualfier.name == "Definition":
            if qualfier.value == "Instantaneous":
                return 0
        else:
            return 1
