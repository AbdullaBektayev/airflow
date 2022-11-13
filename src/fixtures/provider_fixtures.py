from typing import Tuple

import pytest

from model_bakery import baker


__all__: Tuple = ("provider", "provider_a", "provider_b")


@pytest.fixture()
def provider(db):  # pylint: disable=unused-argument
    def _provider(**kwargs):
        return baker.make("flights.Provider", **kwargs)

    return _provider


@pytest.fixture()
def provider_a(db):  # pylint: disable=unused-argument

    return baker.make("flights.Provider", url="http://localhost:9000/api/v1/flights/provider-a/search/")


@pytest.fixture()
def provider_b(db):  # pylint: disable=unused-argument

    return baker.make("flights.Provider", url=" http://localhost:9000/api/v1/flights/provider-b/search/")
