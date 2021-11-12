import os
from tests.testutils import get
from hashlib import blake2b


from config import Config


def test_debug_mode(client):
    if Config.PRODUCTION:
        assert Config.DEBUG == False
    else:
        assert Config.DEBUG == True

def test_testing_mode(client):
    assert Config.TESTING_MODE == True

def test_secrets(client):
    assert Config.SECRET_KEY.startswith('ak512') == True

def test_filesystem(client):
    testfile_path = os.path.join(Config.TESTING_ASSETS_PATH, 'lambo.png')
    assert os.path.isfile(testfile_path) == True
    h = blake2b(digest_size=Config.HASH_DIGEST_SIZE)
    h.update(open(testfile_path, 'rb').read())
    # print(len('011651d77cf25898'))
    assert h.hexdigest() == '011651d77cf25898'


def test_info(client):
    status_code, result = get(client, '/info')
    assert status_code == 200
    assert result['resource'] == 'ak_notes, info'
    assert result['testing'] == True
    assert result['python version'] == '3.10.0'