from django.urls import path

from apps.provider.api.v1.views.provider_views import ProviderAListAPIView, ProviderBListAPIView

urlpatterns = [
    path("provider-a/search/", ProviderAListAPIView.as_view(), name="provider-a"),
    path("provider-b/search/", ProviderBListAPIView.as_view(), name="provider-b"),
]
