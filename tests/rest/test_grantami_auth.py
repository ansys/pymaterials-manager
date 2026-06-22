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

import pytest

from ansys.materials.manager.parsers.rest._grantami_auth import (
    AnsysIDDevelopment,
    AnsysIDProduction,
    MSALOIDCConfiguration,
    get_oidc_config_for_url,
)


def test_subclass_missing_all_required_attrs_raises():
    """`TypeError` should be raised when all three required attrs are absent."""
    with pytest.raises(TypeError, match="must define class attribute"):

        class MissingAll(MSALOIDCConfiguration):
            pass


def test_subclass_missing_authority_and_scope_raises():
    """`TypeError` should name only the missing attrs."""
    with pytest.raises(TypeError, match="authority") as exc_info:

        class MissingTwo(MSALOIDCConfiguration):
            client_id = "x"

    assert "scope" in str(exc_info.value)


def test_subclass_missing_single_attr_raises():
    """`TypeError` should be raised when only one required attr is absent."""
    with pytest.raises(TypeError, match="scope"):

        class MissingScope(MSALOIDCConfiguration):
            client_id = "x"
            authority = "https://example.com"


def test_subclass_error_names_the_class():
    """`TypeError` message should include the offending class name."""
    with pytest.raises(TypeError, match="NamedBadConfig"):

        class NamedBadConfig(MSALOIDCConfiguration):
            pass


def test_complete_subclass_is_accepted():
    """A subclass defining all three required attrs should not raise."""

    class FullConfig(MSALOIDCConfiguration):
        client_id = "my-client"
        authority = "https://login.example.com/tenant/policy"
        scope = "https://api.example.com/scope"

    cfg = FullConfig()
    assert cfg.client_id == "my-client"
    assert cfg.port == 32284  # inherited default


def test_subclass_can_override_port():
    """A subclass may override the default port."""

    class CustomPort(MSALOIDCConfiguration):
        client_id = "c"
        authority = "https://a.example.com"
        scope = "s"
        port = 9999

    assert CustomPort().port == 9999


def test_production_client_id_is_set():
    assert AnsysIDProduction.client_id == "28982bbf-f354-4e48-8bfb-e542d44c588c"


def test_production_authority_targets_ansysaccount():
    assert "ansysaccount.b2clogin.com" in AnsysIDProduction.authority


def test_production_scope_targets_ansysaccount():
    assert "ansysaccount.onmicrosoft.com" in AnsysIDProduction.scope


def test_production_uses_default_port():
    assert AnsysIDProduction.port == 32284


def test_development_client_id_is_set():
    assert AnsysIDDevelopment.client_id == "63377600-f6ce-4c19-9c0e-a7278d7bde8c"


def test_development_authority_targets_a365dev():
    assert "a365dev.b2clogin.com" in AnsysIDDevelopment.authority


def test_development_scope_targets_a365dev():
    assert "a365dev.onmicrosoft.com" in AnsysIDDevelopment.scope


def test_development_uses_default_port():
    assert AnsysIDDevelopment.port == 32284


def test_production_and_development_configs_differ():
    """The two built-in configs must not share credentials."""
    assert AnsysIDProduction.client_id != AnsysIDDevelopment.client_id
    assert AnsysIDProduction.authority != AnsysIDDevelopment.authority
    assert AnsysIDProduction.scope != AnsysIDDevelopment.scope


@pytest.mark.parametrize(
    "url",
    [
        "https://grantamaterials.ansys.com",
        "https://grantamaterials.ansys.com/",
        "https://GRANTAMATERIALS.ANSYS.COM",
    ],
)
def test_production_url_returns_production_config(url):
    config = get_oidc_config_for_url(url)
    assert isinstance(config, AnsysIDProduction)


@pytest.mark.parametrize(
    "url",
    [
        "https://test-grantami.awsansys7np.onscale.com",
        "https://test-grantami.awsansys7np.onscale.com/",
    ],
)
def test_test_url_returns_development_config(url):
    config = get_oidc_config_for_url(url)
    assert isinstance(config, AnsysIDDevelopment)


def test_unknown_url_raises_value_error():
    with pytest.raises(ValueError, match="No default OIDC configuration"):
        get_oidc_config_for_url("https://my-internal-server.example.com")


def test_unknown_url_error_mentions_known_urls():
    with pytest.raises(ValueError, match="grantamaterials.ansys.com"):
        get_oidc_config_for_url("https://unknown.example.com")


def test_unknown_url_error_suggests_explicit_config():
    with pytest.raises(ValueError, match="oidc_config"):
        get_oidc_config_for_url("https://unknown.example.com")
