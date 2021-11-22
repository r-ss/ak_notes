from tests.testutils import post, get, patch, delete

# from config import config

from services.utils import make_random_string

category_uuid_save = None  # will save id upon category creation for tests and remove category by id after all
category_name_save = None
categories_count = None


def test_categories_count(client, alice):
    global categories_count  # TODO - is it possible to save variable for another test cases without "global" keyword?
    status_code, result = get(client, '/categories', auth=alice.token)
    categories_count = len(result)
    assert status_code == 200


def test_category_create(client, alice):
    global category_uuid_save
    global category_name_save
    category_name_save = f'new_category_{ make_random_string(4) }'
    data = {'name': category_name_save}
    status_code, result = post(client, '/categories', data, auth=alice.token)
    category_uuid_save = result['uuid']
    assert result['name'] == category_name_save
    assert status_code == 201  # HTTP_201_CREATED


def test_categories_list(client, alice):
    status_code, result = get(client, '/categories', auth=alice.token)
    assert status_code == 200
    assert len(result) == categories_count + 1


def test_categories_specific(client, alice):
    status_code, result = get(client, f'/categories/{category_uuid_save}', auth=alice.token)
    assert result['uuid'] == category_uuid_save
    assert result['name'] == category_name_save
    assert status_code == 200


def test_category_update(client, alice):
    data = {
        'name': category_name_save + '_upd',
        'uuid': category_uuid_save
    }
    status_code, result = patch(client, f'/categories/{category_uuid_save}', data, auth=alice.token)
    assert result['uuid'] == category_uuid_save
    assert result['name'] == category_name_save + '_upd'
    assert status_code == 200


def test_category_delete(client, alice):
    status_code, result = delete(client, f'/categories/{category_uuid_save}', auth=alice.token)
    assert status_code == 204


def test_category_after_delete(client, alice):
    status_code, result = get(client, f'/categories/{category_uuid_save}', auth=alice.token)
    assert status_code == 404


def test_categories_list_again(client, alice):
    status_code, result = get(client, '/categories', auth=alice.token)
    assert status_code == 200
    assert len(result) == categories_count
