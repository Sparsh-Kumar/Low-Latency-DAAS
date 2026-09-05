import os
from collections.abc import Generator
from dataclasses import dataclass
from typing import Any

import pytest  # type: ignore
from dotenv import load_dotenv  # type: ignore
from pymongo import MongoClient  # type: ignore
from pymongo.collection import Collection  # type: ignore
from pymongo.database import Database  # type: ignore

load_dotenv()


@dataclass
class MongoResource:
  client: MongoClient[dict[str, Any]]
  database: Database[dict[str, Any]]
  collection: Collection[dict[str, Any]]


@pytest.fixture
def mongodb_connection_uri() -> str:
  mongodb_connection_uri = os.getenv("TEST_MONGODB_URI")
  print(f"MongoDB Connection URI = {mongodb_connection_uri}")
  if not mongodb_connection_uri:
    raise RuntimeError(
      "TEST_MONGODB_URI not found. Please set it before running integration tests."
    )
  return mongodb_connection_uri


@pytest.fixture
def mongo_resource(mongodb_connection_uri: str) -> Generator[MongoResource, None, None]:

  client = MongoClient(mongodb_connection_uri)

  database = client["test_database"]
  collection = database["test_collection"]

  resource = MongoResource(
    client=client,
    database=database,
    collection=collection,
  )

  try:
    yield resource
  finally:
    client.close()
