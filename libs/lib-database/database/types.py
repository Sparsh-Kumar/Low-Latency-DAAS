from dataclasses import dataclass
from psycopg import Connection, sql # type: ignore
from typing import Any

@dataclass
class PostgresTable:
  database: Connection[Any]
  table_name: sql.Identifier

