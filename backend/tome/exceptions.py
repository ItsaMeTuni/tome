from typing import Any, Dict, Optional


class HTTPException(Exception):
    """custom HTTPException class supporting custom headers"""

    def __init__(
        self, detail: Any, status_code: int, headers: Optional[Dict[str, str]] = None
    ):
        super(HTTPException, self).__init__()
        self.detail: Any = detail
        self.status_code: int = status_code
        self.headers: Optional[Dict[str, str]] = headers
