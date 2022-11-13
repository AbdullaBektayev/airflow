from rest_framework import status
from rest_framework.reverse import reverse

from src.apps.flights.models import AirflowSearch


def test_airflow_search_create_success(
    db, unauthorized_api_client, json_data_by_path, mocker
):
    response = unauthorized_api_client.post(reverse("api-v1-flights:airflow-search-create"))
    assert response.status_code == status.HTTP_201_CREATED
    assert "search_id" in response.json()
    assert AirflowSearch.objects.count() == 1
    airflow_search_obj = AirflowSearch.objects.first()
    assert airflow_search_obj.state == AirflowSearch.PENDING


def test_airflow_search_by_uuid_success(
    db, unauthorized_api_client, json_data_by_path, airflow_search_kc, currency_kzt
):
    response = unauthorized_api_client.get(
        reverse(
            "api-v1-flights:airflow-search-retrieve",
            kwargs={"pk": airflow_search_kc.uuid, "currency_title": currency_kzt.title}
        ),
    )
    print(response.json())
    assert response.status_code == status.HTTP_200_OK
    # assert response.json() == json_data_by_path()
