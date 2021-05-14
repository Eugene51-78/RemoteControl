from django.db import models
from authentication.models import User

class Device (models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, to_field='id')
    quality = models.IntegerField()
    name = models.CharField(max_length=20)
    isReady = models.BooleanField()