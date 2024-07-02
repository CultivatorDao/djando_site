from django.db import models


class Character(models.Model):
    name = models.CharField(max_length=20)
    max_hp = models.IntegerField(default=100)
    current_hp = models.IntegerField(default=100)
    damage = models.IntegerField(default=10)
    defence = models.IntegerField(default=5)
    level = models.IntegerField(default=1)
    exp_current = models.IntegerField(default=0)
    exp_next = models.IntegerField(default=100)
    attribute_points = models.IntegerField(default=5)
