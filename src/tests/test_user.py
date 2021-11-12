from tests.testutils import post, get, put, delete, postForm

from config import Config

from utils import make_random_string

user_uuid_save = None # will save id upon user creation for tests and remove user by id after all
user_username_save = None
user_password_save = None
user_token_save = None

def test_user_bad_input(client):
    # No password provided
    data = {'username': 'nopassword'}
    status_code, result = post(client, '/user/register', data)
    assert result['message'] == 'Username and password must be provided for registration'
    assert status_code == 400 # HTTP_400_BAD_REQUEST
    # Short password case
    data = {'username': 'shortpassword', 'password': 'short'}
    status_code, result = post(client, '/user/register', data)
    assert result['message'].startswith('Password must at least 6 char') == True
    assert status_code == 400 # HTTP_400_BAD_REQUEST


def test_user_create(client):
    global user_uuid_save
    global user_username_save
    global user_password_save

    user_username_save = f'user_{make_random_string(4)}'
    user_password_save = make_random_string(6)

    # user_username_save = Config.TESTUSER_BOB['username']
    # user_password_save = Config.TESTUSER_BOB['password']

    data = {'username': user_username_save, 'password': user_password_save}
    status_code, result = post(client, '/user/register', data)

    user_uuid_save = result['uuid']
    assert result['message'] == 'user registered'
    assert result['username'] == user_username_save
    assert status_code == 201 # HTTP_201_CREATED


def test_user_get(client):
    status_code, result = get(client, f'/user/{user_uuid_save}')
    assert result['username'] == user_username_save
    assert status_code == 200

def test_user_login(client):
    global user_token_save
    data = {
        'username': user_username_save,
        'password': user_password_save
    }
    status_code, result = postForm(client, '/token', data)
    user_token_save = result['access_token']
    # print(f'{user_username_save} logged in, token: {user_token_save}')
    assert status_code == 202

def test_user_update_by_owner(client):
    data = {'username': user_username_save + '_upd'}
    status_code, result = put(client, f'/user/{user_uuid_save}', data, auth = user_token_save)
    assert result['username'] == user_username_save + '_upd'
    assert status_code == 200

def test_user_update_by_alice(client, alice_token):
    data = {'username': user_username_save + '_upd'}
    status_code, result = put(client, f'/user/{user_uuid_save}', data, auth = alice_token)
    assert result['detail'] =='Seems like you are not authorized to this'
    assert status_code == 401

def test_user_delete_by_alice(client, alice_token):
    status_code, result = delete(client, f'/user/{user_uuid_save}', auth = alice_token)
    assert result['detail'] =='Seems like you are not authorized to this'
    assert status_code == 401

def test_user_delete_by_owner(client):
    status_code, result = delete(client, f'/user/{user_uuid_save}', auth = user_token_save)
    # print(result, user_uuid_save, user_token_save)
    assert status_code == 204 # HTTP_204_NO_CONTENT