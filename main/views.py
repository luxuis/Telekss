from django.shortcuts import render
import random
from .models import stocks, rooms, history
from .models import drinks as dk
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate,logout


def test_salle_1(user):
    for group in user.groups.all():
        if group.name == "Serveur salle 1":
            return True
    if user.is_staff:
        return True
    return False

def test_Zibar(user):
    for group in user.groups.all():
        if group.name == "Zibar":
            return True
    if user.is_staff:
        return True
    return False

def logoutView(request):
    logout(request)
    return render(request,'main/logoutSuccess.html',locals())

def logoutSuccess(request):
    return render(request,'main/logoutSuccess.html',locals())

@login_required
def Fdp(request):
    return render(request,'main/Fdp.html',locals())

@login_required
@user_passes_test(test_Zibar, login_url='/Fdp')
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
        print(drink.container_size)
        st.set_accepter(False)
        value = drink.container_size
        st.refil(value,False)


    for drink in stocks.objects.all():
        print(drink)
        if drink.is_accepter:
            livraison.append((drink.room.name,drink.drinks.name))
        if drink.quantity < drink.drinks.threshold and not(drink.drinks.is_soldout) and not(drink.is_accepter):
            demande.append((drink.room.name,drink.drinks.name))

    return render(request, 'main/Zibar.html', locals())

@login_required
def Accueil(request):
    return render(request,'main/Accueil.html',locals())

@login_required
def sqrtcdf(request):
    sqrt = 102
    while sqrt == 102:  
        sqrt = random.randint(1,175)
    sqrt = str(sqrt)
    return render(request,'main/sqrt(Cdf).html',locals())

@login_required
@user_passes_test(test_salle_1, login_url='/Fdp')
def Client_Salle_1(request):
    salle = "Salle 1"
    salleView = Client_Salle_1
    user = request.user
    drinks = []
    rang = {0,1,2,3,4,5,6,7,8,9}
    for drink in stocks.objects.all():
        if drink.room.name == "Salle_1":
            drinks.append(drink.drinks.name)

        qte = request.POST.get('qte,'+drink.drinks.name)
        accepter = request.POST.get('Accepter')
        if accepter != None and qte != None:
            qte, drinkName  = qte.split(",")
            drinkId = dk.objects.filter(name = drinkName)[0].id
            roomId = rooms.objects.filter(name = "Salle_1")[0].id

            if int(qte) != 0:
                stocks.objects.filter(drinks = drinkId,room = roomId)[0].drain(int(qte),True)
    return render(request,'main/Client.html',locals())

def History(request):
    operation=[]

    btnAnnuler = request.POST.get('Annuler')
    if btnAnnuler != None:
        drinkName, roomName ,quantitynb= btnAnnuler.split(',')
        history.objects.filter(drink__name = drinkName,room__name = roomName,quantity =int(quantitynb))[0].set_cancelled(True)
        history.objects.filter(drink__name = drinkName,room__name = roomName,quantity =int(quantitynb))[0].set_saled(False)
        stocks.objects.filter(drinks__name = drinkName,room__name = roomName)[0].refil2(int(quantitynb))
    for event in history.objects.all():
        if event.is_cancelled:
            operation.append(((event.date, event.room, event.drink, event.quantity, 'Vente annulée')))
        elif event.is_sale:
            operation.append(((event.date, event.room, event.drink, event.quantity,'Vente')))
        else:
            operation.append(((event.date, event.room, event.drink, event.quantity, 'Rechargée')))

    return render(request, 'main/History.html',locals())
