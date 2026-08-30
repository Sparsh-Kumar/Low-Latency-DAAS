from unittest.mock import patch

import pytest  # type: ignore

from database.mongo_database import MongoDatabase


def test_mongo_initialize_correctly_create_connection() -> None:
  database_url = "mongodb://localhost:27017"
  mongo_database = MongoDatabase(database_url)

  with patch("database.mongo_database.MongoClient", autospec=True) as mongo_client:
    mongo_database.initialize()

  mongo_client.assert_called_once_with(database_url)
  assert mongo_database._database_client is mongo_client.return_value


def test_mongno_initialize_does_not_create_connection_if_already_exists() -> None:
  database_url = "mongodb://localhost:27017"
  mongo_database = MongoDatabase(database_url)

  with patch("database.mongo_database.MongoClient", autospec=True) as mongo_client:
    mongo_database.initialize()
    mongo_database.initialize()

  mongo_client.assert_called_once_with(database_url)
  assert mongo_database._database_client is mongo_client.return_value


def test_mongo_get_database_correctly_returns_database_instance_if_exists() -> None:
  database_url = "mongodb://localhost:27017"
  mongo_database = MongoDatabase(database_url)
  mongo_client_return_value = {
    "sample_db": {
      "id": 1,
    }
  }

  with patch("database.mongo_database.MongoClient", autospec=True) as mongo_client:
    mongo_client.return_value = mongo_client_return_value
    mongo_database.initialize()

  mongo_database_instance = mongo_database.get_database("sample_db")
  assert mongo_database_instance == mongo_client_return_value["sample_db"]


def test_mongo_get_database_throws_exception_if_database_name_is_not_passed() -> None:
  database_url = "mongodb://localhost:27017"
  mongo_database = MongoDatabase(database_url)
  mongo_client_return_value = {
    "sample_db": {
      "id": 1,
    }
  }

  with patch("database.mongo_database.MongoClient", autospec=True) as mongo_client:
    mongo_client.return_value = mongo_client_return_value
    mongo_database.initialize()

  with pytest.raises(Exception, match="Database name is required."):
    mongo_database.get_database()


def test_mongo_get_database_throws_exception_if_database_name_is_invalid() -> None:
  database_url = "mongodb://localhost:27017"
  mongo_database = MongoDatabase(database_url)
  invalid_database_name = "another_db"
  mongo_client_return_value = {
    "sample_db": {
      "id": 1,
    }
  }

  with patch("database.mongo_database.MongoClient", autospec=True) as mongo_client:
    mongo_client.return_value = mongo_client_return_value
    mongo_database.initialize()

  with pytest.raises(
    Exception, match=f"No database exists with database name = {invalid_database_name}."
  ):
    mongo_database.get_database("another_db")


def test_mongo_get_table() -> None:
  pass


def test_mongo_find_one() -> None:
  pass


def test_mongo_find_many() -> None:
  pass


def test_mongo_insert_one() -> None:
  pass


def test_mongo_insert_many() -> None:
  pass


def test_mongo_delete_one() -> None:
  pass


def test_mongo_delete_many() -> None:
  pass
