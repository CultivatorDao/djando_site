from django.db import models

# Create your models here.


class Enemy(models.Model):
    name = models.CharField(max_length=255)
    health = models.IntegerField(default=100)
    damage = models.IntegerField(default=10)
    defence = models.IntegerField(default=5)
    gold_reward = models.IntegerField(default=0)
    exp_reward = models.IntegerField(default=0)
