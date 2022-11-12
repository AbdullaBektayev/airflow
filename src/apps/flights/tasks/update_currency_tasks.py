import datetime
from typing import List

import requests
import xmltodict

import settings
from apps.flights.models import Currency
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
