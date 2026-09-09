from dataclasses import dataclass
from typing import Any

from psycopg import Connection, sql

PostgresRecord = dict[str, Any]


@dataclass
class PostgresTable:
  database: Connection[PostgresRecord]
  table_name: sql.Identifier
