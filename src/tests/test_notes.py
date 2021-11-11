from tests.testutils import post, get, put, delete

from config import Config

from utils import make_random_string

note_numerical_id_save = None # will save id upon note creation for tests and remove note by id after all
note_data_save = None
notes_count = None


# def test_notes_count(client):
#     global notes_count  # TODO - is it possible to save variable for another test cases without "global" keyword?
#     status_code, result = get(client, '/notes')
#     notes_count = len(result)
#     assert status_code == 200

# def test_note_create(client):
#     global note_numerical_id_save
#     global note_data_save

#     note_data_save = data = {
#         'title': f'new_note_{ make_random_string(4) }',
#         'body': 'boboboboob'
#     }

#     status_code, result = post(client, '/notes', data)
#     # note_numerical_id_save = int(result['numerical_id'])

#     print(result)

#     # assert result['name'] == note_data_save
#     assert status_code == 201 # HTTP_201_CREATED

# def test_notes_list(client):
#     status_code, result = get(client, '/notes')
#     assert status_code == 200
#     assert len(result) == notes_count + 1

def test_notes_specific(client):
    # status_code, result = get(client, f'/notes/{note_numerical_id_save}')
    status_code, result = get(client, '/notes/1')
    # assert result['numerical_id'] == note_numerical_id_save
    # assert result['name'] == note_data_save
    print(result)
    assert status_code == 200

# def test_note_update(client):
#     data = {'name': note_data_save + '_upd'}
#     status_code, result = put(client, f'/notes/{note_numerical_id_save}', data)
#     assert result['numerical_id'] == note_numerical_id_save
#     assert result['name'] == note_data_save + '_upd'
#     assert status_code == 200

# def test_note_delete(client):
#     status_code, result = delete(client, f'/notes/{note_numerical_id_save}')
#     assert status_code == 204

# def test_note_after_delete(client):
#     status_code, result = get(client, f'/notes/{note_numerical_id_save}')
#     assert status_code == 404

# def test_notes_list_again(client):
#     status_code, result = get(client, '/notes')
#     assert status_code == 200
#     assert len(result) == notes_count
