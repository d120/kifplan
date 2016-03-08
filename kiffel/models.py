from django.db import models

class Kiffel(models.Model):
    nickname = models.CharField(max_length=100)

    class Meta:
        ordering = ('nickname',)
