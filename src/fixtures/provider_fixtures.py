from typing import Tuple

import pytest

from model_bakery import baker


__all__: Tuple = ("provider", "provider_a", "provider_b")

from src.apps.flights.models import Provider


@pytest.fixture()
def provider(db):  # pylint: disable=unused-argument
    def _provider(**kwargs):
        return baker.make("flights.Provider", **kwargs)

    return _provider


@pytest.fixture()
def provider_a(db):  # pylint: disable=unused-argument
    provider, created = Provider.objects.get_or_create(
        title="provider_a", defaults={"url": "http://localhost:9000/api/v1/flights/provider-a/search/"}
    )
    return provider


@pytest.fixture()
def provider_b(db):  # pylint: disable=unused-argument
    provider, created = Provider.objects.get_or_create(
        title="provider_b", defaults={"url": "http://localhost:9000/api/v1/flights/provider-b/search/"}
    )
    return provider
