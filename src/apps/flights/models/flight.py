from django.db import models

from src.apps.common.models import CoreModel
from django.utils.translation import gettext_lazy as _
from settings import DEFAULT_MAX_DIGITS, DEFAULT_DECIMAL_PLACES


class Flight(CoreModel):

    base_price = models.DecimalField(max_digits=DEFAULT_MAX_DIGITS, decimal_places=DEFAULT_DECIMAL_PLACES)
    tax_price = models.DecimalField(max_digits=DEFAULT_MAX_DIGITS, decimal_places=DEFAULT_DECIMAL_PLACES)
    airflow_search = models.ForeignKey(
        to="airflow.AirflowSearch",
        on_delete=models.RESTRICT,
        verbose_name=_("airflow_search"),
        help_text=_("airflow_search"),
        related_name="flights",
    )
    currency = models.ForeignKey(
        to="airflow.Currency",
        on_delete=models.RESTRICT,
        verbose_name=_("currency"),
        help_text=_("currency"),
        related_name="flights",
    )

    def __str__(self):
        return f"pricing: [base_price: {self.base_price}, tax_price: {self.tax_price}, ], currency: [{self.currency}]"
