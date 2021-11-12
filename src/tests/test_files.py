import os
from tests.testutils import post, get, put, delete, postFiles

from config import Config


file_numerical_id_save = None # will save id upon file creation for tests and remove file by id after all
file_name_save = None
files_count = None


# def test_files_count(client):
#     global files_count  # TODO - is it possible to save variable for another test cases without "global" keyword?
#     status_code, result = get(client, '/files')
#     files_count = len(result)
#     assert status_code == 200

def test_file_create(client, user_token):

    path1 = os.path.join(Config.TESTING_ASSETS_PATH, 'lambo.png')
    path2 = os.path.join(Config.TESTING_ASSETS_PATH, 'book.txt')

    # file_name_save = f'new_file_{ make_random_string(4) }'
    status_code, result = postFiles(client, '/files', [path1,path2], auth=user_token)
    # file_numerical_id_save = int(result['id'])

    # print(Config.STORAGE['ROOT'])

    # assert result['name'] == file_name_save
    assert status_code == 201 # HTTP_201_CREATED

def test_files_list(client, user_token):
    status_code, result = get(client, '/files', auth=user_token)
    # print(result)
    assert status_code == 200
    # assert len(result) == files_count + 1

# def test_files_specific(client):
#     status_code, result = get(client, f'/files/{file_numerical_id_save}')
#     assert result['numerical_id'] == file_numerical_id_save
#     assert result['name'] == file_name_save
#     assert status_code == 200

# def test_file_update(client):
#     data = {'name': file_name_save + '_upd'}
#     status_code, result = put(client, f'/files/{file_numerical_id_save}', data)
#     assert result['numerical_id'] == file_numerical_id_save
#     assert result['name'] == file_name_save + '_upd'
#     assert status_code == 200

# def test_file_delete(client):
#     status_code, result = delete(client, f'/files/{file_numerical_id_save}')
#     assert status_code == 204

# def test_file_after_delete(client):
#     status_code, result = get(client, f'/files/{file_numerical_id_save}')
#     assert status_code == 404

# def test_files_list_again(client):
#     status_code, result = get(client, '/files')
#     assert status_code == 200
#     assert len(result) == files_count


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