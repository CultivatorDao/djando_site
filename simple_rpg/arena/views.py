from django.shortcuts import render, redirect
from django.urls import reverse

import random

from .models import Enemy
from character.models import Character

# Create your views here.


def index(request):
    enemy = Enemy.objects.all()[random.randint(0, 1)]
    player = Character.objects.get(pk=1)
    outcome = 'victory' if enemy.health // (player.damage - enemy.defence) <= player.max_hp // (enemy.damage - player.defence) else 'lose'
    data = {
        'enemy': {
            'name': enemy.name,
            'health': enemy.health,
            'damage': enemy.damage,
            'defence': enemy.defence,
            'exp_reward': enemy.exp_reward
        },
        'character': {
            'name': player.name,
            'health': player.max_hp,
            'damage': player.damage,
            'defence': player.defence,
            'exp_current': player.exp_current,
            'exp_next': player.exp_next
        },
        'next': f"{reverse('arena')}?outcome={outcome}&reward={enemy.exp_reward}",
    }
    if request.GET:
        data['outcome'] = request.GET['outcome']
        if request.GET['outcome'] == 'victory':
            player.exp_current += int(request.GET['reward'])
            if player.exp_current >= player.exp_next:
                player.level += 1
                player.attribute_points += 2
                player.exp_current -= player.exp_next
                player.exp_next += player.exp_next * 0.2
            player.save()
    return render(request, 'arena/index.html', data)


def battle_result(request):
    return redirect('arena')
