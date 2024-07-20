import random, json

from django.shortcuts import render, redirect
from django.urls import reverse

from managers.battle_manager import BattleManager
from managers.character_manager import CharacterManager

from .models import Enemy, StrongEnemy, ColosseumBattle
from character.models import Character

# Create your views here.


battle_manager = BattleManager()
character_manager = CharacterManager()


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
    player = Character.objects.get(pk=1)
    enemy = StrongEnemy.objects.get(pk=1)

    # Look if there is any battle with this character
    # In future character will have only 1 battle ongoing
    # If battle unfinished delete all information about this battle and create new
    if player.battles.all():
        battle = player.battles.all()[0]
    else:
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

    data = battle_manager.colosseum_fight_calculate(battle)

    return render(request, 'arena/colosseum.html', data)


def colosseum_battle(request):
    pass


def colosseum_battle_result(request):
    pass
