from typing import Tuple

from src.apps.flights.api.v1.views.airflow_search_views import AirflowSearchCreateAPIView, AirflowSearchRetrieveAPIView
from src.apps.flights.api.v1.views.provider_views import ProviderAListAPIView, ProviderBListAPIView


__all__: Tuple = (
    "ProviderAListAPIView",
    "ProviderBListAPIView",
    "AirflowSearchCreateAPIView",
    "AirflowSearchRetrieveAPIView",
)
