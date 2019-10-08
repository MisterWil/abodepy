"""The exceptions used by AbodePy."""


class AbodeException(Exception):
    """Class to throw general abode exception."""

    def __init__(self, error, details=None):
        """Initialize AbodeException."""
        # Call the base class constructor with the parameters it needs
        super(AbodeException, self).__init__(error[1])

        self.errcode = error[0]
        self.message = error[1]
        self.details = details


class AbodeAuthenticationException(AbodeException):
    """Class to throw authentication exception."""


class SocketIOException(AbodeException):
    """Class to throw SocketIO Error exception."""
