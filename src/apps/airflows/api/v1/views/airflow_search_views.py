import asyncio
import httpx
from rest_framework import status
from rest_framework.generics import CreateAPIView, get_object_or_404
from rest_framework.response import Response

from apps.accounts.api.permissions import IsNotAuthenticated
from apps.airflows.models.airflow_models import Flight, Provider, AirflowSearch

from apps.airflows.models.airflow_models import Currency


class AirflowSearchCreateAPIView(CreateAPIView):
    permission_classes = [IsNotAuthenticated]

    @staticmethod
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

    async def search_on_providers(self, airflow_search):
        async for provider in Provider.objects.all():
            flight_create_list = await self.provider_search(provider_url=provider.url, airflow_search=airflow_search)
            Flight.objects.bulk_create(flight_create_list)
        airflow_search.state = AirflowSearch.COMPLETED
        airflow_search.save(update_fields=("state",))
        return airflow_search

    def post(self, request, *args, **kwargs):
        airflow_search = AirflowSearch.objects.create()
        serializer = self.get_serializer(airflow_search)
        headers = self.get_success_headers(serializer.data)
        loop = asyncio.get_event_loop()
        loop.create_task(self.search_on_providers(airflow_search=airflow_search))
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

