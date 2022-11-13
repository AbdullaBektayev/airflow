from typing import List

from src import celery_app
from src.apps.flights.models import Currency
from src.apps.flights.services.ariflow_services import AirflowService
from src.apps.flights.services.currency_services import CurrencyUpdater


def get_update_currency(response_dict) -> List[Currency]:
    currency_list = []
    for item in response_dict["rates"]["item"]:
        currency_obj, created = Currency.objects.update_or_create(
            title=item["title"], defaults={"fullname": item["fullname"], "in_kzt": item["description"]}
        )
        currency_list.append(currency_obj)
    return currency_list


@celery_app.task(
    name="flights.update_currency_task",
)
def update_currency_task():
    currency_service = CurrencyUpdater
    currency_service.update_currency()
    return {"result": "Currency was updated"}


@celery_app.task(
    name="flights.get_search_results_from_providers",
)
def get_search_results_from_providers(airflow_search_uuid):
    currency_service = AirflowService
    currency_service.get_search_results_from_providers(airflow_search_uuid=airflow_search_uuid)
    return {"result": "Search completed"}
