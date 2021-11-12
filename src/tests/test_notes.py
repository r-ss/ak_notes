from tests.testutils import post, get, put, delete

from config import Config

from utils import make_random_string

note_uuid_save = None # will save id upon note creation for tests and remove note by id after all
note_data_save = None
notes_count = None


def test_notes_count(client, user_token):
    global notes_count  # TODO - is it possible to save variable for another test cases without "global" keyword?
    status_code, result = get(client, '/notes', auth = user_token)
    notes_count = len(result)
    assert status_code == 200

def test_note_create(client, user_token):
    global note_uuid_save
    global note_data_save

    note_data_save = data = {
        'title': f'new_note_{ make_random_string(4) }',
        'body': 'boboboboob'
    }
    status_code, result = post(client, '/notes', data, auth = user_token)
    note_uuid_save = result['uuid']

    assert result['title'] == note_data_save['title']
    assert result['body'] == note_data_save['body']
    assert status_code == 201 # HTTP_201_CREATED

def test_notes_list(client, user_token):
    status_code, result = get(client, '/notes', auth = user_token)
    assert status_code == 200
    assert len(result) == notes_count + 1

def test_notes_specific(client, user_token):
    status_code, result = get(client, f'/notes/{note_uuid_save}', auth = user_token)
    assert result['title'] == note_data_save['title']
    assert status_code == 200

def test_note_update(client, user_token):
    data = {'title': '%s_upd' % note_data_save['title']}
    status_code, result = put(client, f'/notes/{note_uuid_save}', data, auth = user_token)
    assert result['title'] == '%s_upd' % note_data_save['title']
    assert status_code == 200

def test_note_delete(client, user_token):
    status_code, result = delete(client, f'/notes/{note_uuid_save}', auth = user_token)
    assert status_code == 204

def test_note_after_delete(client, user_token):
    status_code, result = get(client, f'/notes/{note_uuid_save}', auth = user_token)
    assert status_code == 404

def test_notes_list_again(client, user_token):
    status_code, result = get(client, '/notes', auth = user_token)
    assert status_code == 200
    assert len(result) == notes_count
