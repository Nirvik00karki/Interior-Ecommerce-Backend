# APP: estimation

from django.db import models


class EstimationCategory(models.Model):
    name = models.CharField(max_length=150)  # e.g. Commercial, Residential
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
