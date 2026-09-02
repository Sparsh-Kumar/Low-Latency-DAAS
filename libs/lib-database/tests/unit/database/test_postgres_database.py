from unittest.mock import MagicMock, patch

import pytest  # type: ignore

from database.postgres_database import PostgresDatabase


def test_postgres_initialize_correctly_create_connection() -> None:
  database_url = "postgresql://localhost:5432/sample_db"
  postgres_database = PostgresDatabase(database_url)

  with patch("database.postgres_database.psycopg.connect", autospec=True) as postgres_connect:
    postgres_database.initialize()

  postgres_connect.assert_called_once_with(database_url)
  assert postgres_database._database_client is postgres_connect.return_value


def test_postgres_initialize_does_not_create_connection_if_already_exists() -> None:
  database_url = "postgresql://localhost:5432/sample_db"
  postgres_database = PostgresDatabase(database_url)

  with patch("database.postgres_database.psycopg.connect", autospec=True) as postgres_connect:
    postgres_database.initialize()
    postgres_database.initialize()

  postgres_connect.assert_called_once_with(database_url)
  assert postgres_database._database_client is postgres_connect.return_value


def test_postgres_get_database_throws_exception_if_database_name_is_not_passed() -> None:
  database_url = "postgresql://localhost:5432/sample_db"
  postgres_database = PostgresDatabase(database_url)

  postgres_connection_mock = MagicMock()

  with patch("database.postgres_database.psycopg.connect", autospec=True) as postgres_connect:
    postgres_connect.return_value = postgres_connection_mock
    postgres_database.initialize()

  with pytest.raises(Exception, match=r"^Database name is required.$"):
    postgres_database.get_database()


def test_postgres_get_database_correctly_returns_database_instance_if_exists() -> None:
  database_url = "postgresql://localhost:5432/sample_db"
  postgres_database = PostgresDatabase(database_url)

  postgres_connection_mock = MagicMock()

  with patch("database.postgres_database.psycopg.connect", autospec=True) as postgres_connect:
    postgres_connect.return_value = postgres_connection_mock
    postgres_database.initialize()

  postgres_database_instance = postgres_database.get_database("sample_db")
  assert postgres_database_instance is postgres_connection_mock


def test_postgres_get_table_throws_exception_if_database_instance_not_provided() -> None:
  database_url = "postgresql://localhost:5432/sample_db"
  postgres_database = PostgresDatabase(database_url)

  postgres_connection_mock = MagicMock()

  with patch("database.postgres_database.psycopg.connect", autospec=True) as postgres_connect:
    postgres_connect.return_value = postgres_connection_mock
    postgres_database.initialize()

  with pytest.raises(Exception, match=r"^Database instance is required.$"):
    postgres_database.get_table(None, "first_table")


def test_postgres_get_table_throws_exception_if_table_name_not_provided() -> None:
  database_url = "postgresql://localhost:5432/sample_db"
  postgres_database = PostgresDatabase(database_url)

  postgres_connection_mock = MagicMock()

  with patch("database.postgres_database.psycopg.connect", autospec=True) as postgres_connect:
    postgres_connect.return_value = postgres_connection_mock
    postgres_database.initialize()

  postgres_database_instance = postgres_database.get_database("sample_db")
  with pytest.raises(Exception, match=r"^Table name is required.$"):
    postgres_database.get_table(postgres_database_instance)


def test_postgres_get_table_returns_table_if_both_parameters_are_provided() -> None:
  database_url = "postgresql://localhost:5432/sample_db"
  postgres_database = PostgresDatabase(database_url)

  postgres_connection_mock = MagicMock()

  with patch("database.postgres_database.psycopg.connect", autospec=True) as postgres_connect:
    postgres_connect.return_value = postgres_connection_mock
    postgres_database.initialize()

  postgres_database_instance = postgres_database.get_database("sample_db")
  postgres_table_instance = postgres_database.get_table(postgres_database_instance, "first_table")
  assert postgres_table_instance is not None


def test_postgres_find_one_throws_exception_if_table_not_provided() -> None:
  database_url = "postgresql://localhost:5432/sample_db"
  postgres_database = PostgresDatabase(database_url)

  postgres_connection_mock = MagicMock()

  with patch("database.postgres_database.psycopg.connect", autospec=True) as postgres_connect:
    postgres_connect.return_value = postgres_connection_mock
    postgres_database.initialize()

  with pytest.raises(Exception, match=r"^Table instance is required.$"):
    postgres_database.find_one()


