"""Django Model for tracking applications defined within an APBR policy."""

import logging

from django.db import models


LOGGER = logging.getLogger(__name__)


class ApbrProfile(models.Model):
    name = models.CharField(max_length=64)
    smell = models.CharField(max_length=32)

    def __str__(self):
        return self.name