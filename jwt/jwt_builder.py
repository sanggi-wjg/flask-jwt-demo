import base64
import datetime
import hashlib
import hmac
import json

from flask import current_app


class JWTBuilder(object):

    def __init__(self, userid: str):
        self._userid = userid
        self._app = current_app

    @property
    def userid(self) -> str:
        return self._userid

    @property
    def app(self) -> "Flask":
        return self._app

    def _create_header(self) -> str:
        return dict_to_base64_url_encode({
            "alg": self.app.config['JWT_HEADER_ALG'],
            "typ": self.app.config['JWT_HEADER_TYP'],
        })

    def _create_payload(self) -> str:
        time_claims = get_time_claims(self.app.config['JWT_PAYLOAD_EXP_DELTA'])

        return dict_to_base64_url_encode({
            'sub' : 'Demo-JWT',
            'name': self.userid,
            'iat' : time_claims[0],
            'exp' : time_claims[1],
        })

    def create(self) -> str:
        header = self._create_header()
        payload = self._create_payload()
        signature = hmac_signature(f"{header}.{payload}.", self.app.config['JWT_SECRET_KEY'])
        print(f"{header}.{payload}.{signature}")
        return f"{header}.{payload}.{signature}"


def create_jwt(userid: str) -> str:
    jwt_builder = JWTBuilder(userid)
    return jwt_builder.create()


def dict_to_base64_url_encode(data: dict) -> str:
    json_string = json.dumps(data)
    return base64.urlsafe_b64encode(bytes(json_string, 'utf-8')).decode('utf-8')


def get_time_claims(delta: int):
    def datetime_to_string(target_datetime: datetime, date_format: str = "%Y-%m-%d %H:%M:%S"):
        return target_datetime.strftime(date_format)

    now = datetime.datetime.now()
    exp = now - datetime.timedelta(hours = delta)
    return datetime_to_string(now), datetime_to_string(exp)


def hmac_signature(message: str, secret_key: str):
    message += f"{secret_key}"
    return hmac.new(
        bytes(secret_key, 'utf-8'),
        msg = bytes(message, 'utf-8'),
        digestmod = hashlib.sha256
    ).hexdigest().upper()
