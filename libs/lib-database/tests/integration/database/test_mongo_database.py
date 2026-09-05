import pytest  # type: ignore


@pytest.mark.integration
def test_mongodb_connection(mongo_resource):
  assert mongo_resource.client is not None
