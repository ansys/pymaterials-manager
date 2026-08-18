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

import json
from unittest.mock import patch

import httpx
import pytest

from ansys.materials.manager.integrations.rest.rest_session_client import (
    AuthenticationError,
    GrantaMIError,
    RestSessionClient,
)

BASE_URL = "https://grantamaterials.ansys.com"
_SESSIONS_URL = f"{BASE_URL}/is/api/v1/sessions/"


def test_create_session_posts_and_stores_id(httpx_mock, mock_auth):
    """create_session should POST to the sessions endpoint and store the returned ID."""
    httpx_mock.add_response(method="POST", url=_SESSIONS_URL, json={"id": "session-001"})

    client = RestSessionClient(BASE_URL)
    client.create_session()

    assert client._session_id == "session-001"


def test_create_session_raises_on_missing_id(httpx_mock, mock_auth):
    """create_session should raise GrantaMIError when the response lacks 'id'."""
    httpx_mock.add_response(method="POST", url=_SESSIONS_URL, json={})

    client = RestSessionClient(BASE_URL)
    with pytest.raises(GrantaMIError):
        client.create_session()


def test_create_session_raises_if_session_already_exists(httpx_mock, mock_auth):
    """create_session should raise ValueError if called twice on the same client."""
    httpx_mock.add_response(method="POST", url=_SESSIONS_URL, json={"id": "session-dup"})

    client = RestSessionClient(BASE_URL)
    client.create_session()

    with pytest.raises(ValueError, match="session already exists"):
        client.create_session()


def test_granta_material_picker_url_contains_session_id(httpx_mock, mock_auth):
    """granta_material_picker_url should embed the session ID and the base URL."""
    httpx_mock.add_response(method="POST", url=_SESSIONS_URL, json={"id": "my-session-xyz"})

    client = RestSessionClient(BASE_URL)
    client.create_session()

    url = client.granta_material_picker_url
    assert "my-session-xyz" in url
    assert url.startswith(BASE_URL)


def test_granta_material_picker_url_raises_without_session(mock_auth):
    """granta_material_picker_url should raise ValueError before create_session is called."""
    client = RestSessionClient(BASE_URL)
    with pytest.raises(ValueError):
        _ = client.granta_material_picker_url


def test_fetch_data_returns_json(httpx_mock, mock_auth):
    """fetch_data should return the parsed JSON dict when the server responds with 200."""
    expected = {"materials": [{"materialName": "Steel", "models": []}]}
    httpx_mock.add_response(method="POST", url=_SESSIONS_URL, json={"id": "session-003"})
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/is/api/v1/sessions/session-003/data",
        json=expected,
    )

    client = RestSessionClient(BASE_URL)
    client.create_session()
    result = client.fetch_data()

    assert result == expected


def test_fetch_data_raises_without_session(mock_auth):
    """fetch_data should raise ValueError when no session has been created."""
    client = RestSessionClient(BASE_URL)
    with pytest.raises(ValueError):
        client.fetch_data()


def test_fetch_data_polls_on_204_then_returns_data(httpx_mock, mock_auth):
    """fetch_data should re-issue the GET on 204 and return data when 200 arrives."""
    expected = {"materials": []}
    httpx_mock.add_response(method="POST", url=_SESSIONS_URL, json={"id": "session-poll"})
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/is/api/v1/sessions/session-poll/data",
        status_code=204,
    )
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/is/api/v1/sessions/session-poll/data",
        json=expected,
    )

    client = RestSessionClient(BASE_URL)
    client.create_session()
    result = client.fetch_data(timeout=300.0)

    assert result == expected


def test_fetch_data_raises_granta_mi_error_on_timeout(httpx_mock, mock_auth):
    """fetch_data should raise GrantaMIError immediately when timeout is already expired."""
    httpx_mock.add_response(method="POST", url=_SESSIONS_URL, json={"id": "session-timeout"})
    # No GET response registered: with timeout=0.0 the deadline check fires before the first
    # request, so no GET is issued.

    client = RestSessionClient(BASE_URL)
    client.create_session()

    with pytest.raises(GrantaMIError, match="Timed out"):
        client.fetch_data(timeout=0.0)


def test_fetch_data_polls_then_times_out(httpx_mock, mock_auth):
    """fetch_data should raise GrantaMIError after exhausting all polls within the timeout."""
    httpx_mock.add_response(method="POST", url=_SESSIONS_URL, json={"id": "session-poll-to"})
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/is/api/v1/sessions/session-poll-to/data",
        status_code=204,
    )

    client = RestSessionClient(BASE_URL)
    client.create_session()

    # Patch monotonic so first check passes (plenty of time), then second check (after the GET)
    # sees the deadline has expired.
    _times = iter([0.0, 0.0, 999.0])  # deadline=1.0; first remaining>0; second remaining<=0
    with patch(
        "ansys.materials.manager.integrations.rest.rest_session_client.time.monotonic",
        side_effect=_times,
    ):
        with pytest.raises(GrantaMIError, match="Timed out"):
            client.fetch_data(timeout=1.0)


def test_fetch_data_read_timeout_raises_granta_mi_error(httpx_mock, mock_auth):
    """fetch_data should convert httpx.ReadTimeout into GrantaMIError."""
    httpx_mock.add_response(method="POST", url=_SESSIONS_URL, json={"id": "session-rt"})
    httpx_mock.add_exception(
        httpx.ReadTimeout("timed out"),
        method="GET",
        url=f"{BASE_URL}/is/api/v1/sessions/session-rt/data",
    )

    client = RestSessionClient(BASE_URL)
    client.create_session()

    with pytest.raises(GrantaMIError, match="Timed out"):
        client.fetch_data(timeout=60.0)


