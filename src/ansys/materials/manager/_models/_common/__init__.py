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

try:
    from ansys.mapdl.core.mapdl import MapdlBase as _MapdlCore
except ImportError:
    try:
        from ansys.mapdl.core.mapdl import _MapdlCore
    except ImportError:
        _MapdlCore = type(None)

try:
    from ansys.fluent.core.session_solver import Solver as _FluentCore
except ImportError:
    _FluentCore = type(None)

from ._packages import SupportedPackage
from .common import (
    QualifierType,
    validate_and_initialize_model_qualifiers,
    validate_parameters,
)
from .independent_parameter import IndependentParameter
from .interpolation_options import InterpolationOptions
from .material_model import MaterialModel
from .model_qualifier import ModelQualifier
from .user_parameter import UserParameter
