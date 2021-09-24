import datetime
from typing import Tuple

import jwt

from flask import _app_ctx_stack as ctx_stack
from flask import current_app, request


class JWTBuilder:

    def __init__(self, name: str):
        self._name = name
        self._app = current_app

    @property
    def name(self) -> str:
        return self._name

    @property
    def app(self) -> "Flask":
        return self._app

    def encode(self) -> str:
        time_claims = get_time_claims(self.app.config['JWT_PAYLOAD_EXP_DELTA'])
        encoded_jwt = jwt.encode({
            'sub' : 'Demo-JWT',
            'name': self.name,
            'jti' : self.name,
            'iat' : time_claims[0],
            'exp' : time_claims[1],
            'iss' : request.host_url,
        }, self.app.config['JWT_SECRET_KEY'], algorithm = 'HS256')
        return encoded_jwt


def encode_jwt(userid: str) -> str:
    jwt_builder = JWTBuilder(userid)
    return jwt_builder.encode()


def decode_jwt(encoded_jwt: str) -> str:
    try:
        decoded_jwt = jwt.decode(
            encoded_jwt, current_app.config['JWT_SECRET_KEY'],
            algorithms = ['HS256']
        )
    except jwt.ExpiredSignatureError:
        raise jwt.ExpiredSignatureError('expired jwt')

    return decoded_jwt


def get_time_claims(delta: int) -> Tuple[float, float]:
    def datetime_to_string(target_datetime: datetime, date_format: str = "%Y-%m-%d %H:%M:%S") -> str:
        return target_datetime.strftime(date_format)

    now = datetime.datetime.now()
    exp = now + datetime.timedelta(hours = delta)
    return now.timestamp(), exp.timestamp()


def get_jwt_identity():
    jwt = getattr(ctx_stack.top, 'jwt')
    return jwt.get('jti')
