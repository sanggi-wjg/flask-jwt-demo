from typing import Callable
from wsgiref.headers import Headers
from flask import _app_ctx_stack as ctx_stack
from flask import request, jsonify

from demo.exceptions import NoAuthorizationError, HeaderError, InvalidAuthorizationFormat
from demo.jwt_builder import decode_jwt


def jwt_required(func: Callable):
    def wrapper(*args, **kwargs):
        try:
            decoded_jwt = get_decoded_jwt_from_header(request.headers)
            print(decoded_jwt)
            ctx_stack.top.jwt = decoded_jwt
        except HeaderError as e:
            return jsonify({ "msg": e.__str__() }), 400

        return func(*args, **kwargs)

    return wrapper


def get_decoded_jwt_from_header(headers: Headers):
    authorization = headers.get('Authorization')
    if not authorization:
        raise NoAuthorizationError('Bad header : Missing Authorization')

    authorization_parts = authorization.split()
    if len(authorization_parts) != 2:
        raise InvalidAuthorizationFormat('Bad header : Invalid Authorization format')

    if authorization_parts[0] != 'Bearer':
        raise InvalidAuthorizationFormat('Bad header : Invalid Authorization user')

    token = authorization_parts[1]
    return decode_jwt(token)
