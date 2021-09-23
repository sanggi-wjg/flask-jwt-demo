class HeaderError(Exception):
    pass


class NoAuthorizationError(HeaderError):
    pass
