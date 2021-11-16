import pytest

from config import config

from main import testclient

from tests.testutils import postForm

# here test users tokens will be saved after login for use in tests
token_alice_save = None
token_bob_save = None
token_super_save = None


@pytest.fixture
def client():
    config.TESTING_MODE = True
    return testclient


@pytest.fixture
def alice_token(client):
    global token_alice_save

    # send login request only on first call
    if not token_alice_save:
        login_data = {
            'username': 'Alice',
            'password': config.TESTUSER_ALICE_PASSWORD,
        }
        status_code, result = postForm(client, '/token', login_data)
        token_alice_save = result['access_token']
    return token_alice_save


@pytest.fixture
def bob_token(client):
    global token_bob_save

    if not token_bob_save:
        login_data = {
            'username': 'Bob',
            'password': config.TESTUSER_BOB_PASSWORD,
        }
        status_code, result = postForm(client, '/token', login_data)
        token_bob_save = result['access_token']
    return token_bob_save


@pytest.fixture
def super_token(client):
    global token_super_save

    if not token_super_save:
        login_data = {
            'username': 'Jesus',
            'password': config.TESTUSER_SUPER_PASSWORD,
        }
        status_code, result = postForm(client, '/token', login_data)
        token_super_save = result['access_token']
    return token_super_save
