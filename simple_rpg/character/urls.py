from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="character_profile"),
    path('increase_stat/', views.increase_stats, name="increase_stat")
]
