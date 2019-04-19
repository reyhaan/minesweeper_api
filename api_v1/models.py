from django.db import models

# Create your models here.
class Game(models.Model):
    uuid        = models.CharField(max_length=255, primary_key=True)
    name        = models.CharField(max_length=120)
    map_state    = models.CharField(max_length=10000)
    map_original = models.CharField(max_length=10000)