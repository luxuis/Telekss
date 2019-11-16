from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('Zibar', views.Zibar),
    path('Client', views.Client),
    path('Accueil',views.Accueil),
    path('Fdp',views.Fdp),
    path('', auth_views.LoginView.as_view()),
]
