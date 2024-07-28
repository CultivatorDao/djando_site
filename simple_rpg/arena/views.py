import json
import random

from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseNotFound

from .models import Enemy, StrongEnemy, ColosseumBattle
from character.models import Character
from managers.battle_manager import BattleManager
from managers.character_manager import CharacterManager
from shared.base64_converter import Base64Converter


battle_manager = BattleManager()
character_manager = CharacterManager()
converter = Base64Converter()


# Buffer view that contains links to various battle views
def index(request):
    data = {
        "menu": {
            "Infinite Grinding": reverse("infinite_grinding"),
            "Colosseum": reverse("colosseum")
        }
    }
    return render(request, 'arena/index.html', data)


def infinite_grinding(request):
    enemy = Enemy.objects.all()[random.randint(0, 1)]
    player = Character.objects.get(pk=1)
    battle_manager.next = reverse('result')
    data = battle_manager.arena_fight_calculate(player=player, enemy=enemy)

    return render(request, 'arena/infinite_grinding.html', data)


def infinite_grinding_result(request):
    player = Character.objects.get(pk=1)
    if request.GET:
        if request.GET['outcome'] == 'victory':
            character_manager.get_reward(player, int(request.GET['reward']), 'exp')
    return redirect('infinite_grinding')


def colosseum(request):
    enemies = StrongEnemy.objects.all()

    data = {}

    for enemy in enemies:
        data[enemy.name] = battle_manager.get_info(
            options={
                'except': ["_state", "name"]
            },
            enemy=enemy
        )['enemy']
        data[enemy.name]['next'] = f"prepare?id={data[enemy.name]['id']}"

    return render(
        request,
        'arena/colosseum.html',
        {
            'enemies': data,
        }
    )


def colosseum_battle(request, state):
    player = Character.objects.get(pk=1)

    match state:
        case 'prepare':

            if request.GET:
                enemy = StrongEnemy.objects.get(pk=request.GET['id'])
            else:
                enemy = StrongEnemy.objects.get(pk=1)

            battle = ColosseumBattle(
                player=player,
                enemy_data=json.dumps(battle_manager.get_info(
                    options={
                        'except': ['_state', 'id']
                    },
                    enemy=enemy
                )['enemy'])
            )
            battle.save()

            return redirect(reverse('colosseum_battle', args=["battle"]))

        case 'battle':
            battle = player.battles.all()[0]

            data = battle_manager.colosseum_fight_calculate(battle, request.GET)

            if battle.is_finished:
                return redirect(reverse('colosseum_battle', args=["result"]))
            return render(request, 'arena/colosseum_battle.html', data)

        case 'result':
            battle = player.battles.all()[0]

            if battle.is_won:
                character_manager.get_reward(player, reward=battle.enemy["exp_reward"], reward_type='exp')

            data = {
                "enemy": battle.enemy,
                "result": battle.is_won,
                "return": reverse('colosseum')
            }

            # Restores player's hp to max. Delete in future
            # after adding methods to heal player.
            player.current_hp = player.max_hp
            player.save()
            battle.delete()

            return render(request, 'arena/colosseum_battle_result.html', data)

        case _:
            return HttpResponseNotFound(request)
