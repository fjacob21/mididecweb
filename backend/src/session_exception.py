class SessionError(Exception):
    """Exception raised for errors in the session handling.

    Attributes:
        code -- The error code
    """

    def __init__(self, code):
        self.code = code