def test_postgres_find_one_calls_function_in_table_instance() -> None:
  database_url = "postgresql://localhost:5432/sample_db"
  postgres_database = PostgresDatabase(database_url)

  postgres_cursor_mock = MagicMock()
  postgres_cursor_mock.fetchone.return_value = {"id": 1}

  postgres_connection_mock = MagicMock()
  postgres_connection_mock.execute.return_value = postgres_cursor_mock

  with patch("database.postgres_database.psycopg.connect", autospec=True) as postgres_connect:
    postgres_connect.return_value = postgres_connection_mock
    postgres_database.initialize()

  postgres_database_instance = postgres_database.get_database("sample_db")
  postgres_table_instance = postgres_database.get_table(postgres_database_instance, "first_table")
  found_record = postgres_database.find_one(postgres_table_instance, {})

  assert found_record == {"id": 1}
  postgres_connection_mock.execute.assert_called_once()
  postgres_cursor_mock.fetchone.assert_called_once()


def test_postgres_find_one_calls_function_with_non_empty_args() -> None:
  database_url = "postgresql://localhost:5432/sample_db"
  postgres_database = PostgresDatabase(database_url)

  postgres_cursor_mock = MagicMock()
  postgres_cursor_mock.fetchone.return_value = {"id": 1}

  postgres_connection_mock = MagicMock()
  postgres_connection_mock.execute.return_value = postgres_cursor_mock

  with patch("database.postgres_database.psycopg.connect", autospec=True) as postgres_connect:
    postgres_connect.return_value = postgres_connection_mock
    postgres_database.initialize()

  postgres_database_instance = postgres_database.get_database("sample_db")
  postgres_table_instance = postgres_database.get_table(postgres_database_instance, "first_table")
  found_record = postgres_database.find_one(postgres_table_instance, {"id": 1})

  assert found_record == {"id": 1}
  postgres_connection_mock.execute.assert_called_once()
  assert postgres_connection_mock.execute.call_args.args[1] == [1]
  postgres_cursor_mock.fetchone.assert_called_once()


def test_postgres_find_many_throws_exception_if_table_not_provided() -> None:
  database_url = "postgresql://localhost:5432/sample_db"
  postgres_database = PostgresDatabase(database_url)

  postgres_connection_mock = MagicMock()

  with patch("database.postgres_database.psycopg.connect", autospec=True) as postgres_connect:
    postgres_connect.return_value = postgres_connection_mock
    postgres_database.initialize()

  with pytest.raises(Exception, match=r"^Table instance is required.$"):
    postgres_database.find_many()


def test_postgres_find_many_calls_function_in_table_instance() -> None:
  database_url = "postgresql://localhost:5432/sample_db"
  postgres_database = PostgresDatabase(database_url)

  postgres_cursor_mock = MagicMock()
  postgres_cursor_mock.fetchall.return_value = [{"id": 1}]

  postgres_connection_mock = MagicMock()
  postgres_connection_mock.execute.return_value = postgres_cursor_mock

  with patch("database.postgres_database.psycopg.connect", autospec=True) as postgres_connect:
    postgres_connect.return_value = postgres_connection_mock
    postgres_database.initialize()

  postgres_database_instance = postgres_database.get_database("sample_db")
  postgres_table_instance = postgres_database.get_table(postgres_database_instance, "first_table")
  found_records = postgres_database.find_many(postgres_table_instance, {})

  assert found_records == [{"id": 1}]
  postgres_connection_mock.execute.assert_called_once()
  postgres_cursor_mock.fetchall.assert_called_once()


def test_postgres_find_many_calls_function_with_non_empty_args() -> None:
  database_url = "postgresql://localhost:5432/sample_db"
  postgres_database = PostgresDatabase(database_url)

  postgres_cursor_mock = MagicMock()
  postgres_cursor_mock.fetchall.return_value = [{"id": 1}]

  postgres_connection_mock = MagicMock()
  postgres_connection_mock.execute.return_value = postgres_cursor_mock

  with patch("database.postgres_database.psycopg.connect", autospec=True) as postgres_connect:
    postgres_connect.return_value = postgres_connection_mock
    postgres_database.initialize()

  postgres_database_instance = postgres_database.get_database("sample_db")
  postgres_table_instance = postgres_database.get_table(postgres_database_instance, "first_table")
  found_records = postgres_database.find_many(postgres_table_instance, {"id": 1})

  assert found_records == [{"id": 1}]
  postgres_connection_mock.execute.assert_called_once()
  assert postgres_connection_mock.execute.call_args.args[1] == [1]
  postgres_cursor_mock.fetchall.assert_called_once()


