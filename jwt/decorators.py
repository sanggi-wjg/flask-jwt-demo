from typing import Callable
from wsgiref.headers import Headers

from flask import request, jsonify

from jwt.exceptions import NoAuthorizationError, HeaderError, InvalidAuthorizationFormat


def jwt_required(func: Callable):
    def wrapper(*args, **kwargs):
        try:
            _check_jwt(request.headers)
        except HeaderError as e:
            return jsonify({ "msg": e.__str__() }), 400

        return func(*args, **kwargs)

    return wrapper


def _check_jwt(headers: Headers):
    authorization = headers.get('Authorization')
    if not authorization:
        raise NoAuthorizationError('Bad header : Missing Authorization')

    authorization_parts = authorization.split()
    if len(authorization_parts) != 2:
        raise InvalidAuthorizationFormat('Bad header : Invalid Authorization format')

    if authorization_parts[0] != 'Bearer':
        raise InvalidAuthorizationFormat('Bad header : Invalid Authorization user')
