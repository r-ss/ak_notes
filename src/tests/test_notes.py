from tests.testutils import post, get, put, delete

from config import config

from services.utils import make_random_string

note_uuid_save = None  # will save id upon note creation for tests and remove note by id after all
note_data_save = None
notes_count = None


def test_note_read_default_note(client, alice):
    status_code, result = get(client, f'/notes/{config.TESTNOTE_BY_ALICE_UUID}', auth=alice.token)
    assert status_code == 200


def test_notes_count(client, alice):
    global notes_count  # TODO - is it possible to save variable for another test cases without "global" keyword?
    status_code, result = get(client, '/notes', auth=alice.token)
    notes_count = len(result)
    assert status_code == 200


def test_note_create_under_default_category(client, alice):
    global note_uuid_save
    global note_data_save
    note_data_save = data = {
        'title': f'new_note_{ make_random_string(4) }',
        'body': 'note in default category by Alice'
    }
    status_code, result = post(client, '/notes', data, auth=alice.token)
    note_uuid_save = result['uuid']
    assert result['title'] == note_data_save['title']
    assert result['body'] == note_data_save['body']
    assert status_code == 201  # HTTP_201_CREATED


def test_note_create_under_specific_category(client, alice):
    global note_uuid_save
    global note_data_save
    data = {
        'title': f'new_nogte_{ make_random_string(4) }',
        'body': 'note in specific category by Alice'
    }
    status_code, result = post(client, f'categories/{alice.default_category_uuid}/notes', data, auth=alice.token)
    # note_uuid_save = result['uuid']
    assert result['title'] == data['title']
    assert result['body'] == data['body']
    assert status_code == 201  # HTTP_201_CREATED


def test_notes_list(client, alice):
    status_code, result = get(client, '/notes', auth=alice.token)
    assert status_code == 200
    assert len(result) == notes_count + 2


def test_note_read_by_owner(client, alice):
    status_code, result = get(client, f'/notes/{note_uuid_save}', auth=alice.token)
    assert result['title'] == note_data_save['title']
    assert status_code == 200


def test_note_read_by_bob(client, bob):
    status_code, result = get(client, f'/notes/{config.TESTNOTE_BY_ALICE_UUID}', auth=bob.token)
    assert status_code == 401


def test_note_filter(client, alice):
    status_code, result = get(client, '/notes?filter=huy', auth=alice.token)
    assert status_code == 200


def test_note_pagination(client, alice):
    status_code, result = get(client, '/notes?filter=huy&limit=1&offset=1', auth=alice.token)
    assert status_code in [200, 400]

# def test_notes_list_by_tag(client, alice):
#     status_code, result = get(client, '/notes/with-tag/supertag', auth=alice.token)
#     assert status_code == 200
#     assert len(result) == 1


def test_note_update_by_owner(client, alice):
    # note_data_save = {
    #     'uuid': note_uuid_save,
    #     'title': f'new_note_{ make_random_string(4) }',
    #     'body': 'boboboboob'
    # }

    # Title
    data = {'uuid': note_uuid_save, 'title': '%s_upd' % note_data_save['title'], 'body': note_data_save['body']}
    status_code, result = put(client, '/notes', data, auth=alice.token)
    assert result['title'] == '%s_upd' % note_data_save['title']
    assert result['body'] == note_data_save['body']
    assert status_code == 200
    # Body
    data = {'uuid': note_uuid_save, 'body': '%s_upd' % note_data_save['body']}
    status_code, result = put(client, '/notes', data, auth=alice.token)
    assert result['body'] == '%s_upd' % note_data_save['body']
    assert status_code == 200
    # Tags
    # data = {'uuid': note_uuid_save, 'tags': ['tag7', 'tag2', 'tag600']}
    # status_code, result = put(client, f'/notes/{note_uuid_save}', data, auth=alice.token)
    # assert result['tags'] == data['tags']
    # assert status_code == 200


def test_note_update_by_bob(client, bob):
    data = {'uuid': note_uuid_save, 'title': 'i_am_bob'}
    status_code, result = put(client, '/notes', data, auth=bob.token)
    assert status_code == 401


# def test_note_change_category_by_owner(client, alice):
#     data = {'numerical_id': 6}
#     status_code, result = put(client, f'/notes/{note_uuid_save}/change-category', data, auth=alice.token)
#     assert status_code == 200


def test_note_delete_by_bob(client, bob):
    status_code, result = delete(client, f'/notes/{note_uuid_save}', auth=bob.token)
    assert status_code == 401


def test_note_delete_by_owner(client, alice):
    status_code, result = delete(client, f'/notes/{note_uuid_save}', auth=alice.token)
    assert status_code == 204


def test_note_after_delete(client, alice):
    status_code, result = get(client, f'/notes/{note_uuid_save}', auth=alice.token)
    assert status_code == 404


def test_remove_unnecessary_notes(client, alice):
    status_code, result = get(client, '/notes', auth=alice.token)

    for item in result:
        uuid = item['uuid']
        if uuid != config.TESTNOTE_BY_ALICE_UUID:
            status_code2, result2 = delete(client, f'/notes/{uuid}', auth=alice.token)
            assert status_code2 == 204

    status_code, result = get(client, '/notes', auth=alice.token)
    assert status_code == 200
    assert len(result) == notes_count
