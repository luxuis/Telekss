from django.shortcuts import render
from .models import stocks
from .models import drinks as dk
from django.contrib.auth.models import User



def Zibar(request):
    demande = []
    livraison = []

    btnAnnuler = request.POST.get('Annuler')
    if btnAnnuler != None:
        drinkName = btnAnnuler
        dk.objects.filter(name = drinkName)[0].set_soldout(True)

    btnAccepter = request.POST.get('Accepter')
    if btnAccepter != None:
        drinkName, roomName = btnAccepter.split(',')
        stocks.objects.filter(drinks__name = drinkName,room__name = roomName)[0].set_accepter(True)

    btnTerminer = request.POST.get('Terminer')
    if btnTerminer != None:
        drinkName, roomName = btnTerminer.split(',')
        st = stocks.objects.filter(drinks__name = drinkName,room__name = roomName)[0]
        drink = dk.objects.filter(name = drinkName)[0]
        st.set_accepter(False)
        value = drink.container_size
        st.refil(value)


    for drink in stocks.objects.all():
        if drink.is_accepter:
            livraison.append((drink.room.name,drink.drinks.name))
        if drink.quantity < drink.drinks.threshold and not(drink.drinks.is_soldout) and not(drink.is_accepter):
            demande.append((drink.room.name,drink.drinks.name))

    return render(request, 'main/Zibar.html', locals())

def Accueil(request):

    return render(request,'main/Accueil.html',locals())

def test_salle(user):

    return True

from django.contrib.auth.decorators import login_required, user_passes_test
@login_required
@user_passes_test(test_salle)
def Client(request):
    user = request.user
    print(user.groups)
    drinks = []
    rang = {0,1,2,3,4,5,6,7,8,9}
    for drink in stocks.objects.all():
        if drink.room.name == "Salle_1":
            drinks.append(drink.drinks.name)
    return render(request,'main/Client.html',locals())
