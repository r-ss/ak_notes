from fastapi_utils.cbv import cbv
from fastapi import status, Depends, HTTPException
from fastapi_utils.inferring_router import InferringRouter
from fastapi.security import OAuth2PasswordRequestForm

from models.user import UserTokenBM

from services.users.auth import is_username_correct, is_password_correct, token_required, login


from config import config

router = InferringRouter(tags=['Authentication'])


@cbv(router)
class AuthCBV:

    """ LOGIN """
    @router.post('/token', status_code=status.HTTP_202_ACCEPTED)
    def login(self, form_data: OAuth2PasswordRequestForm = Depends()):

        def bad_req(msg: str):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=msg)

        if not form_data.password or not form_data.username:
            bad_req('Username and password must be provided for login')

        if not is_username_correct(form_data.username):
            bad_req(config.AUTH_USERNAME_REGEX['failmessage'])

        if not is_password_correct(form_data.password):
            bad_req(config.AUTH_PASSWORD_REGEX['failmessage'])

        token = login(form_data.username, form_data.password)

        return {'access_token': token, 'token_type': 'bearer'}


    """ SECRET PAGE, USED IN TESTS TO ENSURE TOKEN MECHANIC WORKING """
    @router.get('/secretpage', status_code=status.HTTP_200_OK, summary='Works only within tests')
    def secretpage(self, token: UserTokenBM = Depends(token_required)):

        if not config.TESTING_MODE:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You shall not pass!')


        return {'message': 'this is secret message'}
