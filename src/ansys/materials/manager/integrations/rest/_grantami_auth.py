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

"""MSAL OIDC authentication for the Granta MI REST API.

:class:`MSALOIDCConfiguration` is the abstract base that carries OIDC credentials as class
attributes and implements the interactive browser authentication flow.  Concrete subclasses
supply the identity-provider-specific constants.

Two pre-built configurations are provided:

* :class:`AnsysIDProduction` — Ansys ID production environment.
* :class:`AnsysIDDevelopment` — Ansys ID development / staging environment.
"""

from abc import ABC
import logging
from typing import ClassVar

import msal

from ._exceptions import AuthenticationError

_logger = logging.getLogger(__name__)


class MSALOIDCConfiguration(ABC):
    """
    Abstract OIDC configuration for MSAL public-client authentication.

    Subclasses must define three class attributes that identify the identity provider:

    * ``client_id``: MSAL public-client application ID.
    * ``authority``: MSAL authority URL.
    * ``scope``: OAuth2 scope string to request.

    The optional ``port`` class attribute controls the local redirect port used during the
    interactive browser flow and defaults to ``32284``.

    The concrete :meth:`authenticate` method uses these attributes to run the interactive
    acquisition flow and returns the raw MSAL token response dict.
    """

    client_id: ClassVar[str]
    authority: ClassVar[str]
    scope: ClassVar[str]
    _REQUIRED_CLASS_ATTRS: ClassVar[tuple[str, ...]] = ("client_id", "authority", "scope")

    def __init_subclass__(cls, **kwargs: object) -> None:
        """
        Enforce that all required class attributes are defined on concrete subclasses.

        Checks that
        ``client_id``, ``authority``, and ``scope`` are all present somewhere in the subclass's
        MRO (excluding :class:`MSALOIDCConfiguration` itself, which only annotates them).

        Raises
        ------
        TypeError
            If any required attribute is absent, naming both the offending class and the
            missing attributes.
        """
        super().__init_subclass__(**kwargs)
        missing = [
            attr
            for attr in MSALOIDCConfiguration._REQUIRED_CLASS_ATTRS
            if not any(
                attr in base.__dict__
                for base in cls.__mro__
                if base not in (MSALOIDCConfiguration, ABC, object)
            )
        ]
        if missing:
            raise TypeError(
                f"{cls.__name__!r} must define class attribute(s): {', '.join(missing)}"
            )

    port: ClassVar[int] = 32284

    def authenticate(self) -> dict:
        """
        Acquire a token interactively using the system browser.

        Opens the default browser to the identity provider login page.  The call
        blocks until the user completes authentication or closes the window.

        Returns
        -------
        dict
            MSAL token response dict containing at minimum an ``"access_token"`` key.

        Raises
        ------
        AuthenticationError
            If authentication fails or the response contains an ``"error"`` key.
        """
        _logger.debug(
            "Initializing MSAL public client application (client_id=%s, authority=%s)",
            self.client_id,
            self.authority,
        )
        app = msal.PublicClientApplication(self.client_id, authority=self.authority)

        _logger.info(
            "Opening browser for Ansys ID authentication (scope=%s, port=%d)…",
            self.scope,
            self.port,
        )
        token_response = app.acquire_token_interactive(scopes=[self.scope], port=self.port)

        if "error" in token_response:
            _logger.error(
                "Authentication failed: %s - %s",
                token_response.get("error"),
                token_response.get("error_description", ""),
            )
            raise AuthenticationError(
                f"Authentication failed: {token_response.get('error')} - "
                f"{token_response.get('error_description', '')}"
            )

        _logger.info("Authentication successful.")
        _logger.debug("Token response keys: %s", list(token_response.keys()))
        return token_response


class AnsysIDProduction(MSALOIDCConfiguration):
    """OIDC configuration targeting the Ansys ID production environment."""

    client_id: ClassVar[str] = "28982bbf-f354-4e48-8bfb-e542d44c588c"
    authority: ClassVar[str] = (
        "https://ansysaccount.b2clogin.com/ansysaccount.onmicrosoft.com/"
        "B2C_1A_ANSYSID_SIGNUP_SIGNIN"
    )
    scope: ClassVar[str] = "https://ansysaccount.onmicrosoft.com/AnsysID/Authentication"


class AnsysIDDevelopment(MSALOIDCConfiguration):
    """OIDC configuration targeting the Ansys ID development / staging environment."""

    client_id: ClassVar[str] = "63377600-f6ce-4c19-9c0e-a7278d7bde8c"
    authority: ClassVar[str] = (
        "https://a365dev.b2clogin.com/a365dev.onmicrosoft.com/B2C_1A_ANSYSID_SIGNUP_SIGNIN"
    )
    scope: ClassVar[str] = "https://a365dev.onmicrosoft.com/AnsysID/Authentication"


_URL_CONFIG_MAP: dict[str, type[MSALOIDCConfiguration]] = {
    "https://grantamaterials.ansys.com".casefold(): AnsysIDProduction,
    "https://test-grantami.awsansys7np.onscale.com".casefold(): AnsysIDDevelopment,
}


def get_oidc_config_for_url(url: str) -> MSALOIDCConfiguration:
    """
    Return the appropriate :class:`MSALOIDCConfiguration` instance for ``url``.

    The URL is normalised before lookup.

    Parameters
    ----------
    url : str
        Base URL of the Granta MI instance.

    Returns
    -------
    MSALOIDCConfiguration
        An instance of the matching configuration class.

    Raises
    ------
    ValueError
        If ``url`` does not match any known Granta MI deployment.
    """
    normalised = url.rstrip("/").casefold()
    config_class = _URL_CONFIG_MAP.get(normalised)
    if config_class is None:
        known = ", ".join(f'"{u}"' for u in _URL_CONFIG_MAP)
        raise ValueError(
            f"No default OIDC configuration is registered for {url!r}. "
            f"Known URLs: {known}. "
            f"Pass an explicit 'oidc_config' to use a custom configuration."
        )
    _logger.debug("Resolved OIDC config for %r → %s.", url, config_class.__name__)
    return config_class()
