from django.shortcuts import render, redirect
from django.urls import reverse

from managers.battle_manager import BattleManager
from managers.character_manager import CharacterManager

import random

from .models import Enemy
from character.models import Character

# Create your views here.


battle_manager = BattleManager()
character_manager = CharacterManager()


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
            character_manager.get_reward(player, int(request.GET['reward']), 'exp')
    return redirect('arena')
