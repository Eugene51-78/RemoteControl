from django.db import models
from authentication.models import User

class Device (models.Model):
    user_id = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True)
    quality = models.IntegerField(720)
    name = models.CharField(max_length=20)
    isReady = models.BooleanField(False)

    def __str__(self):
        return self.name

class Model(models.Model):
    model_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.model_text
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)