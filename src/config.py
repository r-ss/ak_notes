import os
from decouple import config

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

PRODUCTION = True

STORAGEROOT = '/storage/'
if not os.path.isdir(STORAGEROOT):
    PRODUCTION = False
    STORAGEROOT = '%s/storage/' % os.path.split(BASE_DIR)[0]

# import pytz
# TZ = pytz.timezone('Europe/Moscow')


class Config(object):

    # GENERAL SETTINGS AND HOSTS
    BASE_DIR = BASE_DIR
    PRODUCTION = PRODUCTION
    DEBUG = not PRODUCTION
    SECRET_KEY = config('SECRET_KEY')  # we don't use secret_key in application, but it's used in tests to ensure that secrets file exist and loads properly
    DBHOST = config('DBHOST_DEV')

    # TESTS
    # TODO - move test users credentials into a secrets, for now they presented here for simplicity
    TESTING_MODE = False  # Must be set to True only in autotests
    TESTING_ASSETS_PATH = '%s/testing_assets/' % os.path.split(BASE_DIR)[0]
    TESTUSER_ALICE = {'username': 'Alice', 'password': config('TESTUSER_ALICE_PASSWORD', default='nopassword')}  # Regular user, only for tests
    TESTUSER_BOB = {'username': 'Bob', 'password': config('TESTUSER_BOB_PASSWORD', default='nopassword')}  # Another regular user, used to check ownership
    TESTUSER_SUPER = {'username': 'Jesus', 'password': config('TESTUSER_SUPER_PASSWORD', default='nopassword')}  # Admin user, only for tests - is_superadmin is set in database
    TESTNOTE_BY_ALICE_UUID = '7bee43e5-e7e3-4be3-8a35-0f9ce3cd884b'  # used in tests
    CODECLIMATE_TEST_REPORTER_ID = config('CODECLIMATE_TEST_REPORTER_ID', default='not available')

    # FORMATTERS
    DATETIME_FORMAT_TECHNICAL = '%Y-%m-%d %H:%M:%S'
    DATETIME_FORMAT_HUMAN = '%d.%m.%Y %H:%M'

    # PATHS
    STORAGE = {'ROOT': STORAGEROOT, 'UPLOADS': '%s/uploads/' % os.path.split(BASE_DIR)[0]}

    # AUTHENTICATION
    AUTH_USERNAME = {
        'regex': r'\A[\w\-\.]{3,}\Z',
        'failmessage': 'Username must be at least 3 characters and may contain . - _ chars.'  # also can be used as hint
    }
    AUTH_PASSWORD = {
        'regex': r'\A[\w\-\.]{6,}\Z',
        'failmessage': 'Password must at least 6 characters and may contain . - _ symbols'  # also can be used as hint
    }
    AUTH_HASHING_ALGORITHM = 'HS256'  # algorithm to encode/decode JWT user tokens



    # MISC
    HASH_DIGEST_SIZE = 8  # for hashing files with blake2b

    # ALLOWED_UPLOADS = ['jpg', 'jpeg', 'gif', 'png', 'zip', 'txt']
