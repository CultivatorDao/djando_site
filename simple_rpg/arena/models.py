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
    # level = models.IntegerField(default=1)


class ColosseumBattle(models.Model):
    class Status(models.IntegerChoices):
        ONGOING = 0, 'Ongoing'
        FINISHED = 1, 'Finished'

    player = models.ForeignKey(to=Character, on_delete=models.CASCADE, related_name='battles')
    # player = models.OneToOneField(to="Character", on_delete=models.CASCADE, related_name='battles')
    enemy_data = models.TextField()

    status = models.BooleanField(choices=Status.choices, default=Status.ONGOING)
    is_initialized = models.BooleanField(default=False)
    # WIP. Use only after skill update
    # turn_data = models.TextField()
    # turn_number = models.IntegerField(default=1)

    # battle_log_data = models.TextField()

    is_finished = models.BooleanField(default=False)
    is_won = models.BooleanField(default=False)

    def __init__(self, *args, **kwargs):
        super(ColosseumBattle, self).__init__(*args, **kwargs)

        if self.enemy_data:
            self.enemy = json.loads(self.enemy_data)
            if not self.is_initialized:
                self.enemy['max_health'] = self.enemy['health']
                self.is_initialized = True
        else:
            self.enemy = {}

        # if self.turn_data:
        #     self.turn = json.loads(self.turn_data)
        # else:
        #     self.turn = {}

        # if self.battle_log_data:
        #     self.battle_log = json.loads(self.battle_log_data)
        # else:
        #     self.battle_log = {}

    def save(self, *args, **kwargs):
        self.enemy_data = json.dumps(self.enemy)
        # self.turn_data = json.dumps(self.turn)
        # self.battle_log_data = json.dumps(self.battle_log)
        super(ColosseumBattle, self).save(*args, **kwargs)
