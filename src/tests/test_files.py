import os
# from tests.conftest import alice
from tests.testutils import get, put, delete, postFiles

from config import config


file_numerical_id_save = None  # will save id upon file creation for tests and remove file by id after all
file_name_save = None
files_count = None
uploaded_files = None


def test_files_count(client, alice):
    global files_count  # TODO - is it possible to save variable for another test cases without "global" keyword?
    status_code, result = get(client, f'/users/{alice.uuid}/files', auth=alice.token)
    # print(result, len(result))
    files_count = len(result)
    assert status_code == 200


def test_files_create(client, alice):
    global uploaded_files
    path1 = os.path.join(config.TESTING_ASSETS_PATH, 'lambo.png')
    path2 = os.path.join(config.TESTING_ASSETS_PATH, 'book.txt')
    status_code, result = postFiles(client, f'/notes/{config.TESTNOTE_BY_ALICE_UUID}/files', [path1, path2], auth=alice.token)
    uploaded_files = result
    assert status_code == 201  # HTTP_201_CREATED


def test_files_list_for_user(client, alice):
    global uploaded_files
    status_code, result = get(client, f'/users/{alice.uuid}/files', auth=alice.token)
    # print(result, len(result))
    assert status_code == 200
    assert len(result) == files_count + len(uploaded_files)


def test_files_list_for_note(client, alice):
    status_code, result = get(client, f'/notes/{config.TESTNOTE_BY_ALICE_UUID}/files', auth=alice.token)
    # print(result, len(result))
    assert status_code == 200
    assert len(result) == files_count + len(uploaded_files)


def test_files_specific_by_owner(client, alice):
    global uploaded_files
    status_code, result = get(client, f"/files/{uploaded_files[0]['uuid']}", auth=alice.token)
    assert result['uuid'] == uploaded_files[0]['uuid']
    assert status_code == 200


def test_files_specific_by_bob(client, bob):
    global uploaded_files
    status_code, result = get(client, f"/files/{uploaded_files[0]['uuid']}", auth=bob.token)
    assert status_code == 401


def test_file_update(client, alice):
    global uploaded_files
    data = {
        'uuid': uploaded_files[0]['uuid'],
        'filename': 'supermeganame.png'
    }
    status_code, result = put(client, f"/files/{uploaded_files[0]['uuid']}", data, auth=alice.token)
    assert status_code == 200


def test_files_delete_by_bob(client, bob):
    global uploaded_files
    file = uploaded_files[0]
    status_code, result = delete(client, '/files/%s' % file['uuid'], auth=bob.token)
    assert status_code == 401


def test_files_delete_by_owner(client, alice):
    global uploaded_files
    for file in uploaded_files:
        status_code, result = delete(client, '/files/%s' % file['uuid'], auth=alice.token)
        assert status_code == 204


def test_file_after_delete(client, alice):
    global uploaded_files
    for file in uploaded_files:
        status_code, result = get(client, '/files/%s' % file['uuid'], auth=alice.token)
        assert status_code == 404


def test_files_list_again(client, alice):
    global uploaded_files
    status_code, result = get(client, f'/users/{alice.uuid}/files', auth=alice.token)
    # print(result, len(result))
    assert status_code == 200
    assert len(result) == files_count
