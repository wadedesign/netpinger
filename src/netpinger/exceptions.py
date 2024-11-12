class NetPingerError(Exception):
    """Base exception for all netpinger errors."""
    pass

class QueryError(NetPingerError):
    """Raised when there's an error querying the server."""
    pass

class TimeoutError(NetPingerError):
    """Raised when the query times out."""
    pass 