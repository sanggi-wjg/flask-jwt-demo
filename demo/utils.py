import datetime

from demo.jwt_builder import JWTBuilder


def encode_jwt(userid: str) -> str:
    jwt_builder = JWTBuilder(userid)
    return jwt_builder.encode()


def get_time_claims(delta: int):
    def datetime_to_string(target_datetime: datetime, date_format: str = "%Y-%m-%d %H:%M:%S"):
        return target_datetime.strftime(date_format)

    now = datetime.datetime.now()
    exp = now + datetime.timedelta(hours = delta)
    return datetime_to_string(now), datetime_to_string(exp)
