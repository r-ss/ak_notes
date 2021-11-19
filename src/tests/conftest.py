import pytest

from config import config

from main import testclient


from tests.testutils import get, postForm

# here test users tokens will be saved after login for use in tests
# token_alice_save = None
# token_bob_save = None
# token_super_save = None


class LoggedInTestUser:
    """ Represents logged-in test user, used only in tests """

    def __init__(self, uuid: str, token: str) -> None:
        self.uuid: str = uuid
        self.token: str = token
        self.default_category_uuid = None

# test users, Alice and Bob are regilat users, Jesus have admin privilegies
alice_save = None
bob_save = None
jesus_save = None


@pytest.fixture
def client():
    config.TESTING_MODE = True
    return testclient


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

        status_code, result = get(client, '/categories?only_last=yes', auth=alice_save.token)
        if status_code == 200:
            alice_save.default_category_uuid = result['uuid']

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

        status_code, result = get(client, '/categories?only_last=yes', auth=bob_save.token)
        if status_code == 200:
            bob_save.default_category_uuid = result['uuid']

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

        status_code, result = get(client, '/categories?only_last=yes', auth=jesus_save.token)
        if status_code == 200:
            jesus_save.default_category_uuid = result['uuid']

    return jesus_save