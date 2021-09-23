class HeaderError(Exception):
    pass


class NoAuthorizationError(HeaderError):
    pass


class InvalidAuthorizationFormat(HeaderError):
    pass
