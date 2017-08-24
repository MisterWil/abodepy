"""The exceptions used by AbodePy."""


class AbodeException(Exception):
    """Class to throw general abode exception."""

    def __init__(self, error, details=None):
        """Initialize AbodeException."""
        self.errcode = error[0]
        self.message = error[1]
        self.details = details


class AbodeAuthenticationException(AbodeException):
    """Class to throw authentication exception."""

    pass
