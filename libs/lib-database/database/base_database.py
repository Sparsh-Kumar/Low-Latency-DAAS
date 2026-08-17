from typing import Any, Dict, List
from abc import ABC, abstractmethod

class BaseDatabase(ABC):

  def __init__(
    self,
    database_url: str | None = None,
  ) -> None:
    if not database_url:
      raise Exception('Database URI is required.')
    self._database_url: str = database_url
    self._database_client: Any = None

  @abstractmethod
  def initialize(self) -> None:
    pass

  @abstractmethod
  def get_database(
    self,
    database_name: str | None = None
  ) -> Any:
    pass

  @abstractmethod
  def get_table(
    self,
    database: Any | None = None,
    table_name: str | None = None
  ) -> Any:
    pass

  @abstractmethod
  def find_one(
    self,
    table: Any | None = None,
    filter: Dict[str, Any] | None = None
  ) -> Any:
    pass

  @abstractmethod
  def find_many(
    self,
    table: Any | None = None,
    filter: Dict[str, Any] | None = None
  ) -> List[Any]:
    pass

  @abstractmethod
  def insert_one(
    self,
    table: Any | None = None,
    record: Dict[str, Any] | None = None
  ) -> None:
    pass

  @abstractmethod
  def insert_many(
    self,
    table: Any | None = None,
    records: List[Dict[str, Any]] | None = None
  ) -> None:
    pass

  @abstractmethod
  def delete_one(
    self,
    table: Any | None = None,
    filter: Dict[str, Any] | None = None
  ) -> None:
    pass

  @abstractmethod
  def delete_many(
    self,
    table: Any | None = None,
    filter: Dict[str, Any] | None = None
  ) -> None:
    pass

