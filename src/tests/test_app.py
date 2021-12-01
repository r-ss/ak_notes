import os
from tests.testutils import get
from hashlib import blake2b


from config import config


def test_debug_mode(client):
    if config.PRODUCTION:
        assert config.DEBUG is False
    else:
        assert config.DEBUG is True


def test_testing_mode(client):
    assert config.TESTING_MODE is True


def test_secrets(client):
    assert config.SECRET_KEY.startswith('ak512') is True


def test_filesystem(client):
    testfile_path = os.path.join(config.TESTING_ASSETS_PATH, 'lambo.png')
    assert os.path.isfile(testfile_path) is True
    h = blake2b(digest_size=config.HASH_DIGEST_SIZE)
    h.update(open(testfile_path, 'rb').read())
    assert h.hexdigest() == '011651d77cf25898'


def test_root(client):
    status_code, result = get(client, '/')
    assert status_code == 404


def test_info(client):
    status_code, result = get(client, '/info')
    assert status_code == 200
    assert result['resource'].startswith('ak_notes') is True
    assert result['testing'] is True
    assert result['python version'] == '3.10.0'
