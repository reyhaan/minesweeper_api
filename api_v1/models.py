from django.db import models

# Create your models here.
class Game(models.Model):
    uuid        = models.CharField(max_length=255, primary_key=True)
    name        = models.CharField(max_length=120)
    mapState    = models.CharField(max_length=255)