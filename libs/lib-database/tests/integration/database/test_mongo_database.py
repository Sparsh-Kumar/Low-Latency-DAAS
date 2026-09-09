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


@pytest.mark.integration
def test_find_many_throws_exception_if_table_name_not_provided(
  mongodb_test_connection_uri: str,
  mongodb_test_database_name: str,
  mongodb_test_collection_name: str,
  mongo_resource_with_inserted_fixtures: MongoResource,
) -> None:

  mongo_database = MongoDatabase(mongodb_test_connection_uri)

  mongo_database.initialize()

  with pytest.raises(Exception, match=r"^Table instance is required.$"):
    mongo_database.find_many(None, {"age": 25})


@pytest.mark.integration
def test_find_many_returns_multiple_matched_records(
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

  multiple_matched_records = list(mongo_database.find_many(table_handle, {"age": 25}))

  assert multiple_matched_records is not None
  assert len(multiple_matched_records) > 0
  assert all(record["age"] == 25 for record in multiple_matched_records)


@pytest.mark.integration
def test_insert_one_throws_exception_if_table_name_not_provided(
  mongodb_test_connection_uri: str,
  mongodb_test_database_name: str,
  mongodb_test_collection_name: str,
  mongo_resource_with_inserted_fixtures: MongoResource,
) -> None:

  mongo_database = MongoDatabase(mongodb_test_connection_uri)

  mongo_database.initialize()

  with pytest.raises(Exception, match=r"^Table instance is required.$"):
    mongo_database.insert_one(None, {"name": "Test User", "age": 30})


@pytest.mark.integration
def test_insert_one_throws_exception_if_record_not_provided(
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

  with pytest.raises(Exception, match=r"^Record to insert is required.$"):
    mongo_database.insert_one(table_handle)


@pytest.mark.integration
def test_insert_one_inserts_a_single_record(
  mongodb_test_connection_uri: str,
  mongodb_test_database_name: str,
  mongodb_test_collection_name: str,
  mongo_resource_with_inserted_fixtures: MongoResource,
) -> None:

  test_database_name = mongodb_test_database_name
  test_table_name = mongodb_test_collection_name
  record_to_insert = {"name": "Test User", "age": 30}

  mongo_database = MongoDatabase(mongodb_test_connection_uri)

  mongo_database.initialize()
  database_handle = mongo_database.get_database(test_database_name)
  table_handle = mongo_database.get_table(database_handle, test_table_name)

  mongo_database.insert_one(table_handle, record_to_insert)
  inserted_record = mongo_database.find_one(table_handle, record_to_insert)

  assert inserted_record is not None
  assert inserted_record["name"] == record_to_insert["name"]
  assert inserted_record["age"] == record_to_insert["age"]


@pytest.mark.integration
def test_insert_many_throws_exception_if_table_name_not_provided(
  mongodb_test_connection_uri: str,
  mongodb_test_database_name: str,
  mongodb_test_collection_name: str,
  mongo_resource_with_inserted_fixtures: MongoResource,
) -> None:

  mongo_database = MongoDatabase(mongodb_test_connection_uri)

  mongo_database.initialize()

  with pytest.raises(Exception, match=r"^Table instance is required.$"):
    mongo_database.insert_many(None, [{"name": "Test User", "age": 30}])


@pytest.mark.integration
def test_insert_many_throws_exception_if_records_not_provided(
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

  with pytest.raises(Exception, match=r"^Records to insert are required.$"):
    mongo_database.insert_many(table_handle)


@pytest.mark.integration
def test_insert_many_inserts_multiple_records(
  mongodb_test_connection_uri: str,
  mongodb_test_database_name: str,
  mongodb_test_collection_name: str,
  mongo_resource_with_inserted_fixtures: MongoResource,
) -> None:

  test_database_name = mongodb_test_database_name
  test_table_name = mongodb_test_collection_name
  records_to_insert = [
    {"name": "Test User One", "age": 30},
    {"name": "Test User Two", "age": 30},
  ]

  mongo_database = MongoDatabase(mongodb_test_connection_uri)

  mongo_database.initialize()
  database_handle = mongo_database.get_database(test_database_name)
  table_handle = mongo_database.get_table(database_handle, test_table_name)

  mongo_database.insert_many(table_handle, records_to_insert)
  inserted_records = list(mongo_database.find_many(table_handle, {"age": 30}))

  assert inserted_records is not None
  assert len(inserted_records) >= len(records_to_insert)
  assert any(record["name"] == "Test User One" for record in inserted_records)
  assert any(record["name"] == "Test User Two" for record in inserted_records)


@pytest.mark.integration
def test_delete_one_throws_exception_if_table_name_not_provided(
  mongodb_test_connection_uri: str,
  mongodb_test_database_name: str,
  mongodb_test_collection_name: str,
  mongo_resource_with_inserted_fixtures: MongoResource,
) -> None:

  mongo_database = MongoDatabase(mongodb_test_connection_uri)

  mongo_database.initialize()

  with pytest.raises(Exception, match=r"^Table instance is required.$"):
    mongo_database.delete_one(None, "record_id")


@pytest.mark.integration
def test_delete_one_throws_exception_if_record_id_not_provided(
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

  with pytest.raises(Exception, match=r"^Record id is required for deletion.$"):
    mongo_database.delete_one(table_handle)


@pytest.mark.integration
def test_delete_one_deletes_a_single_record(
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
  record_to_delete = mongo_database.find_one(table_handle, {"age": 25})

  assert record_to_delete is not None

  mongo_database.delete_one(table_handle, record_to_delete["_id"])
  deleted_record = mongo_database.find_one(table_handle, {"_id": record_to_delete["_id"]})

  assert deleted_record is None


@pytest.mark.integration
def test_delete_many_throws_exception_if_table_name_not_provided(
  mongodb_test_connection_uri: str,
  mongodb_test_database_name: str,
  mongodb_test_collection_name: str,
  mongo_resource_with_inserted_fixtures: MongoResource,
) -> None:

  mongo_database = MongoDatabase(mongodb_test_connection_uri)

  mongo_database.initialize()

  with pytest.raises(Exception, match=r"^Table instance is required.$"):
    mongo_database.delete_many(None, {"age": 25})


@pytest.mark.integration
def test_delete_many_deletes_multiple_records(
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

  mongo_database.delete_many(table_handle, {"age": 25})
  deleted_records = list(mongo_database.find_many(table_handle, {"age": 25}))

  assert deleted_records == []
