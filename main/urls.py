from django.urls import path
from . import views

urlpatterns = [
    path('Zibar', views.Zibar),
    path('Client', views.Client),
    path('',views.Accueil),
    path('History',views.History)
]
