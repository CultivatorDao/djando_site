from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='arena'),
    path('result/', views.battle_result, name='result')
]
