from dataclasses import dataclass
from datetime import datetime
from typing import Any, Union, Mapping, Sequence, Optional
import enum

"""
HTTP request or response headers. Array-valued header values can be represented with a comma-separated string.
"""
Headers = Mapping[str, Union[str, Sequence[str]]]

"""
HTTP request query parameters.
"""
Query = Mapping[str, Union[str, Sequence[str]]]

"""
HTTP request protocol.
"""


class Protocol(enum.Enum):
    HTTP = "http"
    HTTPS = "https"


"""
HTTP method.
"""


class HttpMethod(enum.Enum):
    GET = "get"
    PUT = "put"
    POST = "post"
    PATCH = "patch"
    DELETE = "delete"
    OPTIONS = "options"
    TRACE = "trace"
    HEAD = "head"
    CONNECT = "connect"


@dataclass
class Request:
    """
    HTTP request.
    """

    """
    HTTP request body as JSON. Could be dictionary, list, or string.
    """
    bodyAsJson: Optional[Any]

    """
    Timestamp when the request was initiated.
    """
    timestamp: Optional[datetime]

    """
    Request method.
    """
    method: HttpMethod

    """
    Request headers.
    """
    headers: Headers

    """
    Query parameters.
    """
    query: Query

    """
    Request body. Empty string if empty.
    """
    body: str

    """
    Request host, possibly including port number.
    """
    host: str

    """
    Full request path.
    Example value: '/v1/pets?id=234'
    """
    path: str

    """
    Request pathname, not containing query parameters etc.
    Example value: '/v1/pets'
    """
    pathname: str

    """
    Request protocol.
    """
    protocol: Protocol


@dataclass
class Response:
    """
    HTTP response.
    """

    """
    Response body as JSON. Could be dictionary, list, or string.
    """
    bodyAsJson: Optional[Any]

    """
    Timestamp when the response was sent.
    """
    timestamp: Optional[datetime]

    """
    Response body.
    """
    body: str

    """ Response status code."""
    statusCode: int

    """ Response headers. """
    headers: Headers


@dataclass
class HttpExchange:
    """
    HTTP request-response pair.
    """

    request: Request
    response: Response


__all__ = [
    "Request",
    "Response",
    "HttpExchange",
    "Headers",
    "Query",
    "Protocol",
    "HttpMethod",
]
