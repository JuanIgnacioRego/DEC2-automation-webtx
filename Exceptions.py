class BaseError(Exception):
    pass

class TxNotFoundInSACError(BaseError):
    """Exception raised when a tx is looked for in SAC but is not found."""
    pass

