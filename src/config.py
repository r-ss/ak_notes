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


# # print(socket.gethostname())
# if socket.gethostname() in ['ress-mpb.local']:
#     # logger.info('hostname: ' + socket.gethostname())
#     PRODUCTION = False
#     STORAGEROOT = '/Users/ress/dev/storage/'


class Config(object):
    BASE_DIR = BASE_DIR
    PRODUCTION = PRODUCTION
    DEBUG = not PRODUCTION
    SECRET_KEY = config('SECRET_KEY') # we don't use secret_key in application, but it's used in tests to ensure that secrets file exist and loads properly
    DBHOST = config('DBHOST_DEV')
    

    TESTING_MODE = False  # Must be set to True only in autotests
    TESTING_ASSETS_PATH = (
        '%s/testing_assets/' % os.path.split(BASE_DIR)[0]
    )

    DATETIME_FORMAT_TECHNICAL = '%Y-%m-%d %H:%M:%S'
    DATETIME_FORMAT_HUMAN = '%d.%m.%Y %H:%M'

    if PRODUCTION:
        pass

    ALLOWED_UPLOADS = ['jpg', 'jpeg', 'gif', 'png', 'zip', 'txt']

    STORAGE = {
        'ROOT': STORAGEROOT,
        'UPLOADS': '%s/uploads/' % os.path.split(BASE_DIR)[0]
    }