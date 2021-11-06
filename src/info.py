from datetime import datetime
import os
import platform

from config import Config

class Info():

    def get(self):

        load1, load5, load15 = os.getloadavg()

        return {
            'resource': 'ak_notes, info',
            'datetime': datetime.now().strftime('%d %B %Y %H:%M:%S'),
            'os': os.name,
            'platform': platform.system(),
            'platform_release': platform.release(),
            'python version': platform.python_version(),
            'testing': Config.TESTING_MODE,
            'production': Config.PRODUCTION,
            'load averages': f'{load1:.2f} {load5:.2f} {load15:.2f}'
        }
