from src import celery_app
from src.apps.flights.services.ariflow_services import AirflowService


@celery_app.task(
    name="flights.get_search_results_from_providers",
)
def get_search_results_from_providers(airflow_search_uuid):
    currency_service = AirflowService
    currency_service.get_search_results_from_providers(airflow_search_uuid=airflow_search_uuid)
    return {"result": "Search completed"}
