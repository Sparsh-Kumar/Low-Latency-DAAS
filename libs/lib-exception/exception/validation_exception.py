from .base_exception import BaseException

class ValidationException(BaseException):
  def __init__(self, message: str = '') -> None:
    self.status: int = 400
    super().__init__(message)

