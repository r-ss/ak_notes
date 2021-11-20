from fastapi_utils.cbv import cbv
from fastapi import status, Depends, HTTPException
from fastapi_utils.inferring_router import InferringRouter
from fastapi.security import OAuth2PasswordRequestForm

from models.user import UserTokenBM

from services.users.auth import Auth, token_required


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

        if not Auth.is_username_valid(form_data.username):
            bad_req(config.AUTH_USERNAME_REGEX['failmessage'])

        if not Auth.is_password_valid(form_data.password):
            bad_req(config.AUTH_PASSWORD_REGEX['failmessage'])

        user, access_token, refresh_token = Auth.login(form_data.username, form_data.password)

        return {
            'username': user.username,
            'uuid': user.uuid,
            'access_token': access_token,
            'refresh_token': refresh_token,
            'token_type': 'bearer'
        }

    """ REFRESH TOKEN """
    @router.post('/refresh-token', status_code=status.HTTP_202_ACCEPTED)
    def refresh_token(self, refresh_token: str):



        new_access_token, new_refresh_token = Auth.check_refresh_token(refresh_token)

        return {
            'access_token': new_access_token,
            'refresh_token': new_refresh_token,
        }


    # """ SECRET PAGE, USED IN TESTS TO ENSURE TOKEN MECHANIC WORKING """
    # @router.get('/secretpage', status_code=status.HTTP_200_OK, summary='Works only within tests')
    # def secretpage(self, token: UserTokenBM = Depends(token_required)):

    #     if not config.TESTING_MODE:
    #         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You shall not pass!')


    #     return {'message': 'this is secret message'}

