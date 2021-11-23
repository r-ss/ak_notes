from tests.testutils import post, get, patch, delete, postForm

# from config import config

from services.utils import make_random_string

user_uuid_save = None  # will save id upon user creation for tests and remove user by id after all
user_username_save = None
user_password_save = None
user_token_save = None


def test_users_get_all(client):
    status_code, result = get(client, '/users')
    assert status_code == 200


def test_user_bad_input(client):
    # No password provided
    data = {'username': 'nopassword'}
    status_code, result = post(client, '/users', data)
    assert result['detail'] == 'Username and password must be provided for registration'
    assert status_code == 400  # HTTP_400_BAD_REQUEST
    # Short password case
    data = {'username': 'shortpassword', 'password': 'short'}
    status_code, result = post(client, '/users', data)
    assert result['detail'].startswith('Password must at least 6 char') is True
    assert status_code == 400  # HTTP_400_BAD_REQUEST


def test_user_create(client):
    global user_uuid_save
    global user_username_save
    global user_password_save

    user_username_save = f'user_{make_random_string(4)}'
    user_password_save = make_random_string(6)

    data = {'username': user_username_save, 'password': user_password_save}
    status_code, result = post(client, '/users', data)

    user_uuid_save = result['uuid']
    assert result['username'] == user_username_save
    assert status_code == 201  # HTTP_201_CREATED


def test_user_get_specific(client):
    status_code, result = get(client, f'/users/{user_uuid_save}')
    assert result['username'] == user_username_save
    assert status_code == 200


def test_user_login(client):
    global user_token_save
    data = {'username': user_username_save, 'password': user_password_save}
    status_code, result = postForm(client, '/token', data)
    user_token_save = result['access_token']
    assert status_code == 202


def test_user_update_by_owner(client):
    data = {'uuid': user_uuid_save, 'username': user_username_save + '_upd'}
    status_code, result = patch(client, f'/users/{user_uuid_save}', data, auth=user_token_save)
    assert result['username'] == user_username_save + '_upd'
    assert status_code == 200


def test_user_update_by_alice(client, alice):
    data = {'uuid': user_uuid_save, 'username': user_username_save + '_upd'}
    status_code, result = patch(client, f'/users/{user_uuid_save}', data, auth=alice.token)
    assert result['detail'] == 'Not allowed'
    assert status_code == 401


def test_user_delete_by_alice(client, alice):
    status_code, result = delete(client, f'/users/{user_uuid_save}', auth=alice.token)
    assert result['detail'] == 'Not allowed'
    assert status_code == 401


def test_user_delete_by_owner(client):
    status_code, result = delete(client, f'/users/{user_uuid_save}', auth=user_token_save)
    assert status_code == 204  # HTTP_204_NO_CONTENT
