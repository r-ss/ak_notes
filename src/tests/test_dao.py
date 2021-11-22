from tests.testutils import post, get, put, patch, delete

from config import config

from services.utils import make_random_string

note_uuid_save = None  # will save id upon note creation for tests and remove note by id after all
note_data_save = None
notes_count = None


def test_dao_1(client):
    status_code, result = get(client, '/dao')
    print(result)
    assert status_code == 200
