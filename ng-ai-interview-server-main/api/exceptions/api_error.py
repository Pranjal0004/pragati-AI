class APIError(Exception):
    """Base API error"""
    def __init__(self, message: str, code: str = "500"):
        self.message = message
        self.code = code
        super().__init__(self.message)

class ValidationError(APIError):
    """Validation error"""
    def __init__(self, message: str):
        super().__init__(message=message, code="400")

class NotFoundError(APIError):
    """Resource not found error"""
    def __init__(self, message: str):
        super().__init__(message=message, code="404")

class DuplicateError(APIError):
    """Duplicate resource error"""
    def __init__(self, message: str):
        super().__init__(message=message, code="409") 