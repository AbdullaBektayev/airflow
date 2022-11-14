import datetime

import pytest

from src.apps.flights.models import Currency
from src.apps.flights.tasks import update_currency_task


@pytest.mark.freeze_time("2022-11-13T10:45:00Z")
@pytest.mark.django_db(transaction=True)
def test_update_currency(
    db, currency_usd, currency_eur, currency_kzt, mocked_national_bank_api, celery_app, celery_worker
):
    assert Currency.objects.count() == 3

    task = update_currency_task.s().apply()
    assert Currency.objects.count() == 40

    currency_usd.refresh_from_db()
    currency_eur.refresh_from_db()

    assert float(currency_usd.in_kzt) == 462.01
    assert float(currency_eur.in_kzt) == 474.44
    assert task.result == {"result": "Currency was updated"}
