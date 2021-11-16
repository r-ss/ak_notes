from datetime import datetime
import os
import platform

from fastapi import status
from fastapi_utils.cbv import cbv
from fastapi.responses import JSONResponse
from fastapi_utils.inferring_router import InferringRouter

from config import config

router = InferringRouter(tags=['General'])


@cbv(router)
class InfoCBV:

    """ READ """
    @router.get('/info')
    def read(self):
        """ Return basic system information and variables, like is app runs
            in production mode or not. Might be useful on deployment.
            Can be used for fast status check in production

            access via /info url
        """

        load1, load5, load15 = os.getloadavg()

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                'resource': 'ak_notes, info',
                'datetime': datetime.now().strftime('%d %B %Y %H:%M:%S'),
                'os': os.name,
                'platform': platform.system(),
                'platform_release': platform.release(),
                'python version': platform.python_version(),
                'testing': config.TESTING_MODE,
                'production': config.PRODUCTION,
                'load averages': f'{load1:.2f} {load5:.2f} {load15:.2f}'
            }
        )
