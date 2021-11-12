from tests.testutils import get

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

def test_info(client):
    status_code, result = get(client, '/info')
    assert status_code == 200
    assert result['resource'] == 'ak_notes, info'
    assert result['testing'] == True
    assert result['python version'] == '3.10.0'