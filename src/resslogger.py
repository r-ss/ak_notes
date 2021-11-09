
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

    dtformat = '%d.%m.%Y %H:%M:%S'

    @property
    def time(self) -> str:
        return datetime.utcnow().strftime(self.dtformat)

    def info(self, msg) -> None:
        if not Config.TESTING_MODE:
            print('resslogger, %s - info - %s' % (self.time, msg))

            # if Config.PRODUCTION:
            #     if not 'by user ress' in msg: # don't send telegram for actions made by myself
            #         try:
            #             sendTelegram(msg)
            #         except:
            #             pass

    # def error(self, msg):
    #     dt = datetime.now().strftime(self.dtformat)     
    #     print('mylog, %s - error - %s' % (dt, msg))
    
