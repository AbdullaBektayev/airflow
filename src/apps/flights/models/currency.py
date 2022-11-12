from django.db import models

from src.apps.common.models import CoreModel
from settings import DEFAULT_MAX_DIGITS, DEFAULT_DECIMAL_PLACES


class Currency(CoreModel):

    title = models.CharField(max_length=3, unique=True, db_index=True)
    fullname = models.CharField(max_length=300)
    in_kzt = models.DecimalField(max_digits=DEFAULT_MAX_DIGITS, decimal_places=DEFAULT_DECIMAL_PLACES)

    def __str__(self):
        return f"fullname: [{self.fullname}], in_kzt: [{self.in_kzt}]"

