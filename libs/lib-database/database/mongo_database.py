from typing import Any

from pymongo import MongoClient  # type: ignore
from pymongo.collection import Collection  # type: ignore
from pymongo.database import Database  # type: ignore

from .base_database import BaseDatabase


class MongoDatabase(BaseDatabase):
  def initialize(self) -> None:
    if not self._database_client:
      self._database_client: MongoClient = MongoClient(self._database_url)

  def get_database(self, database_name: str | None = None) -> Database:
    if not database_name:
      raise Exception("Database name is required.")
    database_instance: Database = self._database_client.get(database_name, None)
    if not database_instance:
      raise Exception(f"No database exists with database name = {database_name}.")
    return database_instance

  def get_table(self, database: Database, table_name: str | None = None) -> Collection:
    if not database:
      raise Exception("Database instance is required.")
    if not table_name:
      raise Exception("Table name is required.")
    table_instance = database.get(table_name, None)
    if not table_instance:
      raise Exception(f"No table exists with name = {table_name}.")
    return table_instance

  def find_one(
    self,
    table: Collection | None = None,
    filter: dict[str, Any] | None = None,
  ) -> Any:
    if not table:
      raise Exception("Table instance is required.")
    if not filter:
      filter = {}
    return table.find_one(filter)

  def find_many(
    self, table: Collection | None = None, filter: dict[str, Any] | None = None
  ) -> list[Any]:
    if not table:
      raise Exception("Table instance is required.")
    if not filter:
      filter = {}
    return table.find(filter)

  def insert_one(self, table: Any | None = None, record: dict[str, Any] | None = None) -> None:
    if not table:
      raise Exception("Table instance is required.")
    if not record:
      raise Exception("Record to insert is required.")
    return table.insert_one(record)

  def insert_many(
    self, table: Any | None = None, records: list[dict[str, Any]] | None = None
  ) -> None:
    if not table:
      raise Exception("Table instance is required.")
    if not records:
      raise Exception("Records to insert are required.")
    return table.insert_many(records)

  def delete_one(
    self,
    table: Any | None = None,
    record_id: str | None = None,
  ) -> None:
    if not table:
      raise Exception("Table instance is required.")
    if not record_id:
      raise Exception("Record id is required for deletion.")
    return table.delete_one({"_id": record_id})

  def delete_many(self, table: Any | None = None, filter: dict[str, Any] | None = None) -> None:
    if not table:
      raise Exception("Table instance is required.")
    if not filter:
      filter = {}
    return table.delete_many(filter)
