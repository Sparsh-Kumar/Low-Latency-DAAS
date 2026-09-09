import csv
import os
from collections.abc import Generator

import pytest  # type: ignore
from dotenv import load_dotenv  # type: ignore
from psycopg import connect, sql  # type: ignore
from psycopg.conninfo import make_conninfo  # type: ignore
from psycopg.rows import dict_row  # type: ignore
from pymongo import MongoClient  # type: ignore

from database.types import PostgresTable
from tests.typings import MongoResource, PostgresResource

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


@pytest.fixture
def postgres_resource(
  postgres_test_connection_uri: str,
  postgres_test_database_name: str,
  postgres_test_table_name: str,
) -> Generator[PostgresResource, None, None]:

  maintenance_database_url = make_conninfo(
    postgres_test_connection_uri,
    dbname="postgres",
  )
  client = connect(maintenance_database_url, autocommit=True)
  database_exists = client.execute(
    "SELECT 1 FROM pg_database WHERE datname = %s",
    [postgres_test_database_name],
  ).fetchone()
  if database_exists is None:
    client.execute(
      sql.SQL("CREATE DATABASE {}").format(sql.Identifier(postgres_test_database_name))
    )

  database_url = make_conninfo(
    postgres_test_connection_uri,
    dbname=postgres_test_database_name,
  )
  database = connect(database_url, row_factory=dict_row)
  table = PostgresTable(
    database=database,
    table_name=sql.Identifier(postgres_test_table_name),
  )

  resource = PostgresResource(
    client=client,
    database=database,
    table=table,
  )

  try:
    yield resource
  finally:
    database.close()
    client.close()


@pytest.fixture
def postgres_resource_with_inserted_fixtures(
  postgres_test_connection_uri: str,
  postgres_test_database_name: str,
  postgres_test_table_name: str,
) -> Generator[PostgresResource, None, None]:

  maintenance_database_url = make_conninfo(
    postgres_test_connection_uri,
    dbname="postgres",
  )
  client = connect(maintenance_database_url, autocommit=True)
  database_exists = client.execute(
    "SELECT 1 FROM pg_database WHERE datname = %s",
    [postgres_test_database_name],
  ).fetchone()
  if database_exists is None:
    client.execute(
      sql.SQL("CREATE DATABASE {}").format(sql.Identifier(postgres_test_database_name))
    )

  database_url = make_conninfo(
    postgres_test_connection_uri,
    dbname=postgres_test_database_name,
  )
  database = connect(database_url, row_factory=dict_row)
  table = PostgresTable(
    database=database,
    table_name=sql.Identifier(postgres_test_table_name),
  )

  records_to_insert = []
  postgres_fixtures_file_csv = os.path.join(
    os.getcwd(), "libs", "lib-database", "tests", "fixtures", "postgres_records.csv"
  )

  with open(postgres_fixtures_file_csv, newline="", encoding="utf-8") as file:
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

  database.execute(
    sql.SQL(
      """
      CREATE TABLE IF NOT EXISTS {} (
        id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        name TEXT,
        age INTEGER,
        email TEXT
      )
      """
    ).format(table.table_name)
  )
  database.execute(sql.SQL("DELETE FROM {}").format(table.table_name))

  column_names = list(records_to_insert[0].keys())
  columns = [sql.Identifier(column_name) for column_name in column_names]
  placeholders = [sql.Placeholder() for _ in column_names]
  insert_query = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
    table.table_name,
    sql.SQL(", ").join(columns),
    sql.SQL(", ").join(placeholders),
  )
  values = [[record[column_name] for column_name in column_names] for record in records_to_insert]
  with database.cursor() as cursor:
    cursor.executemany(insert_query, values)
  database.commit()

  resource = PostgresResource(
    client=client,
    database=database,
    table=table,
  )

  try:
    yield resource
  finally:
    database.close()
    client.close()
