from django.shortcuts import render
from .models import Character


def index(request):
    charInfo = Character.objects.all()[0]
    data = {
        'name': 'Name',
        'gold': 0,
        'stats': [
            'Name', 'Gold', 'Health', 'Damage', 'Defence'
        ],
        'values': {
            'Name': charInfo.name,
            'Gold': 0,
            'Health': [charInfo.current_hp, charInfo.max_hp],
            'Damage': charInfo.damage,
            'Defence': charInfo.defence
        },
    }

    return render(request, 'character/index.html', context=data)
