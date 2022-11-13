from django.db import models

from src.apps.common.models import CoreModel
from django.utils.translation import gettext_lazy as _
from src.settings import DEFAULT_MAX_DIGITS, DEFAULT_DECIMAL_PLACES


class Ticket(CoreModel):

    base_price = models.DecimalField(max_digits=DEFAULT_MAX_DIGITS, decimal_places=DEFAULT_DECIMAL_PLACES)
    tax_price = models.DecimalField(max_digits=DEFAULT_MAX_DIGITS, decimal_places=DEFAULT_DECIMAL_PLACES)
    airflow_search = models.ForeignKey(
        to="flights.AirflowSearch",
        on_delete=models.RESTRICT,
        verbose_name=_("airflow_search"),
        help_text=_("airflow_search"),
        related_name="tickets",
    )
    currency = models.ForeignKey(
        to="flights.Currency",
        on_delete=models.RESTRICT,
        verbose_name=_("currency"),
        help_text=_("currency"),
        related_name="tickets",
    )

    def __str__(self):
        return f"pricing: [base_price: {self.base_price}, tax_price: {self.tax_price}, ], currency: [{self.currency}]"
