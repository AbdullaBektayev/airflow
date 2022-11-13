import datetime
from typing import List

import httpx
import requests
import xmltodict
from rest_framework.generics import get_object_or_404

from src import settings
from src.apps.flights.models import Currency, Flight, Provider, AirflowSearch
from src import celery_app


def get_update_currency(response_dict) -> List[Currency]:
    currency_list = []
    for currency_dict in response_dict['rates']:
        item = currency_dict['item']
        currency_obj, created = Currency.objects.update_or_create(
            title=item['title'],
            defaults={"fullname": item['fullname'], "in_kzt": item['description']}
        )
        currency_list.append(currency_obj)
    return currency_list


@celery_app.task(
    name="flights.update_currency_task",
)
def update_currency_task():
    today = datetime.date.today()
    url = settings.NATIONAL_BANK_API + f'?fdate={today.strftime("%d.%m.%y")}'
    request = requests.post(url)
    response_dict = xmltodict.parse(request.text)
    get_update_currency(response_dict)
    return "Currency was updated"


async def provider_search(provider_url, airflow_search):
    async with httpx.AsyncClient() as client:
        search_results = await client.get(provider_url)
    flight_create_list = []
    for search_result in search_results.json():
        pricing = search_result['pricing']
        currency = get_object_or_404(Currency, title=pricing['currency'])
        flight_obj = Flight(
            currency=currency,
            base_price=pricing['base_price'],
            tax_price=pricing['tax_price'],
            airflow_search=airflow_search
        )
        flight_create_list.append(flight_obj)
    return flight_create_list


@celery_app.task(
    name="flights.get_search_results_from_providers",
)
def get_search_results_from_providers(airflow_search_uuid):
    for provider in Provider.objects.all():
        flight_create_list = provider_search(provider_url=provider.url, airflow_search=airflow_search)
        Flight.objects.bulk_create(flight_create_list)
    airflow_search = AirflowSearch.objects.get(uuid=airflow_search_uuid)
    airflow_search.state = AirflowSearch.COMPLETED
    airflow_search.save(update_fields=("state",))
    return {"result": "Search completed"}
