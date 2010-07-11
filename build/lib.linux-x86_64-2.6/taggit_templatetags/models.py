# no models in here
from django.db import models

class AModel(models.Model):
    name = models.CharField(max_length=50)