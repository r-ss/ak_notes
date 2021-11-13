from tests.testutils import post, get, put, delete

from config import Config

from utils import make_random_string

note_uuid_save = None # will save id upon note creation for tests and remove note by id after all
note_data_save = None
notes_count = None


def test_notes_count(client, alice_token):
    global notes_count  # TODO - is it possible to save variable for another test cases without "global" keyword?
    status_code, result = get(client, '/notes', auth = alice_token)
    notes_count = len(result)
    assert status_code == 200

def test_note_create(client, alice_token):
    global note_uuid_save
    global note_data_save

    note_data_save = data = {
        'title': f'new_note_{ make_random_string(4) }',
        'body': 'boboboboob',
        'tags': ['tag1', 'tag2']
    }
    status_code, result = post(client, '/notes', data, auth = alice_token)

    note_uuid_save = result['uuid']

    assert result['title'] == note_data_save['title']
    assert result['body'] == note_data_save['body']
    assert status_code == 201 # HTTP_201_CREATED

def test_notes_list(client, alice_token):
    status_code, result = get(client, '/notes', auth = alice_token)
    assert status_code == 200
    assert len(result) == notes_count + 1

def test_note_read_by_owner(client, alice_token):
    status_code, result = get(client, f'/notes/{note_uuid_save}', auth = alice_token)
    assert result['title'] == note_data_save['title']
    assert status_code == 200
    
def test_note_read_by_bob(client, bob_token):
    status_code, result = get(client, f'/notes/{note_uuid_save}', auth = bob_token)
    assert status_code == 401

def test_note_update_by_owner(client, alice_token):
    data = {'title': '%s_upd' % note_data_save['title']}
    status_code, result = put(client, f'/notes/{note_uuid_save}', data, auth = alice_token)
    assert result['title'] == '%s_upd' % note_data_save['title']
    assert result['body'] == note_data_save['body']
    assert status_code == 200

    data = {'body': '%s_upd' % note_data_save['body']}
    status_code, result = put(client, f'/notes/{note_uuid_save}', data, auth = alice_token)
    assert result['body'] == '%s_upd' % note_data_save['body']
    assert status_code == 200

def test_note_update_by_bob(client, bob_token):
    data = {'title': '%s_bob' % note_data_save['title']}
    status_code, result = put(client, f'/notes/{note_uuid_save}', data, auth = bob_token)
    assert status_code == 401


def test_note_change_category_by_owner(client, alice_token):
    data = {'numerical_id': 6}
    status_code, result = put(client, f'/notes/{note_uuid_save}/change-category', data, auth = alice_token)
    assert status_code == 200


def test_note_delete_by_bob(client, bob_token):
    status_code, result = delete(client, f'/notes/{note_uuid_save}', auth = bob_token)
    assert status_code == 401

def test_note_delete_by_owner(client, alice_token):
    status_code, result = delete(client, f'/notes/{note_uuid_save}', auth = alice_token)
    assert status_code == 204

def test_note_after_delete(client, alice_token):
    status_code, result = get(client, f'/notes/{note_uuid_save}', auth = alice_token)
    assert status_code == 404

def test_notes_list_again(client, alice_token):
    status_code, result = get(client, '/notes', auth = alice_token)
    assert status_code == 200
    assert len(result) == notes_count
