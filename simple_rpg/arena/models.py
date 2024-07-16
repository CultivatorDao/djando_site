from django.db import models
import json

from character.models import Character

# Create your models here.


class Enemy(models.Model):
    name = models.CharField(max_length=255)
    health = models.IntegerField(default=100)
    damage = models.IntegerField(default=10)
    defence = models.IntegerField(default=5)
    gold_reward = models.IntegerField(default=0)
    exp_reward = models.IntegerField(default=0)


class StrongEnemy(models.Model):
    name = models.CharField(max_length=255)
    health = models.IntegerField(default=100)
    damage = models.IntegerField(default=10)
    defence = models.IntegerField(default=5)
    gold_reward = models.IntegerField(default=0)
    exp_reward = models.IntegerField(default=0)


class ColosseumBattle(models.Model):
    player = models.ForeignKey(to=Character, on_delete=models.CASCADE, blank=True, related_name='battles')
    enemy_data = models.TextField()

    def __init__(self, *args, **kwargs):
        super(ColosseumBattle, self).__init__(*args, **kwargs)

        if self.enemy_data:
            self.enemy = json.loads(self.enemy_data)
        else:
            self.enemy = {}

    def save(self, *args, **kwargs):
        self.enemy_data = json.dumps(self.enemy)
        super(ColosseumBattle, self).save(*args, **kwargs)
