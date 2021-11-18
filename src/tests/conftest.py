import pytest

from config import config

from main import testclient


from tests.testutils import postForm

# here test users tokens will be saved after login for use in tests
token_alice_save = None
token_bob_save = None
token_super_save = None


class LoggedInTestUser:
    """ Represents logged-in test user, used only in tests """

    def __init__(self, uuid: str, token: str) -> None:
        self.uuid: str = uuid
        self.token: str = token



alice_save = None
bob_save = None
jesus_save = None


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


@pytest.fixture
def alice(client):
    global alice_save

    # send login request only on first call
    if not alice_save:
        login_data = {
            'username': 'Alice',
            'password': config.TESTUSER_ALICE_PASSWORD,
        }
        status_code, result = postForm(client, '/token', login_data)
        alice_save = LoggedInTestUser(result['uuid'], result['access_token'])
    return alice_save

@pytest.fixture
def bob(client):
    global bob_save

    # send login request only on first call
    if not bob_save:
        login_data = {
            'username': 'Bob',
            'password': config.TESTUSER_BOB_PASSWORD,
        }
        status_code, result = postForm(client, '/token', login_data)
        bob_save = LoggedInTestUser(result['uuid'], result['access_token'])
    return bob_save

@pytest.fixture
def jesus(client):
    global jesus_save

    # send login request only on first call
    if not jesus_save:
        login_data = {
            'username': 'Jesus',
            'password': config.TESTUSER_SUPER_PASSWORD,
        }
        status_code, result = postForm(client, '/token', login_data)
        jesus_save = LoggedInTestUser(result['uuid'], result['access_token'])
    return jesus_save