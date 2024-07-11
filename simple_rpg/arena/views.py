from django.shortcuts import render, redirect
from django.urls import reverse

from managers.battle_manager import BattleManager

import random

from .models import Enemy
from character.models import Character

# Create your views here.


battle_manager = BattleManager()


def index(request):
    enemy = Enemy.objects.all()[random.randint(0, 1)]
    player = Character.objects.get(pk=1)
    battle_manager.next = reverse('result')
    data = battle_manager.arena_fight_calculate(player=player, enemy=enemy)
    return render(request, 'arena/index.html', data)


def battle_result(request):
    player = Character.objects.get(pk=1)
    if request.GET:
        if request.GET['outcome'] == 'victory':
            player.exp_current += int(request.GET['reward'])
            if player.exp_current >= player.exp_next:
                player.level += 1
                player.attribute_points += 2
                player.exp_current -= player.exp_next
                player.exp_next += player.exp_next * 0.2
            player.save()
    return redirect('arena')
