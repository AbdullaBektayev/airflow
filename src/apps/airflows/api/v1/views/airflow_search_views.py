import asyncio
import httpx
from django.db.models import Prefetch, F
from rest_framework import status
from rest_framework.generics import CreateAPIView, get_object_or_404, RetrieveAPIView
from rest_framework.response import Response

from apps.airflows.api.v1.serializers import AirflowSearchCreateSerializer
from apps.airflows.models import Flight, Provider, AirflowSearch

from apps.airflows.models import Currency


class AirflowSearchCreateAPIView(CreateAPIView):
    serializer_class = AirflowSearchCreateSerializer

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


class AirflowSearchRetrieveAPIView(RetrieveAPIView):

    def get_queryset(self):

        currency = get_object_or_404(Currency, title=self.kwargs.get("currency_title"))

        queryset = super().get_queryset().prefetch_related(
            Prefetch(
                "flights",
                Flight.objects.select_related("currency").annotate(
                    total_price=F("base_price") + F("tax_price"),
                    converted_price=(F("total_price")*F("currency__in_kzt"))/currency.in_kzt,
                    converted_currency=currency.title
                ).order_by(
                    "converted_price"
                )
            )
        )

        return queryset
