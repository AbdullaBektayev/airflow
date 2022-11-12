from django.db import models

from apps.common.models import CoreModel


class Provider(CoreModel):
    title = models.CharField(max_length=300, unique=True, db_index=True)
    url = models.URLField()

    def __str__(self):
        return f"title: [{self.title}], url: [{self.url}]"
