from django.urls import path

from src.apps.flights.api.v1.views.airflow_search_views import AirflowSearchCreateAPIView, AirflowSearchRetrieveAPIView
from src.apps.flights.api.v1.views.provider_views import ProviderAListAPIView, ProviderBListAPIView

urlpatterns = [
    path("provider-a/search/", ProviderAListAPIView.as_view(), name="provider-a-search"),
    path("provider-b/search/", ProviderBListAPIView.as_view(), name="provider-b-search"),
    path("airflow/search/", AirflowSearchCreateAPIView.as_view(), name="airflow-search-create"),
    path("airflow/<uuid:pk>/<str:currency_title>/", AirflowSearchRetrieveAPIView.as_view(), name="airflow-search-retrieve"),
]
