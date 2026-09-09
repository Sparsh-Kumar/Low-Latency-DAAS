from dataclasses import dataclass
from typing import Any

from psycopg import Connection  # type: ignore
from pymongo import MongoClient  # type: ignore
from pymongo.collection import Collection  # type: ignore
from pymongo.database import Database  # type: ignore

from database.types import PostgresRecord, PostgresTable


@dataclass
class MongoResource:
  client: MongoClient[dict[str, Any]]
  database: Database[dict[str, Any]]
  collection: Collection[dict[str, Any]]


@dataclass
class PostgresResource:
  client: Connection[Any]
  database: Connection[PostgresRecord]
  table: PostgresTable
