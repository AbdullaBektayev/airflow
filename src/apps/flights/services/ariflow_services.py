from rest_framework.generics import get_object_or_404

import requests

from src.apps.flights.models import AirflowSearch, Currency, Provider, Ticket


class AirflowService:
    @staticmethod
    def _provider_search(provider_url, airflow_search):
        search_results = requests.post(provider_url)
        ticket_create_list = []
        for search_result in search_results.json():
            pricing = search_result["pricing"]
            currency = get_object_or_404(Currency, title=pricing["currency"])
            ticket_obj = Ticket(
                currency=currency, base_price=pricing["base"], tax_price=pricing["taxes"], airflow_search=airflow_search
            )
            ticket_create_list.append(ticket_obj)
        return ticket_create_list

    @classmethod
    def get_search_results_from_providers(cls, airflow_search_uuid):
        print(airflow_search_uuid)
        airflow_search = AirflowSearch.objects.get(uuid=airflow_search_uuid)
        for provider in Provider.objects.all():
            ticket_create_list = cls._provider_search(provider_url=provider.url, airflow_search=airflow_search)
            Ticket.objects.bulk_create(ticket_create_list)
        airflow_search.state = AirflowSearch.COMPLETED
        airflow_search.save(update_fields=("state",))
