import datetime

from typing import List

import requests
import xmltodict

from src import settings
from src.apps.flights.models import Currency


class CurrencyUpdater:
    @staticmethod
    def _get_update_currency(response_dict) -> List[Currency]:
        currency_list = []
        for item in response_dict["rates"]["item"]:
            currency_obj, created = Currency.objects.update_or_create(
                title=item["title"], defaults={"fullname": item["fullname"], "in_kzt": item["description"]}
            )
            currency_list.append(currency_obj)
        return currency_list

    @staticmethod
    def _get_query_param():
        today = datetime.date.today()
        query_param = f'?fdate={today.strftime("%d.%m.%Y")}'
        return query_param

    @classmethod
    def update_currency(cls):
        query_param = cls._get_query_param()
        url = settings.NATIONAL_BANK_API + query_param
        request = requests.get(url)
        response_dict = xmltodict.parse(request.text)
        cls._get_update_currency(response_dict)
