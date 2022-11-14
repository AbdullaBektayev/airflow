from rest_framework import status
from rest_framework.reverse import reverse

from src.apps.flights.models import AirflowSearch


def test_airflow_search_create_success(db, unauthorized_api_client, json_data_by_path, mocker):
    mocked_task = mocker.patch(
        "src.apps.flights.tasks.search_result_tasks.get_search_results_from_providers.apply_async", return_value=None
    )
    response = unauthorized_api_client.post(reverse("api-v1-flights:airflow-search-create"))
    assert response.status_code == status.HTTP_201_CREATED
    assert "search_id" in response.json()
    assert AirflowSearch.objects.count() == 1
    mocked_task.assert_called_once()
    airflow_search_obj = AirflowSearch.objects.first()
    assert airflow_search_obj.state == AirflowSearch.PENDING


def test_airflow_search_by_uuid_success(
    db,
    unauthorized_api_client,
    json_data_by_path,
    airflow_search_kc,
    currency_kzt,
    ticket_a,
    ticket_b,
    remove_uuid_fields_from_response,
):
    response = unauthorized_api_client.get(
        reverse(
            "api-v1-flights:airflow-search-retrieve",
            kwargs={"pk": airflow_search_kc.uuid, "currency_title": currency_kzt.title},
        ),
    )
    assert response.status_code == status.HTTP_200_OK
    assert remove_uuid_fields_from_response(response.json()) == json_data_by_path(
        "./src/apps/flights/tests/data/airflow_search_retrieve_response.json"
    )