def test_fetch_data_malformed_json_raises_granta_mi_error(httpx_mock, mock_auth):
    """fetch_data should convert JSONDecodeError on a 200 response into GrantaMIError."""
    httpx_mock.add_response(method="POST", url=_SESSIONS_URL, json={"id": "session-json"})
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/is/api/v1/sessions/session-json/data",
        status_code=200,
        content=b"not valid json {{{{",
    )

    client = RestSessionClient(BASE_URL)
    client.create_session()

    with pytest.raises(GrantaMIError, match="could not be parsed as JSON"):
        client.fetch_data(timeout=60.0)


def test_delete_session_calls_delete_and_clears_id(httpx_mock, mock_auth):
    """delete_session should call DELETE and clear the stored session ID."""
    httpx_mock.add_response(method="POST", url=_SESSIONS_URL, json={"id": "session-004"})
    httpx_mock.add_response(
        method="DELETE",
        url=f"{BASE_URL}/is/api/v1/sessions/session-004",
        status_code=204,
    )

    client = RestSessionClient(BASE_URL)
    client.create_session()
    client.delete_session()

    assert client._session_id is None


def test_context_manager_creates_and_deletes_session(httpx_mock, mock_auth):
    """__enter__ should call create_session; __exit__ should call delete_session."""
    httpx_mock.add_response(method="POST", url=_SESSIONS_URL, json={"id": "session-005"})
    httpx_mock.add_response(
        method="DELETE",
        url=f"{BASE_URL}/is/api/v1/sessions/session-005",
        status_code=204,
    )

    with RestSessionClient(BASE_URL) as client:
        assert client._session_id == "session-005"

    assert client._session_id is None


def test_context_manager_raises_when_session_creation_fails(httpx_mock, mock_auth):
    """Context manager should propagate network exceptions raised during session creation."""
    httpx_mock.add_exception(Exception("network error"), url=_SESSIONS_URL)

    with pytest.raises(Exception, match="network error"):
        with RestSessionClient(BASE_URL):
            pass  # pragma: no cover


def test_context_manager_closes_client_when_enter_raises(httpx_mock, mock_auth):
    """__enter__ should close the HTTP client even when create_session raises."""
    httpx_mock.add_exception(Exception("create failed"), url=_SESSIONS_URL)

    client = RestSessionClient.__new__(RestSessionClient)
    client._base_url = BASE_URL
    client._session_id = None
    client._package_name = None
    # Use a real httpx.Client so we can check is_closed
    import httpx as _httpx

    client._client = _httpx.Client()

    with pytest.raises(Exception, match="create failed"):
        client.__enter__()

    assert client._client.is_closed


def test_context_manager_closes_client_when_delete_raises(httpx_mock, mock_auth):
    """__exit__ should close the HTTP client even if delete_session raises."""
    httpx_mock.add_response(method="POST", url=_SESSIONS_URL, json={"id": "session-err"})
    httpx_mock.add_exception(
        Exception("delete failed"),
        method="DELETE",
        url=f"{BASE_URL}/is/api/v1/sessions/session-err",
    )

    client = RestSessionClient(BASE_URL)
    client.create_session()

    with pytest.raises(Exception, match="delete failed"):
        client.__exit__(None, None, None)

    assert client._client.is_closed
    assert client._session_id is None


def test_delete_session_clears_id_even_when_server_returns_error(httpx_mock, mock_auth):
    """delete_session should clear _session_id before the request so state is always consistent."""
    httpx_mock.add_response(method="POST", url=_SESSIONS_URL, json={"id": "session-del-err"})
    httpx_mock.add_response(
        method="DELETE",
        url=f"{BASE_URL}/is/api/v1/sessions/session-del-err",
        status_code=500,
    )

    client = RestSessionClient(BASE_URL)
    client.create_session()

    with pytest.raises(httpx.HTTPStatusError):
        client.delete_session()

    assert client._session_id is None


def test_create_session_without_package_omits_package_name(httpx_mock, mock_auth):
    """RestSessionClient with no package_name should not include packageName in the payload."""
    httpx_mock.add_response(method="POST", url=_SESSIONS_URL, json={"id": "session-no-pkg"})

    client = RestSessionClient(BASE_URL)
    client.create_session()

    request = httpx_mock.get_requests()[0]
    body = json.loads(request.content)
    assert "packageName" not in body["settings"]


def test_create_session_with_package_includes_package_name(httpx_mock, mock_auth):
    """RestSessionClient with package_name should include packageName in the payload."""
    httpx_mock.add_response(method="POST", url=_SESSIONS_URL, json={"id": "session-pkg"})

    client = RestSessionClient(BASE_URL, package_name="Workbench")
    client.create_session()

    request = httpx_mock.get_requests()[0]
    body = json.loads(request.content)
    assert body["settings"]["packageName"] == "Workbench"


def test_context_manager_uses_instance_package_name(httpx_mock, mock_auth):
    """The context manager should forward the instance package_name in the session payload."""
    httpx_mock.add_response(method="POST", url=_SESSIONS_URL, json={"id": "session-cm-pkg"})
    httpx_mock.add_response(
        method="DELETE",
        url=f"{BASE_URL}/is/api/v1/sessions/session-cm-pkg",
        status_code=204,
    )

    with RestSessionClient(BASE_URL, package_name="Workbench"):
        pass

    request = httpx_mock.get_requests()[0]
    body = json.loads(request.content)
    assert body["settings"]["packageName"] == "Workbench"

    """_authenticate_hosted_granta_mi should raise AuthenticationError on bad token response."""
    mock_auth.side_effect = AuthenticationError("no token")
    with pytest.raises(AuthenticationError):
        RestSessionClient(BASE_URL)
