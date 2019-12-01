from django.shortcuts import render
import random
from .models import stocks, rooms, history, demandeFood, food
from .models import drinks as dk
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate,logout


def test_Serveur(user):
    for group in user.groups.all():
        if group.name == "Serveur Salle Aztèque":
            return True
        if group.name == "Serveur Salle Nordique":
            return True
        if group.name == "Serveur Salle Egypte":
            return True
        if group.name == "Serveur Salle Grèce":
            return True
        if group.name == "CDF":
            return True
    if user.is_staff:
        return True
    return False

def test_history(user):
    for group in user.groups.all():
        if group.name == "Serveur Salle Aztèque":
            return True
        if group.name == "Serveur Salle Nordique":
            return True
        if group.name == "Serveur Salle Egypte":
            return True
        if group.name == "Serveur Salle Grèce":
            return True
        if group.name == "Réserve Zibar":
            return True
        if group.name == "CDF":
            return True
    if user.is_staff:
        return True
    return False


def test_Zibar(user):
    for group in user.groups.all():
        if group.name == "Réserve Zibar":
            return True
        if group.name == "CDF":
            return True
    if user.is_staff:
        return True
    return False

def test_Restal(user):
    for group in user.groups.all():
        if group.name == "Restal":
            return True
        if group.name == "CDF":
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
        st.set_accepter(False)
        value = drink.container_size
        st.refil(value,False)

    for drink in stocks.objects.all():
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
    sqrt = 0
    while sqrt in [0,102,13,119]:
        sqrt = random.randint(1,175)
    sqrt = str(sqrt)
    return render(request,'main/sqrt(Cdf).html',locals())

@login_required
@user_passes_test(test_Serveur, login_url='/Fdp')
def Client(request):
    user=request.user
    groupe=""
    for group in user.groups.all():
        if group.name == "Serveur Salle Aztèque":
            salle = "Aztèque"

        if group.name == "Serveur Salle Nordique":
            salle = "Nordique"

        if group.name == "Serveur Salle Grèce":
            salle = "Grèce"

        if group.name == "Serveur Salle Egypte":
            salle = "Egypte"

        if group.name == "CDF":
            groupe="CDF"

    if user.is_staff or groupe == "CDF":
        staff=True
        salle="Nordique"
        sallelist=["Egypte","Grèce","Aztèque","Nordique"]

        Newsalle=request.POST.get('Room')
        if Newsalle != None:
            salle=Newsalle

    bool = False
    drinks = []
    rang = {0,1,2,3,4,5,6,7,8,9}
    for drink in stocks.objects.all():
        if drink.room.name == salle:
            drinkName=drink.drinks.name
            drinks.append(drinkName)
            drinksoldout=[]
            if dk.objects.filter(name = drinkName)[0].is_soldout:
                drinksoldout.append(drinkName)
            qte = request.POST.get('qte,'+drink.drinks.name)
            accepter = request.POST.get('Accepter')
            if accepter != None and qte != None:
                bool = True
                qte, drinkName  = qte.split(",")
                drinkId = dk.objects.filter(name = drinkName)[0].id
                roomId = rooms.objects.filter(name = salle)[0].id
                if int(qte) != 0:
                    st=stocks.objects.filter(drinks = drinkId,room = roomId)[0]
                    st.drain(int(qte),True)
                    st.set_conso(int(qte))

    return render(request,'main/Client.html',locals())

