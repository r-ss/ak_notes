from tests.testutils import get, patch, delete, post

from config import config

tag_uuid_save = None  # will save id upon tag creation for tests and remove tag by id after all
tag_name_save = None
tags_count = None
created_tag = None


def test_tags_count(client, alice):
    global tags_count  # TODO - is it possible to save variable for another test cases without "global" keyword?
    status_code, result = get(client, "/tags", auth=alice.token)
    tags_count = len(result)
    assert status_code == 200


def test_tags_create(client, alice):
    global created_tag
    data = {"name": "sexysupertag"}
    status_code, result = post(client, f"/notes/{config.TESTNOTE_BY_ALICE_UUID}/tags", data, auth=alice.token)
    created_tag = result
    assert status_code == 201  # HTTP_201_CREATED


def test_tags_count_again(client, alice):
    global tags_count  # TODO - is it possible to save variable for another test cases without "global" keyword?
    status_code, result = get(client, f"/users/{alice.uuid}/tags", auth=alice.token)
    assert len(result) == tags_count + 1
    assert status_code == 200


def test_tags_list_for_user(client, alice):
    global created_tag
    status_code, result = get(client, f"/users/{alice.uuid}/tags", auth=alice.token)
    assert status_code == 200


def test_tags_list_for_note(client, alice):
    status_code, result = get(client, f"/notes/{config.TESTNOTE_BY_ALICE_UUID}/tags", auth=alice.token)
    assert status_code == 200


def test_tag_update(client, alice):
    global created_tag
    data = {"uuid": created_tag["uuid"], "name": "supermeganame", "color": "red"}

    status_code, result = patch(client, f"/tags/{created_tag['uuid']}", data, auth=alice.token)
    assert result["color"] == "red"
    assert status_code == 200


# def test_get_notes_by_tag(client, alice):
#     status_code, result = get(client, f'/tags/{created_tag["uuid"]}/notes', auth=alice.token)
#     print(result)
#     assert status_code == 200


def test_tags_delete_by_bob(client, bob):
    global created_tag
    status_code, result = delete(client, "/tags/%s" % created_tag["uuid"], auth=bob.token)
    assert status_code == 401


def test_tags_delete_by_owner(client, alice):
    global created_tag
    status_code, result = delete(client, "/tags/%s" % created_tag["uuid"], auth=alice.token)
    assert status_code == 204


def test_tag_after_delete(client, alice):
    global created_tag
    status_code, result = get(client, "/tags/%s" % created_tag["uuid"], auth=alice.token)
    assert status_code == 404


def test_tags_list_again(client, alice):
    global created_tag
    status_code, result = get(client, f"/users/{alice.uuid}/tags", auth=alice.token)
    assert status_code == 200
    assert len(result) == tags_count
