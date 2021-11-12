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
    SECRET_KEY = config('SECRET_KEY') # we don't use secret_key in application, but it's used in tests to ensure that secrets file exist and loads properly
    DBHOST = config('DBHOST_DEV')
    
    # TESTS
    # TODO - move test users credentials into a secrets, for now they presented here for simplicity
    TESTING_MODE = False  # Must be set to True only in autotests
    TESTING_ASSETS_PATH = (
        '%s/testing_assets/' % os.path.split(BASE_DIR)[0]
    )
    TESTUSER = {'username':'testuser','password':'5pRHsDMXJCQ4'} # Regular user, only for tests
    TESTUSER_SUPER = {'username':'testsuperuser','password':'jePGE76QVFZY'} # Admin user, only for tests
    CODECLIMATE_TEST_REPORTER_ID = config('CODECLIMATE_TEST_REPORTER_ID')

    # FORMATTERS
    DATETIME_FORMAT_TECHNICAL = '%Y-%m-%d %H:%M:%S'
    DATETIME_FORMAT_HUMAN = '%d.%m.%Y %H:%M'

    ALLOWED_UPLOADS = ['jpg', 'jpeg', 'gif', 'png', 'zip', 'txt']

    STORAGE = {
        'ROOT': STORAGEROOT,
        'UPLOADS': '%s/uploads/' % os.path.split(BASE_DIR)[0]
    }