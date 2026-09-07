from dataclasses import dataclass
from typing import Any

from pymongo import MongoClient  # type: ignore
from pymongo.collection import Collection  # type: ignore
from pymongo.database import Database  # type: ignore


@dataclass
class MongoResource:
  client: MongoClient[dict[str, Any]]
  database: Database[dict[str, Any]]
  collection: Collection[dict[str, Any]]
