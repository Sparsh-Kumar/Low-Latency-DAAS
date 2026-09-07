import os

import pytest  # type: ignore


@pytest.fixture
def mongodb_test_connection_uri() -> str:
  mongodb_test_connection_uri = os.getenv("TEST_MONGODB_URI")
  if not mongodb_test_connection_uri:
    raise RuntimeError(
      "TEST_MONGODB_URI not found. Please set it before running integration tests."
    )
  return mongodb_test_connection_uri


@pytest.fixture
def mongodb_test_database_name() -> str:
  mongodb_test_database_name = os.getenv("TEST_MONGODB_DATABASE_NAME")
  if not mongodb_test_database_name:
    raise RuntimeError(
      "TEST_MONGODB_DATABASE_NAME not found. Please set it before running integration tests."
    )
  return mongodb_test_database_name


@pytest.fixture
def mongodb_test_collection_name() -> str:
  mongodb_test_collection_name = os.getenv("TEST_MONGODB_COLLECTION_NAME")
  if not mongodb_test_collection_name:
    raise RuntimeError(
      "TEST_MONGODB_COLLECTION_NAME not found. Please set it before running integration tests."
    )
  return mongodb_test_collection_name


@pytest.fixture
def postgres_test_connection_uri() -> str:
  postgres_test_connection_uri = os.getenv("TEST_POSTGRES_URI")
  if not postgres_test_connection_uri:
    raise RuntimeError(
      "TEST_POSTGRES_URI not found. Please set it before running integration tests."
    )
  return postgres_test_connection_uri


@pytest.fixture
def postgres_test_database_name() -> str:
  postgres_test_database_name = os.getenv("TEST_POSTGRES_DATABASE_NAME")
  if not postgres_test_database_name:
    raise RuntimeError(
      "TEST_POSTGRES_DATABASE_NAME not found. Please set it before running integration tests."
    )
  return postgres_test_database_name


@pytest.fixture
def postgres_test_table_name() -> str:
  postgres_test_table_name = os.getenv("TEST_POSTGRES_TABLE_NAME")
  if not postgres_test_table_name:
    raise RuntimeError(
      "TEST_POSTGRES_TABLE_NAME not found. Please set it before running integration tests."
    )
  return postgres_test_table_name
