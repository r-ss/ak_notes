from tests.testutils import get, postForm

from config import Config

token_save = None


def test_auth_login(client):
    global token_save

    data = {
        'username': 'Bob',
        'password': Config.TESTUSER_BOB_PASSWORD,
    }
    status_code, result = postForm(client, '/token', data)
    token_save = result['access_token']
    assert result['token_type'] == 'bearer'
    assert status_code == 202


def test_auth_bad_login(client):
    global token_save
    data = {'username': 'sh', 'password': 'wrong-password'}  # too short
    status_code, result = postForm(client, '/token', data)
    assert result['detail'].startswith('Username must be at least 3 char') is True
    assert status_code == 400


def test_auth_bad_password(client):
    global token_save
    data = {'username': 'Alice', 'password': 'wrong-password'}
    status_code, result = postForm(client, '/token', data)
    assert result['detail'] == 'Wrong password'
    assert status_code == 400


def test_auth_check_token(client, alice_token):
    status_code, result = get(client, '/check_token', auth=alice_token)
    assert status_code == 200


def test_auth_secret_page_via_auth_header(client):
    status_code, result = get(client, '/secretpage', headers={'Authorization': 'bearer ' + token_save})
    assert status_code == 200
    assert result['message'] == 'this is secret message'


def test_auth_secret_page_via_fixture(client, alice_token):
    status_code, result = get(client, '/secretpage', auth=alice_token)
    assert status_code == 200
    assert result['message'] == 'this is secret message'
