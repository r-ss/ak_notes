import pytest

from config import Config

from main import testclient

from tests.testutils import postForm

# here test users tokens will be saved after login for use in tests
token_alice_save = None
token_bob_save = None
token_super_save = None

@pytest.fixture
def client():    
    Config.TESTING_MODE = True
    return testclient


@pytest.fixture
def alice_token(client):
    global token_alice_save

    # send login request only on first call
    if not token_alice_save:
        login_data = {
            "username": Config.TESTUSER_ALICE['username'],
            "password": Config.TESTUSER_ALICE['password']
        }
        status_code, result = postForm(client, '/token', login_data)
        token_alice_save = result['access_token']
    return token_alice_save


@pytest.fixture
def bob_token(client):
    global token_bob_save

    if not token_bob_save:
        login_data = {
            "username": Config.TESTUSER_BOB['username'],
            "password": Config.TESTUSER_BOB['password']
        }
        status_code, result = postForm(client, '/token', login_data)
        token_bob_save = result['access_token']
    return token_bob_save

@pytest.fixture
def super_token(client):
    global token_super_save

    if not token_super_save:
        login_data = {
            "username": Config.TESTUSER_SUPER['username'],
            "password": Config.TESTUSER_SUPER['password']
        }
        status_code, result = postForm(client, '/token', login_data)
        token_super_save = result['access_token']
    return token_super_save
