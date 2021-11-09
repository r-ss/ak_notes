from tests.testutils import post, get, put, delete

from config import Config

from utils import make_random_string

user_uuid_save = None # will save id upon user creation for tests and remove user by id after all
user_username_save = None
user_password_save = None

def test_user_create(client):
    global user_uuid_save
    global user_username_save
    global user_password_save

    user_username_save = f'user_{make_random_string(4)}'
    user_password_save = make_random_string(6)

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

def test_user_update(client):
    data = {'username': user_username_save + '_upd'}
    status_code, result = put(client, f'/user/{user_uuid_save}', data)
    assert result['username'] == user_username_save + '_upd'
    assert status_code == 200

def test_user_delete(client):
    status_code, result = delete(client, f'/user/{user_uuid_save}')
    assert status_code == 204 # HTTP_204_NO_CONTENT