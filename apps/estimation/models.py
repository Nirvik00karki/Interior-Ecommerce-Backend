# APP: estimation

from django.db import models


class EstimationCategory(models.Model):
    name = models.CharField(max_length=150)  # e.g. Commercial, Residential

    def __str__(self):
        return self.name
