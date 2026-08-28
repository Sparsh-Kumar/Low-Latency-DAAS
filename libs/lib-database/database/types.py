from dataclasses import dataclass
from typing import Any

from psycopg import Connection, sql  # type: ignore


@dataclass
class PostgresTable:
  database: Connection[Any]
  table_name: sql.Identifier
