from django.db import models

# Create your models here.
class Game(models.Model):
    uuid        = models.CharField(max_length=255, primary_key=True)
    name        = models.CharField(max_length=120)
    map_state    = models.TextField()
    map_original = models.TextField()
    has_lost    = models.BooleanField(default=False)
    has_won     = models.BooleanField(default=False)