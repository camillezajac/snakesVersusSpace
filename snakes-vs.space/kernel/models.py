from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class ScoreModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    accuracy = models.FloatField()
    time_s = models.FloatField()
