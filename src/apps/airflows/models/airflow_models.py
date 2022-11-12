from typing import Tuple

from django.db import models

from apps.common.models import CoreModel
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


class Currency(CoreModel):

    title = models.CharField(max_length=3, unique=True, db_index=True)
    fullname = models.CharField(max_length=300)
    in_kzt = models.DecimalField(max_digits=DEFAULT_MAX_DIGITS, decimal_places=DEFAULT_DECIMAL_PLACES)

    def __str__(self):
        return f"fullname: [{self.fullname}], in_kzt: [{self.in_kzt}]"


class AirflowSearch(CoreModel):
    PENDING: str = "pending"
    COMPLETED: str = "completed"
    STATES: Tuple = ((PENDING, PENDING), (COMPLETED, COMPLETED))

    state = models.CharField(choices=STATES, max_length=15, default=PENDING, verbose_name=_("state"))

    def __str__(self):
        return f"uuid: [{self.uuid}], state: [{self.state}]"


class Provider(CoreModel):
    title = models.CharField(max_length=300, unique=True, db_index=True)
    url = models.URLField()

    def __str__(self):
        return f"title: [{self.title}], url: [{self.url}]"
