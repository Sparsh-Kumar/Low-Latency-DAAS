from unittest.mock import MagicMock, patch

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


def test_mongo_get_database_throws_exception_if_database_name_is_not_passed() -> None:

  database_url = "mongodb://localhost:27017"
  mongo_database = MongoDatabase(database_url)

  mongo_table_instance_mock = MagicMock()

  mongo_database_instance_mock = MagicMock()
  mongo_database_instance_mock.get.return_value = mongo_table_instance_mock

  mongo_client_mock = MagicMock()
  mongo_client_mock.get.return_value = mongo_database_instance_mock

  with patch("database.mongo_database.MongoClient", autospec=True) as mongo_client:
    mongo_client.return_value = mongo_client_mock
    mongo_database.initialize()

  with pytest.raises(Exception, match=r"^Database name is required.$"):
    mongo_database.get_database()


def test_mongo_get_database_throws_exception_if_database_name_is_invalid() -> None:

  database_url = "mongodb://localhost:27017"
  mongo_database = MongoDatabase(database_url)

  mongo_client_mock = MagicMock()
  mongo_client_mock.get.return_value = None

  with patch("database.mongo_database.MongoClient", autospec=True) as mongo_client:
    mongo_client.return_value = mongo_client_mock
    mongo_database.initialize()

  with pytest.raises(Exception, match=r"^No database exists with database name = another_db.$"):
    mongo_database.get_database("another_db")


def test_mongo_get_database_correctly_returns_database_instance_if_exists() -> None:

  database_url = "mongodb://localhost:27017"
  mongo_database = MongoDatabase(database_url)

  mongo_client_mock = MagicMock()
  mongo_client_mock.get.return_value = {"status": "success"}

  with patch("database.mongo_database.MongoClient", autospec=True) as mongo_client:
    mongo_client.return_value = mongo_client_mock
    mongo_database.initialize()

  mongo_database_instance = mongo_database.get_database("sample_db")
  assert mongo_database_instance == {"status": "success"}


def test_mongo_get_table_throws_exception_if_database_instance_not_provided() -> None:

  database_url = "mongodb://localhost:27017"
  mongo_database = MongoDatabase(database_url)

  mongo_table_instance_mock = MagicMock()

  mongo_database_instance_mock = MagicMock()
  mongo_database_instance_mock.get.return_value = mongo_table_instance_mock

  mongo_client_mock = MagicMock()
  mongo_client_mock.get.return_value = mongo_database_instance_mock

  with patch("database.mongo_database.MongoClient", autospec=True) as mongo_client:
    mongo_client.return_value = mongo_client_mock
    mongo_database.initialize()

  with pytest.raises(Exception, match=r"^Database instance is required.$"):
    mongo_database.get_table(None, "first_table")


def test_mongo_get_table_throws_exception_if_table_name_not_provided() -> None:

  database_url = "mongodb://localhost:27017"
  mongo_database = MongoDatabase(database_url)

  mongo_database_instance_mock = MagicMock()

  mongo_client_mock = MagicMock()
  mongo_client_mock.get.return_value = mongo_database_instance_mock

  with patch("database.mongo_database.MongoClient") as mongo_client:
    mongo_client.return_value = mongo_client_mock
    mongo_database.initialize()

  mongo_database_instance = mongo_database.get_database("sample_db")
  with pytest.raises(Exception, match=r"^Table name is required.$"):
    mongo_database.get_table(mongo_database_instance)


def test_mongo_get_table_throws_exception_if_table_name_does_not_exists() -> None:

  database_url = "mongodb://localhost:27017"
  mongo_database = MongoDatabase(database_url)

  mongo_database_instance_mock = MagicMock()
  mongo_database_instance_mock.get.return_value = None

  mongo_client_mock = MagicMock()
  mongo_client_mock.get.return_value = mongo_database_instance_mock

  with patch("database.mongo_database.MongoClient") as mongo_client:
    mongo_client.return_value = mongo_client_mock
    mongo_database.initialize()

  mongo_database_instance = mongo_database.get_database("sample_db")
  with pytest.raises(Exception, match=r"^No table exists with name = second_table.$"):
    mongo_database.get_table(mongo_database_instance, "second_table")


def test_mongo_get_table_returns_table_if_both_parameters_are_provided() -> None:

  database_url = "mongodb://localhost:27017"
  mongo_database = MongoDatabase(database_url)

  mongo_table_instance_mock = MagicMock()

  mongo_database_instance_mock = MagicMock()
  mongo_database_instance_mock.get.return_value = mongo_table_instance_mock

  mongo_client_mock = MagicMock()
  mongo_client_mock.get.return_value = mongo_database_instance_mock

  with patch("database.mongo_database.MongoClient") as mongo_client:
    mongo_client.return_value = mongo_client_mock
    mongo_database.initialize()

  mongo_database_instance = mongo_database.get_database("sample_db")
  mongo_table_instance = mongo_database.get_table(mongo_database_instance, "first_table")
  assert mongo_table_instance is not None


