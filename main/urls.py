from django.urls import path
from . import views

urlpatterns = [
    path('Zibar', views.Zibar),
    path('',views.Accueil)
]
