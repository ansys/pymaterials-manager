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

"""Granta MI REST API session client.

Manages the full session lifecycle used by the Granta Material Picker:

1. Create a session (POST).
2. Return the browser URL so the caller can open the material picker.
3. Fetch selected material data (GET – blocks until a material is selected or the session times
   out, depending on server-side configuration).
4. Delete the session (DELETE).

Authentication is handled via an MSAL-style token response dict, identical to the pattern used
in ``SimpleExample.py``.

Example
-------
::

    import webbrowser
    from ansys.materials.manager.parsers.rest import RestSessionClient, RestMaterialReader

    with RestSessionClient(base_url="https://cloudserver.com") as client:
        webbrowser.open(client.granta_material_picker_url)
        raw_data = client.fetch_data()

    materials = RestMaterialReader(raw_data).convert_materials()
"""

import json
import logging
import time

import httpx

from ._exceptions import AuthenticationError, GrantaMIError

_logger = logging.getLogger(__name__)

_POLL_SECONDS: int = 50
"""
Server-side long-poll duration in seconds.

Advertised to the server via ``pollSeconds`` in the session creation payload. The server holds
the GET ``/data`` connection open for up to this many seconds, then returns ``204 No Content`` if
no material has been selected yet. The client re-issues the request on each ``204`` response.
"""

_POLL_REQUEST_TIMEOUT: float = _POLL_SECONDS + 10.0
"""
Per-request HTTP timeout for the polling GET.

Slightly above ``_POLL_SECONDS`` to allow for connection overheads.
"""

_TIMEOUT_ERROR_MSG = (
    "Timed out after {timeout:.0f}s waiting for a material selection. The material picker may "
    "have been closed without making a selection, or the session timed out."
)


