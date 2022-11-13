from typing import Tuple

import pytest

from model_bakery import baker


__all__: Tuple = ("ticket", "ticket_a", "ticket_b")


@pytest.fixture()
def ticket(db):  # pylint: disable=unused-argument
    def _flight(**kwargs):
        return baker.make("flights.Ticket", **kwargs)

    return _flight


@pytest.fixture()
def ticket_a(db, airflow_search_kc, currency_eur):  # pylint: disable=unused-argument

    return baker.make(
        "flights.Ticket", airflow_search=airflow_search_kc, currency=currency_eur, base_price=291.84, tax_price=0
    )


@pytest.fixture()
def ticket_b(db, airflow_search_kc, currency_usd):  # pylint: disable=unused-argument

    return baker.make(
        "flights.Ticket", airflow_search=airflow_search_kc, currency=currency_usd, base_price=500, tax_price=0
    )
