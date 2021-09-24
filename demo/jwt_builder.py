import jwt

from flask import current_app


class JWTBuilder:

    def __init__(self, userid: str):
        self._userid = userid
        self._app = current_app

    @property
    def userid(self) -> str:
        return self._userid

    @property
    def app(self) -> "Flask":
        return self._app

    def encode(self) -> str:
        time_claims = get_time_claims(self.app.config['JWT_PAYLOAD_EXP_DELTA'])
        encoded_jwt = jwt.encode({
            'sub' : 'Demo-JWT',
            'name': self.userid,
            'iat' : time_claims[0],
            'exp' : time_claims[1],
        }, self.app.config['JWT_SECRET_KEY'], algorithm = 'HS256')
        return encoded_jwt

    def decode(self, encoded_jwt: str) -> dict:
        try:
            decoded_jwt = jwt.decode(encoded_jwt, self.app.config['JWT_SECRET_KEY'], algorithms = ['HS256'])
        except jwt.ExpiredSignatureError:
            raise jwt.ExpiredSignatureError('expired jwt')

        return decoded_jwt
