import csv
import os
from collections.abc import Generator

import pytest  # type: ignore
from dotenv import load_dotenv  # type: ignore
from pymongo import MongoClient  # type: ignore

from tests.typings import MongoResource

load_dotenv()

TYPE_CASTERS = {
  "int": int,
  "float": float,
  "bool": lambda v: v.lower() in ("true", "1", "yes"),
  "str": str,
}


@pytest.fixture
def mongo_resource(
  mongodb_test_connection_uri: str,
  mongodb_test_database_name: str,
  mongodb_test_collection_name: str,
) -> Generator[MongoResource, None, None]:

  client = MongoClient(mongodb_test_connection_uri)
  database = client[mongodb_test_database_name]
  collection = database[mongodb_test_collection_name]

  resource = MongoResource(
    client=client,
    database=database,
    collection=collection,
  )

  try:
    yield resource
  finally:
    client.close()


@pytest.fixture
def mongo_resource_with_inserted_fixtures(
  mongodb_test_connection_uri: str,
  mongodb_test_database_name: str,
  mongodb_test_collection_name: str,
) -> Generator[MongoResource, None, None]:

  client = MongoClient(mongodb_test_connection_uri)
  database = client[mongodb_test_database_name]
  collection = database[mongodb_test_collection_name]

  records_to_insert = []
  mongo_fixtures_file_csv = os.path.join(
    os.getcwd(), "libs", "lib-database", "tests", "fixtures", "mongo_records.csv"
  )

  with open(mongo_fixtures_file_csv, newline="", encoding="utf-8") as file:
    csv_reader = csv.reader(file)
    csv_headers = next(csv_reader)
    headers_with_types = []

    for header in csv_headers:
      if ":" in header:
        field_name, field_type = header.split(":", 1)
      else:
        field_name, field_type = header, "str"
      headers_with_types.append((field_name, field_type))

    for row in csv_reader:
      record_to_insert = {}
      for (field_name, field_type), value in zip(headers_with_types, row, strict=True):
        type_cast = TYPE_CASTERS.get(field_type, str)
        record_to_insert[field_name] = type_cast(value) if value != "" else None
      records_to_insert.append(record_to_insert)

  collection.delete_many({})
  collection.insert_many(records_to_insert)

  resource = MongoResource(
    client=client,
    database=database,
    collection=collection,
  )

  try:
    yield resource
  finally:
    client.close()
