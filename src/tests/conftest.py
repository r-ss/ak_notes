import pytest

from config import Config

from main import testclient

from tests.testutils import post

# here test users tokens will be saved after login for use in tests
user_token_save = None
superuser_token_save = None

@pytest.fixture
def client():    
    Config.TESTING_MODE = True
    return testclient


@pytest.fixture
def user_token(client):
    global user_token_save

    # send login request only on first call
    if not user_token_save:
        login_data = {
            "username": Config.TESTUSER['username'],
            "password": Config.TESTUSER['password']
        }
        status_code, result = post(client, '/login', login_data)
        user_token_save = result['token']
    return user_token_save





# @pytest.fixture
# def test_campaign_id():
#     return '60425575ff2ae57e62fc9f16' # No — Campaign for tests
#     # return '60238f2947352c6ff2b835b2' # mazda cx-30 january
