import pytest
from abode import AbodeController

def test_gateway_login_logout_success(username, password):
    # Create abode controller with get_devices=False so devices aren't automatically
    # filled at startup (which causes a login attempt at startup)
    abode = AbodeController(username, password, get_devices=False)
    assert abode

    # Login explicitly and ensure the expected values are filled
    assert abode.login()
    assert abode.token
    assert abode.user
    assert abode.panel

    # Logout explicitly and ensure the expected values are emptied
    assert abode.logout()
    assert not abode.token
    assert not abode.user
    assert not abode.panel

def test_gateway_login_failure(username, password):
    # Create abode controller with get_devices=False so devices aren't automatically
    # filled at startup (which causes a login attempt at startup)
    abode = AbodeController("non-existant@login.com", "password", get_devices=False)
    assert abode

    # Attempt to login explicitly, which should fail and raise an exception
    with pytest.raises(Exception):
        abode.login()

    # None of these values should be filled upon failure
    assert not abode.token
    assert not abode.user
    assert not abode.panel
