from tests.testutils import post, get, put, patch, delete

from config import config

from services.utils import make_random_string

note_uuid_save = None



def test_dao_post(client):
    global note_uuid_save
    data = {
        'title': f'new_note_via_dao',
        'body': 'note via dao'
    }
    status_code, result = post(client, '/dao', data)
    print(result)
    note_uuid_save = result['uuid']
    assert status_code == 201

def test_dao_get_one(client):
    status_code, result = get(client, f'/dao/one/{note_uuid_save}')
    print(result)
    assert status_code == 200

def test_dao_get_all(client):
    status_code, result = get(client, '/dao/all')
    print(result)
    assert status_code == 200

def test_dao_delete(client):
    status_code, result = delete(client, f'/dao/{note_uuid_save}')
    print(result)
    assert status_code == 200