from src import celery_app
from src.apps.flights.services.currency_services import CurrencyUpdater


@celery_app.task(
    name="flights.update_currency_task",
)
def update_currency_task():
    currency_service = CurrencyUpdater
    currency_service.update_currency()
    return {"result": "Currency was updated"}
