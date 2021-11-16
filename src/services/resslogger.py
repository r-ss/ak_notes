# Singleton - https://stackoverflow.com/questions/42237752/single-instance-of-class-in-python
from datetime import datetime

from config import config


def singleton(cls, *args, **kw):
    instances = {}

    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]

    return _singleton


@singleton
class RessLogger(object):
    """ For now, it's just wrapper for print function to debug, but later... it can send telegram messages :) """

    @property
    def time(self) -> str:
        return datetime.utcnow().strftime(config.DATETIME_FORMAT_HUMAN)

    def info(self, msg) -> None:
        if not config.TESTING_MODE:
            print('resslogger, %s - info - %s' % (self.time, msg))