def test_postgres_insert_one_throws_exception_if_table_not_provided() -> None:
  database_url = "postgresql://localhost:5432/sample_db"
  postgres_database = PostgresDatabase(database_url)

  postgres_connection_mock = MagicMock()

  with patch("database.postgres_database.psycopg.connect", autospec=True) as postgres_connect:
    postgres_connect.return_value = postgres_connection_mock
    postgres_database.initialize()

  with pytest.raises(Exception, match=r"^Table instance is required.$"):
    postgres_database.insert_one()


def test_postgres_insert_one_throws_exception_if_record_not_provided() -> None:
  database_url = "postgresql://localhost:5432/sample_db"
  postgres_database = PostgresDatabase(database_url)

  postgres_connection_mock = MagicMock()

  with patch("database.postgres_database.psycopg.connect", autospec=True) as postgres_connect:
    postgres_connect.return_value = postgres_connection_mock
    postgres_database.initialize()

  postgres_database_instance = postgres_database.get_database("sample_db")
  postgres_table_instance = postgres_database.get_table(postgres_database_instance, "first_table")

  with pytest.raises(Exception, match=r"^Record to insert is required.$"):
    postgres_database.insert_one(postgres_table_instance)


def test_postgres_insert_one_calls_function_in_table_instance() -> None:
  database_url = "postgresql://localhost:5432/sample_db"
  postgres_database = PostgresDatabase(database_url)

  postgres_connection_mock = MagicMock()

  with patch("database.postgres_database.psycopg.connect", autospec=True) as postgres_connect:
    postgres_connect.return_value = postgres_connection_mock
    postgres_database.initialize()

  postgres_database_instance = postgres_database.get_database("sample_db")
  postgres_table_instance = postgres_database.get_table(postgres_database_instance, "first_table")

  postgres_database.insert_one(postgres_table_instance, {"id": 1})

  postgres_connection_mock.execute.assert_called_once()
  assert postgres_connection_mock.execute.call_args.args[1] == [1]
  postgres_connection_mock.commit.assert_called_once()


def test_postgres_insert_many_throws_exception_if_table_not_provided() -> None:
  database_url = "postgresql://localhost:5432/sample_db"
  postgres_database = PostgresDatabase(database_url)

  postgres_connection_mock = MagicMock()

  with patch("database.postgres_database.psycopg.connect", autospec=True) as postgres_connect:
    postgres_connect.return_value = postgres_connection_mock
    postgres_database.initialize()

  with pytest.raises(Exception, match=r"^Table instance is required.$"):
    postgres_database.insert_many()


def test_postgres_insert_many_throws_exception_if_records_not_provided() -> None:
  database_url = "postgresql://localhost:5432/sample_db"
  postgres_database = PostgresDatabase(database_url)

  postgres_connection_mock = MagicMock()

  with patch("database.postgres_database.psycopg.connect", autospec=True) as postgres_connect:
    postgres_connect.return_value = postgres_connection_mock
    postgres_database.initialize()

  postgres_database_instance = postgres_database.get_database("sample_db")
  postgres_table_instance = postgres_database.get_table(postgres_database_instance, "first_table")

  with pytest.raises(Exception, match=r"^Record to insert is required.$"):
    postgres_database.insert_many(postgres_table_instance)


def test_postgres_insert_many_calls_function_in_table_instance() -> None:
  database_url = "postgresql://localhost:5432/sample_db"
  postgres_database = PostgresDatabase(database_url)

  postgres_cursor_mock = MagicMock()
  postgres_connection_mock = MagicMock()
  postgres_connection_mock.cursor.return_value.__enter__.return_value = postgres_cursor_mock

  with patch("database.postgres_database.psycopg.connect", autospec=True) as postgres_connect:
    postgres_connect.return_value = postgres_connection_mock
    postgres_database.initialize()

  postgres_database_instance = postgres_database.get_database("sample_db")
  postgres_table_instance = postgres_database.get_table(postgres_database_instance, "first_table")

  postgres_database.insert_many(postgres_table_instance, [{"id": 1}, {"id": 2}])

  postgres_cursor_mock.executemany.assert_called_once()
  assert postgres_cursor_mock.executemany.call_args.args[1] == [[1], [2]]
  postgres_connection_mock.commit.assert_called_once()


