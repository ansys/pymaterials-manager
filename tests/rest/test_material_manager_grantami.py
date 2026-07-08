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


from unittest.mock import MagicMock, patch

import pytest

from ansys.materials.manager import MaterialManager
from ansys.materials.manager.models import Material

GRANTA_MI_URL = "https://grantamaterials.ansys.com"
_SESSIONS_URL = f"{GRANTA_MI_URL}/is/api/v1/sessions/"
_SESSION_ID = "session-test"
_DATA_URL = f"{GRANTA_MI_URL}/is/api/v1/sessions/{_SESSION_ID}/data"
_DELETE_URL = f"{GRANTA_MI_URL}/is/api/v1/sessions/{_SESSION_ID}"

_RAW_DATA = {"materials": [{"materialName": "Steel", "materialId": "mat-1", "models": []}]}
_MATERIAL_DICT = {"Steel": Material(name="Steel", material_id="mat-1")}

_READER_PATH = "ansys.materials.manager.integrations.rest.rest_material_reader.RestMaterialReader"


@pytest.fixture
def mock_reader():
    """Stub RestMaterialReader so no real JSON parsing occurs."""
    mock_cls = MagicMock()
    mock_instance = MagicMock()
    mock_cls.return_value = mock_instance
    mock_instance.convert_materials.return_value = _MATERIAL_DICT
    with patch(_READER_PATH, mock_cls):
        yield mock_instance


@pytest.fixture
def grantami_httpx(httpx_mock):
    """Register the standard three Granta MI session lifecycle responses."""
    httpx_mock.add_response(method="POST", url=_SESSIONS_URL, json={"id": _SESSION_ID})
    httpx_mock.add_response(method="GET", url=_DATA_URL, json=_RAW_DATA)
    httpx_mock.add_response(method="DELETE", url=_DELETE_URL, status_code=204)
    return httpx_mock


def test_from_grantami_returns_material_manager(grantami_httpx, mock_reader, mock_auth):
    """from_grantami should return a MaterialManager instance."""
    with patch("webbrowser.open"):
        manager = MaterialManager.from_grantami(granta_mi_url=GRANTA_MI_URL)

    assert isinstance(manager, MaterialManager)


def test_from_grantami_populates_materials(grantami_httpx, mock_reader, mock_auth):
    """from_grantami should populate the manager's material library."""
    with patch("webbrowser.open"):
        manager = MaterialManager.from_grantami(granta_mi_url=GRANTA_MI_URL)

    assert "Steel" in manager.materials


def test_from_grantami_opens_browser(grantami_httpx, mock_reader, mock_auth):
    """from_grantami should open the browser with a URL containing the base server address."""
    with patch("webbrowser.open") as mock_browser:
        MaterialManager.from_grantami(granta_mi_url=GRANTA_MI_URL)

    mock_browser.assert_called_once()
    url = mock_browser.call_args.args[0]
    assert GRANTA_MI_URL in url


def test_read_from_grantami_adds_to_existing_library(grantami_httpx, mock_reader, mock_auth):
    """read_from_grantami should merge materials into an existing library."""
    existing = Material(name="Aluminium", material_id="al-1")
    manager = MaterialManager()
    manager._materials = {"Aluminium": existing}

    with patch("webbrowser.open"):
        manager.read_from_grantami(granta_mi_url=GRANTA_MI_URL)

    assert "Aluminium" in manager.materials
    assert "Steel" in manager.materials


def test_read_from_grantami_returns_none(grantami_httpx, mock_reader, mock_auth):
    """read_from_grantami should return None (adds to library in place)."""
    manager = MaterialManager()
    with patch("webbrowser.open"):
        result = manager.read_from_grantami(granta_mi_url=GRANTA_MI_URL)

    assert result is None
