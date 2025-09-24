import uuid

from django.db import models


class Component(models.Model):
    name = models.CharField(max_length=200)
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    description = models.CharField(max_length=500)
    pub_date = models.DateTimeField("date published")

    def __str__(self):
        return f"{self.name}: {self.description}"
