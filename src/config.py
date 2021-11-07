import os
# import pytz
from decouple import config

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

PRODUCTION = False

STORAGEROOT = '/storage/'
# if not os.path.isdir(STORAGEROOT):
#     STORAGEROOT = (
#         '/home/ress/ak_notes_storage/'  # in case of running on remote server without Docker
#     )


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
    # TZ = pytz.timezone('Europe/Moscow')

    TESTING_MODE = False  # Must be set to True only in autotests
    TESTING_ASSETS_PATH = (
        '%s/testing_assets/' % os.path.split(STORAGEROOT)[0]
    )  # using in tests

    if PRODUCTION:
        pass

    STORAGE = {
        'ROOT': STORAGEROOT,
        'MEDIA': '%s/media/' % os.path.split(STORAGEROOT)[0]
    }