def test_mongo_find_one_throws_exception_if_table_not_provided() -> None:

  database_url = "mongodb://localhost:27017"
  mongo_database = MongoDatabase(database_url)

  mongo_table_instance_mock = MagicMock()
  mongo_table_instance_mock.find_one.return_value = {"_id": 1}

  mongo_database_instance_mock = MagicMock()
  mongo_database_instance_mock.get.return_value = mongo_table_instance_mock

  mongo_client_mock = MagicMock()
  mongo_client_mock.get.return_value = mongo_database_instance_mock

  with patch("database.mongo_database.MongoClient") as mongo_client:
    mongo_client.return_value = mongo_client_mock
    mongo_database.initialize()

  with pytest.raises(Exception, match=r"^Table instance is required.$"):
    mongo_database.find_one()


def test_mongo_find_one_calls_function_in_table_instance() -> None:

  database_url = "mongodb://localhost:27017"
  mongo_database = MongoDatabase(database_url)

  mongo_table_instance_mock = MagicMock()
  mongo_table_instance_mock.find_one.return_value = {"_id": 1}

  mongo_database_instance_mock = MagicMock()
  mongo_database_instance_mock.get.return_value = mongo_table_instance_mock

  mongo_client_mock = MagicMock()
  mongo_client_mock.get.return_value = mongo_database_instance_mock

  with patch("database.mongo_database.MongoClient") as mongo_client:
    mongo_client.return_value = mongo_client_mock
    mongo_database.initialize()

  mongo_database_instance = mongo_database.get_database("sample_db")
  mongo_table_instance = mongo_database.get_table(mongo_database_instance, "first_table")
  found_record = mongo_database.find_one(mongo_table_instance, {})

  assert found_record == {"_id": 1}
  mongo_table_instance.find_one.assert_called_once_with({})


def test_mongo_find_one_calls_function_with_non_empty_args() -> None:

  database_url = "mongodb://localhost:27017"
  mongo_database = MongoDatabase(database_url)

  mongo_table_instance_mock = MagicMock()
  mongo_table_instance_mock.find_one.return_value = {"_id": 1}

  mongo_database_instance_mock = MagicMock()
  mongo_database_instance_mock.get.return_value = mongo_table_instance_mock

  mongo_client_mock = MagicMock()
  mongo_client_mock.get.return_value = mongo_database_instance_mock

  with patch("database.mongo_database.MongoClient") as mongo_client:
    mongo_client.return_value = mongo_client_mock
    mongo_database.initialize()

  mongo_database_instance = mongo_database.get_database("sample_db")
  mongo_table_instance = mongo_database.get_table(mongo_database_instance, "first_table")
  found_record = mongo_database.find_one(mongo_table_instance, {"_id": 1})

  assert found_record == {"_id": 1}
  mongo_table_instance.find_one.assert_called_once_with({"_id": 1})


def test_mongo_find_many_throws_exception_if_table_not_provided() -> None:

  database_url = "mongodb://localhost:27017"
  mongo_database = MongoDatabase(database_url)

  mongo_table_instance_mock = MagicMock()

  mongo_database_instance_mock = MagicMock()
  mongo_database_instance_mock.get.return_value = mongo_table_instance_mock

  mongo_client_mock = MagicMock()
  mongo_client_mock.get.return_value = mongo_database_instance_mock

  with patch("database.mongo_database.MongoClient") as mongo_client:
    mongo_client.return_value = mongo_client_mock
    mongo_database.initialize()

  with pytest.raises(Exception, match=r"^Table instance is required.$"):
    mongo_database.find_many()


def test_mongo_find_many_calls_function_in_table_instance() -> None:

  database_url = "mongodb://localhost:27017"
  mongo_database = MongoDatabase(database_url)

  mongo_table_instance_mock = MagicMock()
  mongo_table_instance_mock.find.return_value = [{"_id": 1}]

  mongo_database_instance_mock = MagicMock()
  mongo_database_instance_mock.get.return_value = mongo_table_instance_mock

  mongo_client_mock = MagicMock()
  mongo_client_mock.get.return_value = mongo_database_instance_mock

  with patch("database.mongo_database.MongoClient") as mongo_client:
    mongo_client.return_value = mongo_client_mock
    mongo_database.initialize()

  mongo_database_instance = mongo_database.get_database("sample_db")
  mongo_table_instance = mongo_database.get_table(mongo_database_instance, "first_table")
  found_records = mongo_database.find_many(mongo_table_instance, {})

  assert found_records == [{"_id": 1}]
  mongo_table_instance.find.assert_called_once_with({})


