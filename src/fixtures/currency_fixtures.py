from typing import Tuple

import pytest

from model_bakery import baker


__all__: Tuple = (
    "currency", "currency_usd", "currency_eur"
)


@pytest.fixture()
def currency(db):  # pylint: disable=unused-argument
    def _currency(**kwargs):
        return baker.make("flights.Currency", **kwargs)

    return _currency


@pytest.fixture()
def currency_usd(db):  # pylint: disable=unused-argument

    return baker.make(
        "flights.Currency", title='USD', fullname='dollar', in_kzt=470.00
    )


@pytest.fixture()
def currency_eur(db):  # pylint: disable=unused-argument

    return baker.make(
        "flights.Currency", title='EUR', fullname='euro', in_kzt=500.00
    )

