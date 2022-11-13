from src.apps.flights.models import AirflowSearch, Ticket
from src.apps.flights.tasks import get_search_results_from_providers


def test_get_search_results_from_providers(
    db,
    airflow_search,
    mocked_provider_a_search,
    mocked_provider_b_search,
    provider_a,
    provider_b,
    currency_usd,
    currency_eur,
):
    airflow = airflow_search()
    assert Ticket.objects.count() == 0
    assert airflow.state == AirflowSearch.PENDING

    task = get_search_results_from_providers.s(airflow_search_uuid=airflow.uuid).apply()
    airflow.refresh_from_db()
    assert Ticket.objects.count() == 2
    assert task.result == {"result": "Search completed"}
    assert airflow.state == AirflowSearch.COMPLETED
