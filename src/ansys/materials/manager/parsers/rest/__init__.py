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

"""
REST-based visitor framework for populating material models from a Granta MI REST API.

Requires the ``grantami`` extra::

    pip install ansys-materials-manager[grantami]
"""

_MISSING: list[str] = []
try:
    import httpx  # noqa: F401
except ImportError:
    _MISSING.append("httpx")

try:
    import msal  # noqa: F401
except ImportError:
    _MISSING.append("msal")

if _MISSING:
    raise ImportError(
        f"The following packages are required to use the Granta MI REST visitor but are not "
        f"installed: {', '.join(_MISSING)}. "
        f"Install them with: pip install ansys-materials-manager[grantami]"
    )

from ansys.materials.manager.parsers.rest.rest_material_reader import (  # noqa: E402, F401
    RestMaterialReader,
)
from ansys.materials.manager.parsers.rest.rest_session_client import (  # noqa: E402, F401
    RestSessionClient,
)

__all__ = ["RestSessionClient", "RestMaterialReader"]
