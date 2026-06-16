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

# conftest.py for tests/rest/
# Stubs out optional heavy dependencies that may not be installed in all
# environments (e.g. ansys-dyna-core, ansys-mapdl-core, ansys-fluent-core).

import sys
import types
from unittest.mock import MagicMock, patch

import pytest


class _AutoModule(types.ModuleType):
    """A module that returns a MagicMock for any undefined attribute."""

    def __getattr__(self, name: str):
        value = MagicMock()
        setattr(self, name, value)
        return value


def _stub_leaf(name: str) -> None:
    """Insert an _AutoModule for *name* without touching the 'ansys' namespace."""
    parts = name.split(".")
    for i in range(1, len(parts) + 1):
        key = ".".join(parts[:i])
        if key == "ansys":
            continue
        if key not in sys.modules:
            mod = _AutoModule(key)
            mod.__spec__ = None
            mod.__path__ = []
            mod.__package__ = key
            sys.modules[key] = mod


for _mod in [
    "ansys.dyna.core.lib.keyword_base",
    "ansys.dyna.core.lib",
    "ansys.dyna.core",
    "ansys.dyna",
    "ansys.mapdl.core.mapdl",
    "ansys.mapdl.core",
    "ansys.mapdl",
    "ansys.fluent.core",
    "ansys.fluent",
    "coolprop",
]:
    _stub_leaf(_mod)


_AUTH_PATH = (
    "ansys.materials.manager.parsers.rest.rest_session_client."
    "RestSessionClient._authenticate_hosted_granta_mi"
)


@pytest.fixture
def mock_auth():
    """Patch MSAL authentication so no real identity-provider call is made."""
    with patch(_AUTH_PATH, return_value="test-token") as mock:
        yield mock
