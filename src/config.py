import os
import datetime
from pydantic import BaseSettings

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

PRODUCTION = True

STORAGEROOT = '/storage/'
if not os.path.isdir(STORAGEROOT):
    PRODUCTION = False
    STORAGEROOT = '%s/storage/' % os.path.split(BASE_DIR)[0]

# import pytz
# TZ = pytz.timezone('Europe/Moscow')


class AppConfig(BaseSettings):
    """ Using Pydantic's approach to manage application config
        Docs: https://pydantic-docs.helpmanual.io/usage/settings/
    """

    # GENERAL SETTINGS AND HOSTS
    BASE_DIR: str = BASE_DIR
    PRODUCTION: bool = PRODUCTION
    DEBUG: bool = not PRODUCTION
    SECRET_KEY: str = None
    DBHOST: str = None

    # TESTS
    # TODO - move test users credentials into a secrets, for now they presented here for simplicity
    TESTING_MODE: bool = False  # Must be set to True only in autotests
    TESTING_ASSETS_PATH: str = '%s/testing_assets/' % os.path.split(BASE_DIR)[0]
    # Define passwords for 2 regular users and 1 admin to check permissions in tests
    TESTUSER_ALICE_PASSWORD: str = None  # username: Alice
    TESTUSER_BOB_PASSWORD: str = None  # username: Bob
    TESTUSER_SUPER_PASSWORD: str = None  # username: Jesus
    TESTNOTE_BY_ALICE_UUID: str = 'a71158eb-016f-4c56-b516-b6c7a49ed8c4'  # used in tests
    CODECLIMATE_TEST_REPORTER_ID: str = 'not available locally, will be overwritten by ENV'

    # FORMATTERS
    DATETIME_FORMAT_TECHNICAL: str = '%Y-%m-%d %H:%M:%S'
    DATETIME_FORMAT_HUMAN: str = '%d.%m.%Y %H:%M'

    # PATHS
    STORAGE: dict = {'ROOT': STORAGEROOT, 'UPLOADS': '%s/uploads/' % os.path.split(BASE_DIR)[0]}

    # AUTHENTICATION
    AUTH_USERNAME_REGEX: dict = {
        'regex': r'\A[\w\-\.]{3,}\Z',
        'failmessage': 'Username must be at least 3 characters and may contain . - _ chars.'  # also can be used as hint
    }
    AUTH_PASSWORD_REGEX: dict = {
        'regex': r'\A[\w\-\.]{6,}\Z',
        'failmessage': 'Password must at least 6 characters and may contain . - _ symbols'  # also can be used as hint
    }
    AUTH_HASHING_ALGORITHM: str = 'HS256'  # algorithm to encode/decode JWT user tokens
    AUTH_TOKEN_EXPIRATION_TIME: datetime.timedelta = datetime.timedelta(days=30)

    # MISC
    HASH_DIGEST_SIZE: int = 8  # for hashing files with blake2b

    # ALLOWED_UPLOADS = ['jpg', 'jpeg', 'gif', 'png', 'zip', 'txt']

    class Config:
        """ Loads the dotenv file."""

        env_file: str = '.env'


config = AppConfig()
