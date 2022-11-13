from django.db.models import Prefetch, F, Value, CharField
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema, no_body
from rest_framework import status
from rest_framework.generics import CreateAPIView, get_object_or_404, RetrieveAPIView
from rest_framework.response import Response

from src.apps.flights.api.v1.serializers import AirflowSearchCreateSerializer
from src.apps.flights.api.v1.serializers.airflow_search_serializers import AirflowSearchRetrieveSerializer
from src.apps.flights.models import Flight, AirflowSearch, Currency
from src.apps.flights.tasks import get_search_results_from_providers


class AirflowSearchCreateAPIView(CreateAPIView):
    serializer_class = AirflowSearchCreateSerializer
    queryset = AirflowSearch.objects.all()

    @swagger_auto_schema(
        request_body=no_body,
        responses={status.HTTP_201_CREATED: openapi.Response("UUID of AirflowSearch", AirflowSearchCreateSerializer)}
    )
    def post(self, request, *args, **kwargs):
        airflow_search = AirflowSearch.objects.create()
        serializer = self.get_serializer(airflow_search)
        headers = self.get_success_headers(serializer.data)
        get_search_results_from_providers.delay(airflow_search_uuid=airflow_search.uuid)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class AirflowSearchRetrieveAPIView(RetrieveAPIView):
    queryset = AirflowSearch.objects.all()
    serializer_class = AirflowSearchRetrieveSerializer

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):  # pragma: no cover
            return AirflowSearch.objects.none()

        currency = get_object_or_404(Currency, title=self.kwargs.get("currency_title"))
        queryset = super().get_queryset().prefetch_related(
            Prefetch(
                "flights",
                Flight.objects.select_related("currency").annotate(
                    total_price=F("base_price") + F("tax_price"),
                    converted_price=(F("total_price")*F("currency__in_kzt"))/currency.in_kzt,
                    converted_currency=Value(currency.title, CharField())
                ).order_by(
                    "converted_price"
                )
            )
        )

        return queryset
