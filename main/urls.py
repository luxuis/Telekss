from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('Zibar', views.Zibar),
    path('Salle_1', views.Client_Salle_1),
    path('Accueil',views.Accueil),
    path('Fdp',views.Fdp),
    path('', auth_views.LoginView.as_view()),
    path('History',views.History),
    path('sqrt(Cdf)',views.sqrtcdf),
    path('logout',views.logoutView),
    path('logoutSuccess',views.logoutSuccess),
    path('soldout',views.Soldout),
    path('Restal',views.Restal),
    path('HistoryRestal',views.HistoryRestal)
]
