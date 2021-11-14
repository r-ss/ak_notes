from fastapi_utils.cbv import cbv
from fastapi import status, Depends, HTTPException
from fastapi_utils.inferring_router import InferringRouter
from fastapi.security import OAuth2PasswordRequestForm

from models.user import UserTokenBM

from services.auth import is_username_correct, is_password_correct, token_required, login


from config import Config

router = InferringRouter()


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
            bad_req(Config.AUTH_USERNAME_REGEX['failmessage'])

        if not is_password_correct(form_data.password):
            bad_req(Config.AUTH_PASSWORD_REGEX['failmessage'])

        token = login(form_data.username, form_data.password)

        return {'access_token': token, 'token_type': 'bearer'}

    """ CHECK TOKEN """
    @router.get('/check_token', status_code=status.HTTP_200_OK)
    def check_token(self, token: UserTokenBM = Depends(token_required)):
        return {'token': token}

    """ SECRET PAGE, USED TO ENSURE TOKEN MECHANIC WORKING """
    @router.get('/secretpage', status_code=status.HTTP_200_OK)
    def secretpage(self, token: UserTokenBM = Depends(token_required)):
        return {'message': 'this is secret message'}
