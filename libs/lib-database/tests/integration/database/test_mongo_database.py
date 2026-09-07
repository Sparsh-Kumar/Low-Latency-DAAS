import pytest  # type: ignore
from dotenv import load_dotenv  # type: ignore

from database.mongo_database import MongoDatabase
from tests.typings import MongoResource

load_dotenv()


@pytest.mark.integration
def test_mongodb_test_connection_uri_returns_non_empty_uri(
  mongodb_test_connection_uri: str,
) -> None:
  assert mongodb_test_connection_uri is not None


@pytest.mark.integration
def test_get_database_throws_exception_if_database_name_not_provided(
  mongodb_test_connection_uri: str,
) -> None:

  mongo_database = MongoDatabase(mongodb_test_connection_uri)

  mongo_database.initialize()
  with pytest.raises(Exception, match=r"^Database name is required.$"):
    mongo_database.get_database()


@pytest.mark.integration
def test_get_database_returns_non_empty_database_instance(
  mongodb_test_connection_uri: str,
  mongodb_test_database_name: str,
) -> None:

  test_database_name = mongodb_test_database_name
  mongo_database = MongoDatabase(mongodb_test_connection_uri)

  mongo_database.initialize()
  database_handle = mongo_database.get_database(test_database_name)

  assert database_handle is not None


@pytest.mark.integration
def test_get_table_throws_exception_if_database_name_not_provided(
  mongodb_test_connection_uri: str,
  mongodb_test_database_name: str,
  mongodb_test_collection_name: str,
) -> None:

  test_database_name = mongodb_test_database_name
  test_table_name = mongodb_test_collection_name
  mongo_database = MongoDatabase(mongodb_test_connection_uri)

  mongo_database.initialize()
  mongo_database.get_database(test_database_name)

  with pytest.raises(Exception, match=r"^Database instance is required.$"):
    mongo_database.get_table(None, test_table_name)


@pytest.mark.integration
def test_get_table_throws_exception_if_table_name_not_provided(
  mongodb_test_connection_uri: str,
  mongodb_test_database_name: str,
) -> None:

  test_database_name = mongodb_test_database_name
  mongo_database = MongoDatabase(mongodb_test_connection_uri)

  mongo_database.initialize()
  database_handle = mongo_database.get_database(test_database_name)

  with pytest.raises(Exception, match=r"^Table name is required.$"):
    mongo_database.get_table(database_handle, None)


@pytest.mark.integration
def test_get_table_returns_non_empty_table_instance(
  mongodb_test_connection_uri: str,
  mongodb_test_database_name: str,
  mongodb_test_collection_name: str,
) -> None:

  test_database_name = mongodb_test_database_name
  test_table_name = mongodb_test_collection_name
  mongo_database = MongoDatabase(mongodb_test_connection_uri)

  mongo_database.initialize()
  database_handle = mongo_database.get_database(test_database_name)
  table_handle = mongo_database.get_table(database_handle, test_table_name)

  assert table_handle is not None


@pytest.mark.integration
def test_find_one_throws_exception_if_table_name_not_provided(
  mongodb_test_connection_uri: str,
  mongodb_test_database_name: str,
  mongodb_test_collection_name: str,
  mongo_resource_with_inserted_fixtures: MongoResource,
) -> None:

  mongo_database = MongoDatabase(mongodb_test_connection_uri)

  mongo_database.initialize()

  with pytest.raises(Exception, match=r"^Table instance is required.$"):
    mongo_database.find_one(None, {"age": 25})


@pytest.mark.integration
def test_find_one_returns_a_single_matched_record(
  mongodb_test_connection_uri: str,
  mongodb_test_database_name: str,
  mongodb_test_collection_name: str,
  mongo_resource_with_inserted_fixtures: MongoResource,
) -> None:

  test_database_name = mongodb_test_database_name
  test_table_name = mongodb_test_collection_name

  mongo_database = MongoDatabase(mongodb_test_connection_uri)

  mongo_database.initialize()
  database_handle = mongo_database.get_database(test_database_name)
  table_handle = mongo_database.get_table(database_handle, test_table_name)

  single_matched_record = mongo_database.find_one(table_handle, {"age": 25})

  assert single_matched_record is not None
  assert single_matched_record["age"] == 25
