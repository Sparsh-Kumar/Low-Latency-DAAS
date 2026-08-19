import psycopg # type: ignore
from psycopg import Connection, sql # type: ignore
from .base_database import BaseDatabase
from .types import PostgresTable
from typing import Dict, Any, List

class PostgresDatabase(BaseDatabase):

  def initialize(self) -> None:
    if not self._database_client:
      self._database_client = psycopg.connect(
        self._database_url
      )

  def get_database(
    self,
    database_name: str | None = None
  ) -> Connection:
    if not database_name:
      raise Exception('Database name is required.')
    return self._database_client

  def get_table(
    self,
    database: Connection | None = None,
    table_name: str | None = None
  ) -> PostgresTable:
    if not database:
      raise Exception('Database instance is required.')
    if not table_name:
      raise Exception('Table name is required.')
    return PostgresTable(
      database=database,
      table_name=sql.Identifier(table_name)
    )

  def find_one(
    self,
    table: PostgresTable | None = None,
    filter: Dict[str, Any] | None = None,
  ) -> Any:
    if not table:
      raise Exception('Table instance is required.')
    if not filter:
      filter = {}
    query = sql.SQL("SELECT * FROM {}").format(
      table.table_name
    )
    params: List[Any] = []
    if filter:
      conditions: List[sql.Composable] = []
      for column, value in filter.items():
        conditions.append(
          sql.SQL("{} = %s").format(
            sql.Identifier(column)
          )
        )
        params.append(value)
      query += sql.SQL(" WHERE ") + sql.SQL(" AND ").join(conditions)
    query += sql.SQL(" LIMIT 1 ")
    cursor = table.database.execute(
      query,
      params,
    )
    return cursor.fetchone()

  def find_many(
    self,
    table: PostgresTable | None = None,
    filter: Dict[str, Any] | None = None,
  ) -> Any:
    if not table:
      raise Exception('Table instance is required.')
    if not filter:
      filter = {}
    query = sql.SQL("SELECT * FROM {}").format(
      table.table_name
    )
    params: List[Any] = []
    if filter:
      conditions: List[sql.Composable] = []
      for column, value in filter.items():
        conditions.append(
          sql.SQL("{} = %s").format(
            sql.Identifier(column)
          )
        )
        params.append(value)
      query += sql.SQL(" WHERE ") + sql.SQL(" AND ").join(conditions)
    cursor = table.database.execute(
      query,
      params,
    )
    return cursor.fetchall()

  def insert_one(
    self,
    table: PostgresTable | None = None,
    record: Dict[str, Any] | None = None
  ) -> None:
    if not table:
      raise Exception('Table instance is required.')
    if not record:
      raise Exception('Record to insert is required.')
    columns = [
      sql.Identifier(column)
      for column in record.keys()
    ]
    placeholders = [
      sql.Placeholder()
      for _ in record
    ]
    query = sql.SQL(
      "INSERT INTO {} ({}) VALUES ({})"
    ).format(
      table.table_name,
      sql.SQL(", ").join(columns),
      sql.SQL(", ").join(placeholders),
    )
    table.database.execute(
      query,
      list(record.values())
    )
    table.database.commit()

  def insert_many(
    self,
    table: PostgresTable | None = None,
    records: List[Dict[str, Any]] | None = None
  ) -> None:
    if not table:
      raise Exception('Table instance is required.')
    if not records:
      raise Exception('Record to insert is required.')
    column_names = list(records[0].keys())
    columns = [
      sql.Identifier(column)
      for column in column_names
    ]
    placeholders = [
      sql.Placeholder()
      for _ in column_names
    ]
    query = sql.SQL(
      "INSERT INTO {} ({}) VALUES ({})"
    ).format(
      table.table_name,
      sql.SQL(", ").join(columns),
      sql.SQL(", ").join(placeholders)
    )
    values = [
      [record[column] for column in column_names]
      for record in records
    ]
    with table.database.cursor() as cursor:
      cursor.executemany(
        query,
        values
      )
    table.database.commit()

  def delete_one(
    self,
    table: PostgresTable | None = None,
    record_id: str | None = None,
  ) -> None:
    if not table:
      raise Exception('Table instance is required.')
    if not record_id:
      raise Exception('Record id is required for deletion')
    query = sql.SQL(
      "DELETE FROM {} WHERE {} = %s"
    ).format(
      table.table_name,
      sql.Identifier("id")
    )
    table.database.execute(
      query,
      [record_id]
    )
    table.database.commit()

  def delete_many(
    self,
    table: PostgresTable | None = None,
    filter: Dict[str, Any] | None = None,
  ) -> None:
    if not table:
      raise Exception('Table instance is required.')
    if not filter:
      raise Exception('Filter expression is required.')
    query = sql.SQL("DELETE FROM {}").format(
      table.table_name
    )
    params: List[Any] = []
    if filter:
      conditions: List[sql.Composable] = []
      for column, value in filter.items():
        conditions.append(
          sql.SQL("{} = %s").format(
            sql.Identifier(column)
          )
        )
        params.append(value)
      query += sql.SQL(" WHERE ") + sql.SQL(" AND ").join(conditions)
    table.database.execute(
      query,
      params,
    )
    table.database.commit()