class RestSessionClient:
    """
    Client for the Granta MI material-picker REST API session lifecycle.

    Parameters
    ----------
    base_url : str
        Base URL for the REST API, e.g. ``"https://cloudserver.com/is"``.
    verify_ssl : bool
        Whether to verify SSL certificates.  Defaults to ``True``.
    oidc_config : MSALOIDCConfiguration | None
        OIDC configuration used to authenticate with the identity provider.
        When ``None`` (default), the configuration is resolved automatically from ``base_url``
        using :func:`~ansys.materials.manager.parsers.rest._grantami_auth.get_oidc_config_for_url`.
        A :class:`ValueError` is raised at construction time if ``base_url`` is not a recognized
        Granta MI deployment and no explicit config is supplied.
    """

    def __init__(
        self,
        base_url: str,
        verify_ssl: bool = True,
        oidc_config=None,
    ) -> None:
        """Initialize the REST session client."""
        from ._grantami_auth import get_oidc_config_for_url

        self._base_url = base_url.rstrip("/")
        self._oidc_config = (
            oidc_config if oidc_config is not None else get_oidc_config_for_url(base_url)
        )
        auth_token = self._authenticate_hosted_granta_mi()
        auth_header = {"Authorization": f"Bearer {auth_token}"}
        self._client = httpx.Client(headers=auth_header, verify=verify_ssl)
        self._session_id: str | None = None

    def _authenticate_hosted_granta_mi(self) -> str:
        _logger.info("Authenticating with Granta MI at %s…", self._base_url)
        token_response = self._oidc_config.authenticate()
        if "access_token" not in token_response:
            raise AuthenticationError("Response did not contain 'access_token'")
        _logger.debug("Access token acquired successfully.")
        return token_response["access_token"]

    def create_session(self, name: str = "PyMaterials Manager") -> None:
        """
        Create a new Granta MI material-picker session.

        Parameters
        ----------
        name : str
            Human-readable session name displayed in the material picker.

        Raises
        ------
        ValueError
            If a session has already been created on this client instance.
        httpx.HTTPStatusError
            If the server returns a non-2xx status code.
        """
        if self._session_id is not None:
            raise ValueError(
                "A session already exists on this client. "
                "Call delete_session() first or use a new RestSessionClient instance."
            )
        endpoint = f"{self._base_url}/is/api/v1/sessions/"
        payload = {
            "name": name,
            "settings": {
                "title": name,
                "packageName": "Workbench",
                "pollSeconds": _POLL_SECONDS,
            },
        }
        _logger.info("Creating Granta MI session '%s' at %s", name, endpoint)
        _logger.debug("Session creation payload: %s", payload)
        response = self._client.post(endpoint, json=payload)
        response.raise_for_status()
        session_data = response.json()
        if "id" not in session_data:
            raise GrantaMIError(
                "Response from Granta MI Integration Service did not contain session id."
            )
        self._session_id = session_data["id"]
        _logger.info("Session created with ID: %s", self._session_id)

    @property
    def granta_material_picker_url(self) -> str:
        """
        Return the URL that should be opened in the user's browser.

        Returns
        -------
        str
            Full URL for the Granta Material Picker web interface.

        Raises
        ------
        ValueError
            If the session has not been initialized.
        """
        if self._session_id is None:
            raise ValueError("Session has not been initialized.")
        return f"{self._base_url}/grantami/#/granta-material-picker?sessionId={self._session_id}"

    def fetch_data(self, timeout: float = 300.0) -> dict:
        """
        Retrieve material data for the session, polling until a selection is made.

        The server returns a 204 response while the user is browsing the material picker
        (up to ``_POLL_SECONDS`` seconds per request). This method re-issues the GET on each
        204 response until either a 200 response is received or the client-side ``timeout``
        is reached.

        Parameters
        ----------
        timeout : float
            Total time in seconds to wait for a material selection before raising
            :class:`~ansys.materials.manager.parsers.rest._exceptions.GrantaMIError`.
            Defaults to 300 seconds (5 minutes).

        Returns
        -------
        dict
            The parsed JSON response from the server.

        Raises
        ------
        GrantaMIError
            If the polling loop times out without receiving a material selection, or if
            the response cannot be parsed.
        httpx.HTTPStatusError
            If the server returns a non-2xx, non-204 status code.
        ValueError
            If the session has not been initialized.
        """
        if self._session_id is None:
            raise ValueError("Session has not been initialized.")
        endpoint = f"{self._base_url}/is/api/v1/sessions/{self._session_id}/data"
        _logger.info(
            "Waiting for material selection in session %s (timeout=%.0fs)...",
            self._session_id,
            timeout,
        )
        deadline = time.monotonic() + timeout
        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise GrantaMIError(_TIMEOUT_ERROR_MSG.format(timeout=timeout))
            request_timeout = min(_POLL_REQUEST_TIMEOUT, remaining)
            try:
                response = self._client.get(endpoint, timeout=request_timeout)
            except httpx.ReadTimeout:
                raise GrantaMIError(_TIMEOUT_ERROR_MSG.format(timeout=timeout))
            response.raise_for_status()
            if response.status_code != 204:
                _logger.debug("Raw response body: %s", response.text)
                _logger.info("Received material data response (%d bytes).", len(response.content))
                try:
                    return response.json()
                except json.JSONDecodeError as exc:
                    raise GrantaMIError(
                        "The server returned a 200 response that could not be parsed as JSON."
                    ) from exc
            _logger.debug("No material selected yet (HTTP 204), re-polling...")

    def delete_session(self) -> None:
        """
        Delete a session on the server.

        Raises
        ------
        httpx.HTTPStatusError
            If the server returns a non-2xx status code.
        ValueError
            If the session has not been initialized.
        """
        if self._session_id is None:
            raise ValueError("Session has not been initialized.")
        endpoint = f"{self._base_url}/is/api/v1/sessions/{self._session_id}"
        session_id = self._session_id
        self._session_id = None
        _logger.info("Deleting Granta MI session %s.", session_id)
        response = self._client.delete(endpoint)
        response.raise_for_status()
        _logger.debug("Session %s deleted successfully.", session_id)

    def __enter__(self) -> "RestSessionClient":
        """Enter the context manager."""
        try:
            self.create_session()
            return self
        except Exception:
            self._client.close()
            raise

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit the context manager, cleaning up any active session and closing the HTTP client."""
        try:
            if self._session_id is not None:
                self.delete_session()
        finally:
            self._client.close()
