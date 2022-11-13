import pytest

from src.settings import NATIONAL_BANK_API

PROVIDER_BASE_URL = "http://localhost:9000/api/v1/flights/"


@pytest.fixture()
def mocked_provider_a_search(requests_mock, json_data_by_path):
    response_data = json_data_by_path("./src/fixtures/data/search_a.json")
    url = PROVIDER_BASE_URL + "provider-a/search/"
    requests_mock.post(
        url=url,
        json=response_data,
        status_code=201,
    )


@pytest.fixture()
def mocked_provider_b_search(requests_mock, json_data_by_path):
    response_data = json_data_by_path("./src/fixtures/data/search_b.json")
    url = PROVIDER_BASE_URL + "provider-b/search/"
    requests_mock.post(
        url=url,
        json=response_data,
        status_code=201,
    )


@pytest.fixture()
def mocked_national_bank_api(requests_mock, json_data_by_path):
    with open("./src/fixtures/data/national_bank_result.xml", 'r') as f:
        xml_file = f.read()
    # xml_str = ElementTree.tostring(xml_file, encoding='utf8', method='xml')
    url = NATIONAL_BANK_API + "?fdate=13.11.2022"
    requests_mock.get(
        url=url,
        text=xml_file,
        status_code=200,
    )
