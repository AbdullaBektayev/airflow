import datetime
from typing import List

import requests
import xmltodict
from rest_framework.generics import get_object_or_404

from src import settings
from src.apps.flights.models import Currency, Ticket, Provider, AirflowSearch
from src import celery_app


def get_update_currency(response_dict) -> List[Currency]:
    currency_list = []
    for item in response_dict['rates']['item']:
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
    url = settings.NATIONAL_BANK_API + f'?fdate={today.strftime("%d.%m.%Y")}'
    request = requests.get(url)
    response_dict = xmltodict.parse(request.text)
    get_update_currency(response_dict)
    return {"result": "Currency was updated"}


def provider_search(provider_url, airflow_search):
    search_results = requests.post(provider_url)
    ticket_create_list = []
    for search_result in search_results.json():
        pricing = search_result['pricing']
        currency = get_object_or_404(Currency, title=pricing['currency'])
        ticket_obj = Ticket(
            currency=currency,
            base_price=pricing['base'],
            tax_price=pricing['taxes'],
            airflow_search=airflow_search
        )
        ticket_create_list.append(ticket_obj)
    return ticket_create_list


@celery_app.task(
    name="flights.get_search_results_from_providers",
)
def get_search_results_from_providers(airflow_search_uuid):
    airflow_search = AirflowSearch.objects.get(uuid=airflow_search_uuid)
    for provider in Provider.objects.all():
        ticket_create_list = provider_search(provider_url=provider.url, airflow_search=airflow_search)
        Ticket.objects.bulk_create(ticket_create_list)
    airflow_search.state = AirflowSearch.COMPLETED
    airflow_search.save(update_fields=("state",))
    return {"result": "Search completed"}
