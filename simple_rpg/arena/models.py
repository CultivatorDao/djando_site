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
    class Status(models.IntegerChoices):
        ONGOING = 0, 'Ongoing'
        FINISHED = 1, 'Finished'

    player = models.ForeignKey(to=Character, on_delete=models.CASCADE, related_name='battles')
    enemy_data = models.TextField()

    status = models.BooleanField(choices=Status.choices, default=Status.ONGOING)
    is_initialized = models.BooleanField(default=False)
    # is_finished = models.BooleanField(default=False)
    # is_won = models.BooleanField(default=False)

    def __init__(self, *args, **kwargs):
        super(ColosseumBattle, self).__init__(*args, **kwargs)

        if self.enemy_data:
            self.enemy = json.loads(self.enemy_data)
            if not self.is_initialized:
                self.enemy['max_health'] = self.enemy['health']
                self.is_initialized = True
        else:
            self.enemy = {}

    def save(self, *args, **kwargs):
        self.enemy_data = json.dumps(self.enemy)
        super(ColosseumBattle, self).save(*args, **kwargs)
