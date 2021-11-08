import pytest

from config import Config

from main import testclient

from tests.testutils import post


@pytest.fixture
def client():    
    Config.TESTING_MODE = True
    return testclient


# @pytest.fixture
# def test_campaign_id():
#     return '60425575ff2ae57e62fc9f16' # No — Campaign for tests
#     # return '60238f2947352c6ff2b835b2' # mazda cx-30 january
