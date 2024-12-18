class CustomHTTPException(Exception):
    def __init__(
        self,
        status_code: int,
        success: bool = False,
        message: str = "",
    ):
        self.status_code = status_code
        self.success = success
        self.message = message
