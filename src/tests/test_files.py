import os
from tests.testutils import get, put, delete, postFiles

from config import Config


file_numerical_id_save = None  # will save id upon file creation for tests and remove file by id after all
file_name_save = None
files_count = None
uploaded_files = None


def test_files_count(client, alice_token):
    global files_count  # TODO - is it possible to save variable for another test cases without "global" keyword?
    status_code, result = get(client, '/files/for-user', auth=alice_token)
    files_count = len(result)
    assert status_code == 200


def test_files_create(client, alice_token):
    global uploaded_files
    path1 = os.path.join(Config.TESTING_ASSETS_PATH, 'lambo.png')
    path2 = os.path.join(Config.TESTING_ASSETS_PATH, 'book.txt')
    status_code, result = postFiles(client, f'/notes/{Config.TESTNOTE_BY_ALICE_UUID}/create-file', [path1, path2], auth=alice_token)
    uploaded_files = result
    assert status_code == 201  # HTTP_201_CREATED


def test_files_list_for_user(client, alice_token):
    global uploaded_files
    status_code, result = get(client, '/files/for-user', auth=alice_token)
    assert status_code == 200
    assert len(result) == files_count + len(uploaded_files)


def test_files_list_for_note(client, alice_token):
    status_code, result = get(
        client, f'/files/for-note/{Config.TESTNOTE_BY_ALICE_UUID}', auth=alice_token
    )
    assert status_code == 200
    assert len(result) == files_count + len(uploaded_files)


def test_files_specific_by_owner(client, alice_token):
    global uploaded_files
    status_code, result = get(client, f"/files/read/{uploaded_files[0]['uuid']}", auth=alice_token)
    assert result['uuid'] == uploaded_files[0]['uuid']
    assert status_code == 200


def test_files_specific_by_bob(client, bob_token):
    global uploaded_files
    status_code, result = get(client, f"/files/read/{uploaded_files[0]['uuid']}", auth=bob_token)
    assert status_code == 401


def test_file_update(client, alice_token):
    data = {'filename': 'supermeganame.png'}
    status_code, result = put(client, f"/files/{uploaded_files[0]['uuid']}", data, auth=alice_token)
    assert status_code == 200


def test_files_delete_by_bob(client, bob_token):
    global uploaded_files
    file = uploaded_files[0]
    status_code, result = delete(client, '/files/%s' % file['uuid'], auth=bob_token)
    assert status_code == 401


def test_files_delete_by_owner(client, alice_token):
    global uploaded_files
    for file in uploaded_files:
        status_code, result = delete(client, '/files/%s' % file['uuid'], auth=alice_token)
        assert status_code == 204


def test_file_after_delete(client, alice_token):
    global uploaded_files
    for file in uploaded_files:
        status_code, result = get(client, '/files/read/%s' % file['uuid'], auth=alice_token)
        assert status_code == 404


def test_files_list_again(client, alice_token):
    global uploaded_files
    status_code, result = get(client, '/files/for-user', auth=alice_token)
    assert status_code == 200
    assert len(result) == files_count
