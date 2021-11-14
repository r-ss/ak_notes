# Singleton - https://stackoverflow.com/questions/42237752/single-instance-of-class-in-python
from datetime import datetime

from config import Config


def singleton(cls, *args, **kw):
    instances = {}

    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]

    return _singleton


@singleton
class RessLogger(object):
    @property
    def time(self) -> str:
        return datetime.utcnow().strftime(Config.DATETIME_FORMAT_HUMAN)

    def info(self, msg) -> None:
        if not Config.TESTING_MODE:
            print('resslogger, %s - info - %s' % (self.time, msg))
