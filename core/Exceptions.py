__author__ = 'kitru'

class AstroException(Exception):
    def __init__(self, msg, logger=None):
        Exception.__init__(self, msg)
        if logger:
            logger.exception(msg)

class ConfigurationException(AstroException):
    """Exception raised for errors during configuration system.
    Attributes:
        msg  -- explanation of the error
    """

    def __init__(self, msg, logger=None):
        AstroException.__init__(self, msg, logger)


class InitializationException(AstroException):
    """Exception raised for errors during system initialization.
    Attributes:
        msg  -- explanation of the error
    """

    def __init__(self, msg, logger=None):
        AstroException.__init__(self, msg, logger)


class ClosingException(AstroException):
    """Exception raised for errors during system closing.
    Attributes:
        msg  -- explanation of the error
    """

    def __init__(self, msg, logger=None):
        AstroException.__init__(self, msg, logger)


class DbException(AstroException):
    """Exception raised if Db return Exception.
    Attributes:
        msg  -- explanation of the error
    """

    def __init__(self, msg, logger=None):
        AstroException.__init__(self, msg, logger)

class GuiException(AstroException):
    """Exception raised if GUI return Exception.
    Attributes:
        msg  -- explanation of the error
    """

    def __init__(self, msg, logger=None):
        AstroException.__init__(self, msg, logger)