@login_required
@user_passes_test(test_history, login_url='/Fdp')
def History(request):
    user=request.user
    groupe=""
    for group in user.groups.all():
        if group.name == "Serveur Salle Aztèque":
            roomuser = "Aztèque"

        if group.name == "Serveur Salle Nordique":
            roomuser = "Nordique"

        if group.name == "Serveur Salle Grèce":
            roomuser = "Grèce"

        if group.name == "Serveur Salle Egypte":
            roomuser = "Egypte"

        if group.name == "Réserve Zibar":
            roomuser = "Réserve Zibar"

        if group.name == "CDF":
            groupe="CDF"

    operation=[]

    if user.is_staff or groupe == "CDF":
        staff=True
        for event in history.objects.all():
            if event.is_sale:
                if event.is_cancelled:
                        operation.append((event.id,event.date, event.room, event.drink, event.quantity, 'Vente annulée'))
                else:
                        operation.append((event.id,event.date, event.room, event.drink, event.quantity,'Vente'))
            else:
                if event.is_cancelled:
                    operation.append((event.id,event.date, event.room, event.drink, event.quantity, 'Recharge annulée'))
                else:
                    operation.append((event.id,event.date, event.room, event.drink, event.quantity, 'Rechargée'))
        return render(request, 'main/History.html',locals())

    btnAnnuler = request.POST.get('Annuler')
    if btnAnnuler != None:
        ID=btnAnnuler
        Commande=history.objects.filter(id=ID)[0]
        Commande.set_cancelled(True)
        drinkName,roomName,quantitynb=Commande.drink,Commande.room,Commande.quantity
        drinkId = dk.objects.filter(name = drinkName)[0].id
        roomId = rooms.objects.filter(name = roomName)[0].id
        stocks.objects.filter(drinks = drinkId,room = roomId)[0].refilClient(int(quantitynb))
        stocks.objects.filter(drinks = drinkId,room = roomId)[0].cancel_conso(int(quantitynb))

    btnAnnulerZibar = request.POST.get('AnnulerZibar')
    if btnAnnulerZibar != None:
        ID=btnAnnulerZibar
        Recharge=history.objects.filter(id=ID)[0]
        Recharge.set_cancelled(True)
        drinkName,roomName,quantitynb=Recharge.drink,Recharge.room,Recharge.quantity
        drinkId = dk.objects.filter(name = drinkName)[0].id
        roomId = rooms.objects.filter(name = roomName)[0].id
        stocks.objects.filter(drinks = drinkId,room = roomId)[0].drainZibar(int(quantitynb))

    for event in history.objects.all():
        if event.is_sale:
            if str(event.room) == roomuser:
                if event.is_cancelled:
                    operation.append((event.id,event.date, event.room, event.drink, event.quantity, 'Vente annulée'))
                else:
                    operation.append((event.id,event.date, event.room, event.drink, event.quantity,'Vente'))
        elif roomuser =="Réserve Zibar":
            if event.is_cancelled:
                operation.append((event.id,event.date, event.room, event.drink, event.quantity, 'Recharge annulée'))
            else:
                operation.append((event.id,event.date, event.room, event.drink, event.quantity, 'Rechargée'))

    operation=operation[:30]
    return render(request, 'main/History.html',locals())

@login_required
@user_passes_test(test_Zibar, login_url='/Fdp')
def Soldout(request):
    Drinks=dk.objects.filter(is_soldout=True)
    btnAnnuler = request.POST.get('Annuler')
    if btnAnnuler != None:
        dk.objects.filter(name=btnAnnuler)[0].set_soldout(False)
    return render(request,'main/soldout.html',locals( ))


@login_required
@user_passes_test(test_Restal, login_url='/Fdp')
def Restal(request):
    demande = []
    preparation = []
    livraison = []

    btnAnnuler = request.POST.get('Annuler')
    if btnAnnuler != None:
        foodname, roomName = btnAnnuler.split(',')
        demandeFood.objects.filter(food__name = foodname,room__name = roomName)[0].delete()

    btnAccepter = request.POST.get('Accepter')
    if btnAccepter != None:

        foodname, roomName = btnAccepter.split(',')
        demandeFood.objects.filter(food__name = foodname,room__name = roomName)[0].set_preparation(True)

    btnTerminer = request.POST.get('Terminer')
    if btnTerminer != None:
        foodname, roomName = btnTerminer.split(',')
        demandeFood.objects.filter(food__name = foodname,room__name = roomName)[0].set_livraison(True)

    btnLivré = request.POST.get('Livré')
    if btnLivré != None:
        foodname, roomName = btnLivré.split(',')
        df = demandeFood.objects.filter(food__name = foodname,room__name = roomName)[0]
        df.set_preparation(False)
        df.set_livraison(False)
        df.set_livre(True)

    for food in demandeFood.objects.all():
        print(food.is_en_preparation  and not(food.is_en_livraison) and not(food.is_livre))
        if food.is_en_preparation  and not(food.is_en_livraison) and not(food.is_livre):
            print(food.food.name)
            preparation.append((food.room.name,food.food.name))
        elif food.is_en_livraison and not(food.is_livre):
            livraison.append((food.room.name,food.food.name))
        elif not(food.is_livre):
            demande.append((food.room.name,food.food.name))

    return render(request, 'main/Restal.html', locals())

@login_required
@user_passes_test(test_Restal, login_url='/Fdp')
def HistoryRestal(request):

    operation=[]

    btnAnnuler = request.POST.get('Annuler')
    if btnAnnuler != None:
        ID=btnAnnuler
        Commande=demandeFood.objects.filter(id=ID)[0]
        Commande.set_livre(False)
        Commande.set_preparation(True)
        Commande.set_livraison(True)

    for event in demandeFood.objects.all():
        if event.is_livre:
            operation.append((event.id,event.date, event.room, event.food))

    operation=operation[:30]
    return render(request, 'main/HistoryRestal.html',locals())
