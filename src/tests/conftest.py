import pytest

from pydantic import UUID4


from config import config

from main import testclient

from tests.testutils import get, postForm


""" We have 3 Test users:
    - Alice, regular user
    - Bob, regular user
    - Jesus, with admin privilegies
"""

alice_save = bob_save = jesus_save = None


class LoggedInTestUser:
    """Represents logged-in test user, used only in tests"""

    def __init__(self, uuid: str, token: str) -> None:
        self.uuid: UUID4 = uuid
        self.token: str = token
        self.default_category_uuid: UUID4 = None


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
            "username": "Alice",
            "password": config.TESTUSER_ALICE_PASSWORD,
        }
        status_code, result = postForm(client, "/token", login_data)
        alice_save = LoggedInTestUser(result["uuid"], result["access_token"])

        status_code, result = get(client, "/categories?only_last=yes", auth=alice_save.token)
        if status_code == 200:
            alice_save.default_category_uuid = result["uuid"]

    return alice_save


@pytest.fixture
def bob(client):
    global bob_save

    # send login request only on first call
    if not bob_save:
        login_data = {
            "username": "Bob",
            "password": config.TESTUSER_BOB_PASSWORD,
        }
        status_code, result = postForm(client, "/token", login_data)
        bob_save = LoggedInTestUser(result["uuid"], result["access_token"])

        status_code, result = get(client, "/categories?only_last=yes", auth=bob_save.token)
        if status_code == 200:
            bob_save.default_category_uuid = result["uuid"]

    return bob_save


@pytest.fixture
def jesus(client):
    global jesus_save

    # send login request only on first call
    if not jesus_save:
        login_data = {
            "username": "Jesus",
            "password": config.TESTUSER_SUPER_PASSWORD,
        }
        status_code, result = postForm(client, "/token", login_data)
        jesus_save = LoggedInTestUser(result["uuid"], result["access_token"])

        status_code, result = get(client, "/categories?only_last=yes", auth=jesus_save.token)
        if status_code == 200:
            jesus_save.default_category_uuid = result["uuid"]

    return jesus_save
