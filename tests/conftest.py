import pytest
from abode import AbodeController

def pytest_addoption(parser):
    parser.addoption("--username", help="Username", required=True)
    parser.addoption("--password", help="Password", required=True)

@pytest.fixture(scope="module")
def username(request):
    return request.config.getoption("--username")

@pytest.fixture(scope="module")
def password(request):
    return request.config.getoption("--password")

@pytest.fixture(scope="module")
def abode(username, password):
    a = AbodeController(username, password)
    yield a
    a.logout()
