from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='arena'),
    path('infinite_grinding', views.infinite_grinding, name='infinite_grinding'),
    path('result/', views.infinite_grinding_result, name='result'),
    path('colosseum/', views.colosseum, name='colosseum'),
    path('colosseum/<slug:state>', views.colosseum_battle, name='colosseum_battle')
]
