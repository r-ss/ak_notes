from tests.testutils import post, get, put, delete

# from config import Config

from utils import make_random_string

category_numerical_id_save = None  # will save id upon category creation for tests and remove category by id after all
category_name_save = None
categories_count = None


def test_categories_count(client, alice_token):
    global categories_count  # TODO - is it possible to save variable for another test cases without "global" keyword?
    status_code, result = get(client, '/categories', auth=alice_token)
    categories_count = len(result)
    assert status_code == 200


def test_category_create(client, alice_token):
    global category_numerical_id_save
    global category_name_save
    category_name_save = f'new_category_{ make_random_string(4) }'
    data = {'name': category_name_save}
    status_code, result = post(client, '/categories', data, auth=alice_token)
    category_numerical_id_save = int(result['numerical_id'])
    assert result['name'] == category_name_save
    assert status_code == 201  # HTTP_201_CREATED


def test_categories_list(client, alice_token):
    status_code, result = get(client, '/categories', auth=alice_token)
    assert status_code == 200
    assert len(result) == categories_count + 1


def test_categories_specific(client, alice_token):
    status_code, result = get(client, f'/categories/{category_numerical_id_save}', auth=alice_token)
    assert result['numerical_id'] == category_numerical_id_save
    assert result['name'] == category_name_save
    assert status_code == 200


def test_category_update(client, alice_token):
    data = {'name': category_name_save + '_upd'}
    status_code, result = put(client, f'/categories/{category_numerical_id_save}', data, auth=alice_token)
    assert result['numerical_id'] == category_numerical_id_save
    assert result['name'] == category_name_save + '_upd'
    assert status_code == 200


def test_category_delete(client, alice_token):
    status_code, result = delete(client, f'/categories/{category_numerical_id_save}', auth=alice_token)
    assert status_code == 204


def test_category_after_delete(client, alice_token):
    status_code, result = get(client, f'/categories/{category_numerical_id_save}', auth=alice_token)
    assert status_code == 404


def test_categories_list_again(client, alice_token):
    status_code, result = get(client, '/categories', auth=alice_token)
    assert status_code == 200
    assert len(result) == categories_count
