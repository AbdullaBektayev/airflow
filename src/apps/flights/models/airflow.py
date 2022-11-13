from typing import Tuple

from django.db import models
from django.utils.translation import gettext_lazy as _

from src.apps.common.models import CoreModel


class AirflowSearch(CoreModel):
    PENDING: str = "pending"
    COMPLETED: str = "completed"
    STATES: Tuple = ((PENDING, PENDING), (COMPLETED, COMPLETED))

    state = models.CharField(choices=STATES, max_length=15, default=PENDING, verbose_name=_("state"))

    def __str__(self):
        return f"uuid: [{self.uuid}], state: [{self.state}]"
