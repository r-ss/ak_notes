from tests.testutils import post, get, put, delete

from config import Config

from utils import make_random_string

tag_numerical_id_save = None # will save id upon tag creation for tests and remove tag by id after all
tag_name_save = None
tags_count = None


def test_tags_count(client):
    global tags_count  # TODO - is it possible to save variable for another test cases without "global" keyword?
    status_code, result = get(client, '/tags')
    tags_count = len(result)
    assert status_code == 200

def test_tag_create(client):
    global tag_numerical_id_save
    global tag_name_save

    tag_name_save = f'new_tag_{ make_random_string(4) }'
    data = {'name': tag_name_save}
    status_code, result = post(client, '/tags', data)
    tag_numerical_id_save = int(result['numerical_id'])

    assert result['name'] == tag_name_save
    assert status_code == 201 # HTTP_201_CREATED

def test_tags_list(client):
    status_code, result = get(client, '/tags')
    assert status_code == 200
    assert len(result) == tags_count + 1

def test_tags_specific(client):
    status_code, result = get(client, f'/tags/{tag_numerical_id_save}')
    assert result['numerical_id'] == tag_numerical_id_save
    assert result['name'] == tag_name_save
    assert status_code == 200

def test_tag_update(client):
    data = {'name': tag_name_save + '_upd'}
    status_code, result = put(client, f'/tags/{tag_numerical_id_save}', data)
    assert result['numerical_id'] == tag_numerical_id_save
    assert result['name'] == tag_name_save + '_upd'
    assert status_code == 200

def test_tag_deletes(client):
    status_code, result = delete(client, f'/tags/{tag_numerical_id_save}')
    assert status_code == 204

def test_tag_after_delete(client):
    status_code, result = get(client, f'/tags/{tag_numerical_id_save}')
    assert status_code == 404

def test_tags_list_again(client):
    status_code, result = get(client, '/tags')
    assert status_code == 200
    assert len(result) == tags_count


# def test_login(client):
#     login_data = json.dumps({"data": { "username": "Alice","password": "pass_alice" } })
#     status_code, result = post(client, '/login', login_data)
#     assert status_code == 200
#     assert result['auth'] == True

# def test_badlogin(client):
#     login_data = json.dumps({"data": { "username": "bad","password": "fake" } })
#     status_code, result = post(client, '/login', login_data)
#     assert status_code == 400 # User not found
#     assert result['auth'] == False