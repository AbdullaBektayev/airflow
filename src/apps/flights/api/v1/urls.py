from django.urls import path

from src.apps.flights.api.v1.views.airflow_search_views import AirflowSearchCreateAPIView
from src.apps.flights.api.v1.views.provider_views import ProviderAListAPIView, ProviderBListAPIView

urlpatterns = [
    path("provider-a/search/", ProviderAListAPIView.as_view(), name="provider-a"),
    path("provider-b/search/", ProviderBListAPIView.as_view(), name="provider-b"),
    path("airflow/search/", AirflowSearchCreateAPIView.as_view(), name="airflow-search-create"),
    path("airflow/<uuid:pk>/<str:currency>/", ProviderBListAPIView.as_view(), name="airflow-search-retrieve"),
]