def test_postgres_delete_one_throws_exception_if_table_not_provided() -> None:
  database_url = "postgresql://localhost:5432/sample_db"
  postgres_database = PostgresDatabase(database_url)

  postgres_connection_mock = MagicMock()

  with patch("database.postgres_database.psycopg.connect", autospec=True) as postgres_connect:
    postgres_connect.return_value = postgres_connection_mock
    postgres_database.initialize()

  with pytest.raises(Exception, match=r"^Table instance is required.$"):
    postgres_database.delete_one()


def test_postgres_delete_one_throws_exception_if_record_id_not_provided() -> None:
  database_url = "postgresql://localhost:5432/sample_db"
  postgres_database = PostgresDatabase(database_url)

  postgres_connection_mock = MagicMock()

  with patch("database.postgres_database.psycopg.connect", autospec=True) as postgres_connect:
    postgres_connect.return_value = postgres_connection_mock
    postgres_database.initialize()

  postgres_database_instance = postgres_database.get_database("sample_db")
  postgres_table_instance = postgres_database.get_table(postgres_database_instance, "first_table")

  with pytest.raises(Exception, match=r"^Record id is required for deletion$"):
    postgres_database.delete_one(postgres_table_instance)


def test_postgres_delete_one_calls_function_in_table_instance() -> None:
  database_url = "postgresql://localhost:5432/sample_db"
  postgres_database = PostgresDatabase(database_url)

  postgres_connection_mock = MagicMock()

  with patch("database.postgres_database.psycopg.connect", autospec=True) as postgres_connect:
    postgres_connect.return_value = postgres_connection_mock
    postgres_database.initialize()

  postgres_database_instance = postgres_database.get_database("sample_db")
  postgres_table_instance = postgres_database.get_table(postgres_database_instance, "first_table")

  postgres_database.delete_one(postgres_table_instance, "123")

  postgres_connection_mock.execute.assert_called_once()
  assert postgres_connection_mock.execute.call_args.args[1] == ["123"]
  postgres_connection_mock.commit.assert_called_once()


def test_postgres_delete_many_throws_exception_if_table_not_provided() -> None:
  database_url = "postgresql://localhost:5432/sample_db"
  postgres_database = PostgresDatabase(database_url)

  postgres_connection_mock = MagicMock()

  with patch("database.postgres_database.psycopg.connect", autospec=True) as postgres_connect:
    postgres_connect.return_value = postgres_connection_mock
    postgres_database.initialize()

  with pytest.raises(Exception, match=r"^Table instance is required.$"):
    postgres_database.delete_many()


def test_postgres_delete_many_throws_exception_if_filter_not_provided() -> None:
  database_url = "postgresql://localhost:5432/sample_db"
  postgres_database = PostgresDatabase(database_url)

  postgres_connection_mock = MagicMock()

  with patch("database.postgres_database.psycopg.connect", autospec=True) as postgres_connect:
    postgres_connect.return_value = postgres_connection_mock
    postgres_database.initialize()

  postgres_database_instance = postgres_database.get_database("sample_db")
  postgres_table_instance = postgres_database.get_table(postgres_database_instance, "first_table")

  with pytest.raises(Exception, match=r"^Filter expression is required.$"):
    postgres_database.delete_many(postgres_table_instance)


def test_postgres_delete_many_calls_function_in_table_instance() -> None:
  database_url = "postgresql://localhost:5432/sample_db"
  postgres_database = PostgresDatabase(database_url)

  postgres_connection_mock = MagicMock()

  with patch("database.postgres_database.psycopg.connect", autospec=True) as postgres_connect:
    postgres_connect.return_value = postgres_connection_mock
    postgres_database.initialize()

  postgres_database_instance = postgres_database.get_database("sample_db")
  postgres_table_instance = postgres_database.get_table(postgres_database_instance, "first_table")

  postgres_database.delete_many(postgres_table_instance, {"id": 123})

  postgres_connection_mock.execute.assert_called_once()
  assert postgres_connection_mock.execute.call_args.args[1] == [123]
  postgres_connection_mock.commit.assert_called_once()
