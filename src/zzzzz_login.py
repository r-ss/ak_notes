import datetime
from re import compile

import bcrypt
import jwt

from config import Config

import mongoengine
from mongoengine.queryset.visitor import Q as mongo_Q

from models.user import User

from resslogger import RessLogger
log = RessLogger()

USERNAME_REGEX = compile(r'\A[\w\-\.]{4,}\Z')
PASSWORD_REGEX = compile(r'\A[\w\-\.]{6,}\Z')

# checking username for valid characters
def username_pass_regex(username):
    return USERNAME_REGEX.match(username) is not None
def password_pass_regex(password):
    return PASSWORD_REGEX.match(password) is not None


class UserRegister:

    def post(self):
        data = request.get_json()['data']
        username = data['username']
        password = data['password'] 
        # email = data['email']


        if not username_pass_regex(username):
            return {
                'auth': False,
                'message': 'Username must be at least 3 alphanumeric characters long & may contain . - _ chars.'
            }, 401  # return data with 401 Unauthorized
        if not password_pass_regex(password):
            return {
                'auth': False,
                'message': 'Password must at least 4 chars and may contain . - _ symbols'
            }, 401  # return data with 401 Unauthorized

        passwd = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(passwd, salt).decode('utf-8')

        user = User(
            username = username,
            userhash = hashed
        )

        try:
            user.save()
        except mongoengine.errors.NotUniqueError:
            return {
                'auth': False,
                'message': 'That user already exist'
            }, 401  # return data with 401 Unauthorized

        log.info(f'User { username } has been registered')

        return {
            # 'result': 'user registered %s' % user['username'],
            'result': 'user registered',
            'username': username
        }, 200  # return data with 200 OK

class Login():

    def post(self):
        data = request.get_json()['data']
        username = data['username']
        password = data['password']     

        # TODO - .casefold() on username

        if not username_regex(username):
            return {
                'auth': False,
                'message': 'Username must be at least 3 alphanumeric characters long & may contain . - _ chars.'
            }, 401  # return data with 401 Unauthorized
        if not password_regex(password):
            return {
                'auth': False,
                'message': 'Password must at least 4 chars and may contain . - _ symbols'
            }, 401  # return data with 401 Unauthorized

        try:
            #user = User.objects(username = username)[0]
            user = User.objects.filter( mongo_Q(username = username) | mongo_Q(email = username) )[0]
            # print(user.id)
            # db.users.find( { $or: [ { tickect_number: 547 }, { winner: true } ] } );
        except IndexError:
            return {
                'auth': False,
                'message': 'User does not found'
            }, 400 

        # drop if user is banned
        if user.is_disabled:
            return {
                'auth': False,
                'message': 'User is disabled'
            }, 401 

        if bcrypt.checkpw(password.encode('utf-8'), user.userhash.encode('utf-8')):
#           salt = bcrypt.gensalt()
#           hashed = bcrypt.hashpw(user.username.encode('utf-8'), salt).decode('utf-8')

            timeLimit = datetime.datetime.utcnow() + datetime.timedelta(days=30) # set limit for user, can use utcnow() instead
            payload = { 'username': user.username, 'is_superadmin': user.is_superadmin, 'userid': str( user.id ), 'exp': timeLimit}
            # logger.info(payload)
            token = jwt.encode(payload, Config.SECRET_KEY, algorithm='HS256')

            user.lastactive = datetime.datetime.utcnow()
            user.save()

            log.info(f'User { user.username } logged in')

            return {
                'auth': True,
                'token': token, # token.decode('utf-8')
                'user': user.to_json(),
                'token_expires_at': f'{timeLimit}'
            }, 200  # return data with 200 OK
        else:
            return {
                'auth': False,
                'message': 'Wrong password'
            }, 401  # return data with 401 Unauthorized


class CheckToken():

    def post(self):
        # logger.info(request.headers)
        data = request.get_json()['data']
        token = data['token']

        try:
            decoded_data = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
        except jwt.exceptions.ExpiredSignatureError:
            return {
                'auth': False,
                'message': 'Token has expired'
            }, 401  # return data with 401 Unauthorized
        except:
            return {
                'auth': False,
                'message': 'Invalid Token'
            }, 401  # return data with 401 Unauthorized

        return {
            'resource': 'CheckToken',
            'token_username': decoded_data['username'],
            'token_expires': datetime.datetime.fromtimestamp(decoded_data['exp']).strftime("%d %B %Y %H:%M:%S"),
        }, 200  # return data with 200 OK

# decorator
def token_required(something):
    def wrap(*args, **kwargs):

        token = None
        # print(request.headers)

        try:
            token = request.headers['Authorization']
        except:
            try:
                token = request.get_json()['token']
            except:
                # print('many exceptions... login.py')
                return {'message': 'token required'}, 401

        # log.info(request.headers)
        # log.info('TOKEN PRESENT:' + token)

        if token:
            try:
                tokendata = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
                # kwargs['tokendata'] = 'SEX'
                # print(data)
                
            except jwt.exceptions.ExpiredSignatureError:
                return {'message': 'token has expired'}, 401
            except jwt.exceptions.InvalidTokenError:
                return {'message': 'invalid token'}, 401
            # except Exception as e:
            #     logger.info(e)
            #     return {'message': 'token invalid'}, 401

            return something(tokendata, *args, **kwargs)

        else:
            return {'message': 'token required'}, 401

    return wrap

class CheckClosed():
    @token_required # Verify token decorator
    def get(tokendata, self):
        return {'message': 'this is secret message'}, 200  # return data and 200 OK