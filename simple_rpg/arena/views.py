from django.shortcuts import render

import random

from .models import Enemy
from character.models import Character

# Create your views here.


def index(request):
    enemy = Enemy.objects.all()[0]
    player = Character.objects.get(pk=1)
    data = {
        'enemy': {
            'name': enemy.name,
            'health': enemy.health,
            'damage': enemy.damage,
            'defence': enemy.defence
        },
        'character': {
            'name': player.name,
            'health': player.max_hp,
            'damage': player.damage,
            'defence': player.defence
        }
    }
    return render(request, 'arena/index.html', data)
