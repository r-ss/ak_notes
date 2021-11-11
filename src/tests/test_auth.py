from tests.testutils import post, get

from config import Config

token_save = None

def test_auth_login(client):
    global token_save
    data = {
        'username': Config.TESTUSER['username'],
        'password': Config.TESTUSER['password']
    }
    status_code, result = post(client, '/login', data)
    token_save = result['token']
    assert result['auth'] == True
    assert status_code == 202


def test_auth_check_token(client):
    data = {'token': token_save}
    status_code, result = post(client, '/token', data)
    assert status_code == 202


def test_auth_secret_page(client):
    status_code, result = get(client, '/secretpage', headers={'X-Token': token_save})
    assert status_code == 200
    assert result['message'] == 'this is secret message'