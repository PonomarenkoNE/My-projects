from django.db import models
from django.contrib.auth.models import User


class City(models.Model):
    name = models.CharField(max_length=20)


class Subscribe(models.Model):
    follower = models.ForeignKey(User, related_name='subscriber', on_delete=models.CASCADE)
    following = models.CharField(max_length=20)
    notification_period = models.IntegerField(default=2)
