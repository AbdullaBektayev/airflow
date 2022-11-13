import pytest

PROVIDER_BASE_URL = "http://localhost:9000/api/v1/flights/"


@pytest.fixture()
def mocked_provider_a_search(requests_mock, json_data_by_path):
    response_data = json_data_by_path("./src/fixtures/data/search_a.json")
    url = PROVIDER_BASE_URL + "provider-a/search/"
    requests_mock.post(
        url=url,
        json=response_data,
        status_code=200,
    )


@pytest.fixture()
def mocked_provider_b_search(requests_mock, json_data_by_path):
    response_data = json_data_by_path("./src/fixtures/data/search_b.json")
    url = PROVIDER_BASE_URL + "provider-b/search/"
    requests_mock.post(
        url=url,
        json=response_data,
        status_code=200,
    )
