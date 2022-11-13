from src.apps.flights.models import AirflowSearch
from src.apps.flights.tasks import get_search_results_from_providers


def test_get_search_results_from_providers(db, airflow_search):
    airflow = airflow_search()
    assert airflow.state == AirflowSearch.PENDING

    task = get_search_results_from_providers.s(airflow_search_uuid=airflow.uuid).apply()
    airflow.refresh_from_db()

    assert task.result == {"result": "Search completed"}
    assert airflow.state == AirflowSearch.COMPLETED
