class BaseError(Exception):
    pass

class TxNotFoundInSACError(BaseError):
    """Exception raised when a tx is looked for in SAC but is not found."""
    pass

class URLStatusCodeNot200Exception(BaseError):
    """Exception raised when requests.get() tries to reach a URL and
    its status code is not 200."""
    pass

