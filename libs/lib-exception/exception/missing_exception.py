from .base_exception import BaseException

class MissingException(BaseException):
  def __init__(self, message: str = '') -> None:
    self.status: int = 404
    super().__init__(message)



