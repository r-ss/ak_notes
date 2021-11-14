import os
from tests.testutils import get
from hashlib import blake2b


from config import Config


def test_debug_mode(client):
    if Config.PRODUCTION:
        assert Config.DEBUG is False
    else:
        assert Config.DEBUG is True


def test_testing_mode(client):
    assert Config.TESTING_MODE is True


def test_secrets(client):
    assert Config.SECRET_KEY.startswith('ak512') is True


def test_filesystem(client):
    testfile_path = os.path.join(Config.TESTING_ASSETS_PATH, 'lambo.png')
    assert os.path.isfile(testfile_path) is True
    h = blake2b(digest_size=Config.HASH_DIGEST_SIZE)
    h.update(open(testfile_path, 'rb').read())
    # print(len('011651d77cf25898'))
    assert h.hexdigest() == '011651d77cf25898'


def test_root(client):
    status_code, result = get(client, '/')
    assert status_code == 200
    assert result['message'] == 'there is no root url'


def test_info(client):
    status_code, result = get(client, '/info')
    assert status_code == 200
    assert result['resource'] == 'ak_notes, info'
    assert result['testing'] is True
    assert result['python version'] == '3.10.0'