def test_mongo_find_many_calls_function_with_non_empty_args() -> None:

  database_url = "mongodb://localhost:27017"
  mongo_database = MongoDatabase(database_url)

  mongo_table_instance_mock = MagicMock()
  mongo_table_instance_mock.find.return_value = [{"_id": 1}]

  mongo_database_instance_mock = MagicMock()
  mongo_database_instance_mock.get.return_value = mongo_table_instance_mock

  mongo_client_mock = MagicMock()
  mongo_client_mock.get.return_value = mongo_database_instance_mock

  with patch("database.mongo_database.MongoClient") as mongo_client:
    mongo_client.return_value = mongo_client_mock
    mongo_database.initialize()

  mongo_database_instance = mongo_database.get_database("sample_db")
  mongo_table_instance = mongo_database.get_table(mongo_database_instance, "first_table")
  found_records = mongo_database.find_many(mongo_table_instance, {"_id": 1})

  assert found_records == [{"_id": 1}]
  mongo_table_instance.find.assert_called_once_with({"_id": 1})


def test_mongo_insert_one_throws_exception_if_table_not_provided() -> None:

  database_url = "mongodb://localhost:27017"
  mongo_database = MongoDatabase(database_url)

  mongo_table_instance_mock = MagicMock()
  mongo_table_instance_mock.insert_one.return_value = {"status": "success"}

  mongo_database_instance_mock = MagicMock()
  mongo_database_instance_mock.get.return_value = mongo_table_instance_mock

  mongo_client_mock = MagicMock()
  mongo_client_mock.get.return_value = mongo_database_instance_mock

  with patch("database.mongo_database.MongoClient") as mongo_client:
    mongo_client.return_value = mongo_client_mock
    mongo_database.initialize()

  with pytest.raises(Exception, match=r"^Table instance is required.$"):
    mongo_database.insert_one()


def test_mongo_insert_one_throws_exception_if_record_not_provided() -> None:

  database_url = "mongodb://localhost:27017"
  mongo_database = MongoDatabase(database_url)

  mongo_table_instance_mock = MagicMock()
  mongo_table_instance_mock.insert_one.return_value = {"status": "success"}

  mongo_database_instance_mock = MagicMock()
  mongo_database_instance_mock.get.return_value = mongo_table_instance_mock

  mongo_client_mock = MagicMock()
  mongo_client_mock.return_value = mongo_database_instance_mock

  with patch("database.mongo_database.MongoClient") as mongo_client:
    mongo_client.return_value = mongo_client_mock
    mongo_database.initialize()

  mongo_database_instance = mongo_database.get_database("sample_db")
  mongo_table_instance = mongo_database.get_table(mongo_database_instance, "first_table")

  with pytest.raises(Exception, match=r"^Record to insert is required.$"):
    mongo_database.insert_one(mongo_table_instance)


def test_mongo_insert_one_calls_function_in_table_instance() -> None:

  database_url = "mongodb://localhost:27017"
  mongo_database = MongoDatabase(database_url)

  mongo_table_instance_mock = MagicMock()
  mongo_table_instance_mock.insert_one.return_value = {"status": "success"}

  mongo_database_instance_mock = MagicMock()
  mongo_database_instance_mock.get.return_value = mongo_table_instance_mock

  mongo_client_mock = MagicMock()
  mongo_client_mock.get.return_value = mongo_database_instance_mock

  with patch("database.mongo_database.MongoClient") as mongo_client:
    mongo_client.return_value = mongo_client_mock
    mongo_database.initialize()

  mongo_database_instance = mongo_database.get_database("sample_db")
  mongo_table_instance = mongo_database.get_table(mongo_database_instance, "first_table")

  insert_response = mongo_database.insert_one(mongo_table_instance, {"_id": 1})

  assert insert_response == {"status": "success"}
  mongo_table_instance.insert_one.assert_called_once_with({"_id": 1})


def test_mongo_insert_many_throws_exception_if_table_not_provided() -> None:

  database_url = "mongodb://localhost:27017"
  mongo_database = MongoDatabase(database_url)

  mongo_table_instance_mock = MagicMock()
  mongo_table_instance_mock.insert_many.return_value = [{"status": "success"}]

  mongo_database_instance_mock = MagicMock()
  mongo_database_instance_mock.get.return_value = mongo_table_instance_mock

  mongo_client_mock = MagicMock()
  mongo_client_mock.get.return_value = mongo_database_instance_mock

  with patch("database.mongo_database.MongoClient") as mongo_client:
    mongo_client.return_value = mongo_client_mock
    mongo_database.initialize()

  with pytest.raises(Exception, match=r"^Table instance is required.$"):
    mongo_database.insert_many()


