import datetime

import jwt.exceptions as jwt_exceptions
from flask_jwt_extended import JWTManager, exceptions as jwt_extended_exceptions

from bolinette import response, env
from bolinette.exceptions import APIError
from bolinette.services import user_service

jwt = JWTManager()


def init_jwt(app):
    app.config['JWT_TOKEN_LOCATION'] = ['cookies']
    app.config['JWT_COOKIE_SECURE'] = False
    app.config['JWT_ACCESS_COOKIE_PATH'] = '/api/'
    app.config['JWT_REFRESH_COOKIE_PATH'] = '/api/user/token/refresh'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = datetime.timedelta(days=30)
    app.config['JWT_COOKIE_CSRF_PROTECT'] = True
    app.config['JWT_SECRET_KEY'] = env['JWT_SECRET_KEY']
    jwt.init_app(app)

    def handle_auth_error(e):
        return response.unauthorized(str(e))

    app.errorhandler(jwt_extended_exceptions.JWTExtendedException)(handle_auth_error)
    app.errorhandler(jwt_exceptions.PyJWTError)(handle_auth_error)


@jwt.user_loader_callback_loader
def user_loader_callback(identity):
    try:
        return user_service.get_by_username(identity)
    except APIError:
        return None


@jwt.unauthorized_loader
def unauthorized(_):
    return response.unauthorized('user.unauthorized')


@jwt.expired_token_loader
def expired_token(_):
    return response.unauthorized('user.token.expired')


@jwt.needs_fresh_token_loader
def need_fresh_token():
    return response.unauthorized('user.token.fresh_required')
