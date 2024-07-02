from django.shortcuts import render, redirect
from django.urls import reverse

from .models import Character


def index(request):
    charInfo = Character.objects.all()[0]
    data = {
        'name': charInfo.name,
        'gold': 0,
        'values': {
            'Name': charInfo.name,
            'Gold': 0,
            'Health': [charInfo.current_hp, charInfo.max_hp],
            'Damage': charInfo.damage,
            'Defence': charInfo.defence,
            'Attribute Points': charInfo.attribute_points
        },
        'next': f"{reverse('increase_stat')}"
    }
    return render(request, 'character/index.html', context=data)


def increase_stats(request):
    # TODO: replace with manager (character)
    charInfo = Character.objects.all()[0]
    if request.GET:
        if charInfo.attribute_points > 0:
            if request.GET['attribute'] == "health":
                charInfo.max_hp += 20
                charInfo.attribute_points -= 1
            elif request.GET['attribute'] == "damage":
                charInfo.damage += 1
                charInfo.attribute_points -= 1
            elif request.GET['attribute'] == "defence":
                charInfo.defence += 1
                charInfo.attribute_points -= 1
            charInfo.save()

    return redirect('character_profile')
