from pymongo import MongoClient # type: ignore
from pymongo.database import Database # type: ignore
from pymongo.collection import Collection # type: ignore
from .base_database import BaseDatabase
from typing import Dict, Any, List

class MongoDatabase(BaseDatabase):

  def initialize(self) -> None:
    if not self._database_client:
      self._database_client: MongoClient = MongoClient(self._database_url)

  def get_database(
    self,
    database_name: str | None = None
  ) -> Database:
    if not database_name:
      raise Exception('Database name is required.')
    return self._database_client[database_name]

  def get_table(
    self,
    database: Database,
    table_name: str | None = None
  ) -> Collection:
    if not database:
      raise Exception('Database instance is required.')
    if not table_name:
      raise Exception('Table name is required.')
    return database[table_name]

  def find_one(
    self,
    table: Collection | None = None,
    filter: Dict[str, Any] | None = None,
  ) -> Any:
    if not table:
      raise Exception('Table instance is required.')
    if not filter:
      filter = {}
    return table.find_one(filter)

  def find_many(
    self,
    table: Collection | None = None,
    filter: Dict[str, Any] | None = None
  ) -> List[Any]:
    if not table:
      raise Exception('Table instance is required.')
    if not filter:
      filter = {}
    return table.find(filter)

  def insert_one(
    self,
    table: Any | None = None,
    record: Dict[str, Any] | None = None
  ) -> None:
    if not table:
      raise Exception('Table instance is required.')
    if not record:
      raise Exception('Record to insert is required.')
    return table.insert_one(record)

  def insert_many(
    self,
    table: Any | None = None,
    records: List[Dict[str, Any]] | None = None
  ) -> None:
    if not table:
      raise Exception('Table instance is required.')
    if not records:
      raise Exception('Records to insert are required.')
    return table.insert_many(records)

  def delete_one(
    self,
    table: Any | None = None,
    record_id: str | None = None,
  ) -> None:
    if not table:
      raise Exception('Table instance is required.')
    if not record_id:
      raise Exception('Record id is required for deletion')
    return table.delete_one({ '_id': record_id  })

  def delete_many(
    self,
    table: Any | None = None,
    filter: Dict[str, Any] | None = None
  ) -> None:
    if not table:
      raise Exception('Table instance is required.')
    if not filter:
      filter = {}
    return table.delete_many(filter)