def test_mongo_insert_many_throws_exception_if_records_not_provided() -> None:

  database_url = "mongodb://localhost:27017"
  mongo_database = MongoDatabase(database_url)

  mongo_table_instance_mock = MagicMock()
  mongo_table_instance_mock.insert_many.return_value = [{"status": "success"}]

  mongo_database_instance_mock = MagicMock()
  mongo_database_instance_mock.get.return_value = mongo_table_instance_mock

  mongo_client_mock = MagicMock()
  mongo_client_mock.get.return_value = mongo_database_instance_mock

  with patch("database.mongo_database.MongoClient") as mongo_client:
    mongo_client.return_value = mongo_client_mock
    mongo_database.initialize()

  mongo_database_instance = mongo_database.get_database("sample_db")
  mongo_table_instance = mongo_database.get_table(mongo_database_instance, "first_table")

  with pytest.raises(Exception, match=r"^Records to insert are required.$"):
    mongo_database.insert_many(mongo_table_instance)


def test_mongo_insert_many_calls_function_in_table_instance() -> None:

  database_url = "mongodb://localhost:27017"
  mongo_database = MongoDatabase(database_url)

  mongo_table_instance_mock = MagicMock()
  mongo_table_instance_mock.insert_many.return_value = [{"status": "success"}]

  mongo_database_instance_mock = MagicMock()
  mongo_database_instance_mock.get.return_value = mongo_table_instance_mock

  mongo_client_mock = MagicMock()
  mongo_client_mock.get.return_value = mongo_database_instance_mock

  with patch("database.mongo_database.MongoClient") as mongo_client:
    mongo_client.return_value = mongo_client_mock
    mongo_database.initialize()

  mongo_database_instance = mongo_database.get_database("sample_db")
  mongo_table_instance = mongo_database.get_table(mongo_database_instance, "first_table")

  insert_response = mongo_database.insert_many(mongo_table_instance, [{"_id": 1}, {"_id": 2}])

  assert insert_response == [{"status": "success"}]
  mongo_table_instance.insert_many.assert_called_once_with([{"_id": 1}, {"_id": 2}])


def test_mongo_delete_one_throws_exception_if_table_not_provided() -> None:

  database_url = "mongodb://localhost:27017"
  mongo_database = MongoDatabase(database_url)

  mongo_table_instance_mock = MagicMock()
  mongo_table_instance_mock.delete_one.return_value = {"status": "success"}

  mongo_database_instance_mock = MagicMock()
  mongo_database_instance_mock.get.return_value = mongo_table_instance_mock

  mongo_client_mock = MagicMock()
  mongo_client_mock.get.return_value = mongo_database_instance_mock

  with patch("database.mongo_database.MongoClient") as mongo_client:
    mongo_client.return_value = mongo_client_mock
    mongo_database.initialize()

  with pytest.raises(Exception, match=r"^Table instance is required.$"):
    mongo_database.delete_one()


def test_mongo_delete_one_throws_exception_if_record_id_not_provided() -> None:

  database_url = "mongodb://localhost:27017"
  mongo_database = MongoDatabase(database_url)

  mongo_table_instance_mock = MagicMock()
  mongo_table_instance_mock.delete_one.return_value = {"status": "success"}

  mongo_database_instance_mock = MagicMock()
  mongo_database_instance_mock.get.return_value = mongo_table_instance_mock

  mongo_client_mock = MagicMock()
  mongo_client_mock.get.return_value = mongo_database_instance_mock

  with patch("database.mongo_database.MongoClient") as mongo_client:
    mongo_client.return_value = mongo_client_mock
    mongo_database.initialize()

  mongo_database_instance = mongo_database.get_database("sample_db")
  mongo_table_instance = mongo_database.get_table(mongo_database_instance, "first_table")

  with pytest.raises(Exception, match=r"^Record id is required for deletion.$"):
    mongo_database.delete_one(mongo_table_instance)


def test_mongo_delete_one_calls_function_in_table_instance() -> None:

  database_url = "mongodb://localhost:27017"
  mongo_database = MongoDatabase(database_url)

  mongo_table_instance_mock = MagicMock()
  mongo_table_instance_mock.delete_one.return_value = {"status": "success"}

  mongo_database_instance_mock = MagicMock()
  mongo_database_instance_mock.get.return_value = mongo_table_instance_mock

  mongo_client_mock = MagicMock()
  mongo_client_mock.get.return_value = mongo_database_instance_mock

  with patch("database.mongo_database.MongoClient") as mongo_client:
    mongo_client.return_value = mongo_client_mock
    mongo_database.initialize()

  mongo_database_instance = mongo_database.get_database("sample_db")
  mongo_table_instance = mongo_database.get_table(mongo_database_instance, "first_table")

  delete_record_response = mongo_database.delete_one(mongo_table_instance, 123)

  assert delete_record_response == {"status": "success"}
  mongo_table_instance.delete_one.assert_called_once_with({"_id": 123})
