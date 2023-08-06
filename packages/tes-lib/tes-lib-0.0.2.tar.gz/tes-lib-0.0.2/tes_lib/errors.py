"""Error types used by the library"""


class TesLibError(RuntimeError):
    """Raised when an expected library error occurs"""

    pass


class EventNotFoundError(AssertionError):
    """Raised when an expected event was not found"""

    pass


class UnexpectedEventFoundError(AssertionError):
    """Raised when an unexpected event is found"""

    pass
