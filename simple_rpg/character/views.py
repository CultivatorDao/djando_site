from django.shortcuts import render


def index(request):
    data = {
        'name': 'Name',
        'gold': 0
    }
    return render(request, 'character/index.html', context=data)
