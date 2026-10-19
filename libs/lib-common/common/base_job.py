from abc import ABC, abstractmethod
from typing import Any


class BaseJob(ABC):
  def __init__(
    self, job_name: str | None = None, job_payload: dict[str, Any] | None = None
  ) -> None:
    if not job_name:
      raise Exception("Job name is required.")
    self._job_name = job_name
    self._job_payload = job_payload

  @abstractmethod
  async def execute(self) -> None:
    pass
