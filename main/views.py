from django.shortcuts import render
import random
from .models import stocks, rooms, history, demandeFood, food
from .models import drinks as dk
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate,logout
import numpy as np

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

def test_soldout(user):
    for group in user.groups.all():
        if group.name in ["Serveur Salle Aztèque","Serveur Salle Nordique","Serveur Salle Grèce","Serveur Salle Egypte"]:
            return True
        if group.name =="Réserve Zibar":
            return True
        if group.name == "CDF":
            return True
    if user.is_staff :
        return True
    return False

def logoutView(request):
    logout(request)
    return render(request,'main/logoutSuccess.html',locals())

def logoutSuccess(request):
    return render(request,'main/logoutSuccess.html',locals())

@login_required(redirect_field_name='', login_url='/logout')
def Fdp(request):
    user=request.user
    for group in user.groups.all():
        if group.name in ["Serveur Salle Aztèque","Serveur Salle Nordique","Serveur Salle Grèce","Serveur Salle Egypte"]:
            serveur=True
        if group.name == "Restal":
            restal=True
        if group.name =="Réserve Zibar":
            zibar=True
        if group.name == "CDF":
            CDF=True
    if user.is_staff:
        staff=True
    return render(request,'main/Fdp.html',locals())

@login_required(redirect_field_name='', login_url='/logout')
@user_passes_test(test_Zibar, login_url='/Fdp')
def Zibar(request):
    zibar=True
    user=request.user
    for group in user.groups.all():
        if group.name == "CDF":
            CDF=True
            zibar=False
    if user.is_staff:
        staff=True
        zibar=False
    demande = []
    livraison = []
    rang=np.linspace(1,100,100,dtype='uint32')

    btnAnnuler = request.POST.get('Annuler')
    if btnAnnuler != None:
        drinkName = btnAnnuler
        dk.objects.filter(name = drinkName)[0].set_soldout(True)

    btnAccepter = request.POST.get('Accepter')
    if btnAccepter != None:
        drinkName, roomName = btnAccepter.split(',')
        q=request.POST.get('Quantité '+drinkName+' '+roomName)
        stocks.objects.filter(drinks__name = drinkName,room__name = roomName)[0].set_accepter(True)
        drinkid=dk.objects.filter( name = drinkName )[0].id
        roomid=rooms.objects.filter(name = roomName)[0].id
        h = history(drink = dk.objects.filter(name = drinkName)[0], room = rooms.objects.filter(name = roomName)[0], is_sale = False, quantity = q)
        h.save()

    btnTerminer = request.POST.get('Terminer')
    if btnTerminer != None:
        drinkName, roomName = btnTerminer.split(',')
        st = stocks.objects.filter(drinks__name = drinkName,room__name = roomName)[0]
        drink = dk.objects.filter(name = drinkName)[0]
        qte=history.objects.filter(drink__name = drinkName, room__name = roomName, is_sale = False)[0].quantity
        value = drink.container_size*qte
        st.set_accepter(False)
        st.refilClient(value)

    for drink in stocks.objects.all():
        if drink.is_accepter :
            qte=history.objects.filter(drink__name = drink.drinks.name, room__name = drink.room.name, is_sale = False)[0].quantity
            value = dk.objects.filter(name = drink.drinks.name)[0].container_size*qte
            livraison.append((drink.room.name,drink.drinks.name,value))
        if drink.quantity < drink.drinks.threshold and not(drink.drinks.is_soldout) and not(drink.is_accepter):
            demande.append((drink.room.name,drink.drinks.name))
    return render(request, 'main/Zibar.html', locals())

@login_required(redirect_field_name='', login_url='/logout')
def Accueil(request):
    user=request.user
    for group in user.groups.all():
        if group.name in ["Serveur Salle Aztèque","Serveur Salle Nordique","Serveur Salle Grèce","Serveur Salle Egypte"]:
            serveur=True
        elif group.name == "Restal":
            restal=True
        elif group.name =="Réserve Zibar":
            zibar=True
        elif group.name == "CDF":
            CDF=True
    if user.is_staff:
        staff=True
    return render(request,'main/Accueil.html',locals())

@login_required(redirect_field_name='', login_url='/logout')
def sqrtcdf(request):
    user=request.user
    for group in user.groups.all():
        if group.name in ["Serveur Salle Aztèque","Serveur Salle Nordique","Serveur Salle Grèce","Serveur Salle Egypte"]:
            serveur=True
        elif group.name == "Restal":
            restal=True
        elif group.name =="Réserve Zibar":
            zibar=True
        elif group.name == "CDF":
            CDF=True
    if user.is_staff:
        staff=True
    Nums=[99,123,19,36,45,74,106,85,11,3,113,25,136,143,160,167,63,41,107,40,38,93,137,124,163,47,116,29,5,140,52,54,10,141,4,148,158,7,14,39,132,87,115,145,125,76,105,37,20,97,55,109,129,170,56,66,75,91,168,77,79,65,128,27,161,171,130,80,64,164,50,51,104,89,28,49,72,58,96,110,174,121,114,155,6,133,42,59,149,32,86,131,70,16,8,165,5,5,5,5,5,5,5,5,5,5,5,5,5,5,80,80,80,80,80,5,5,5,5,5,5,5,5,5,5,5,5,5,5,80,80,80,80,80,32,32,32,32,32,32,47,47,47,47,25,25,25,25,25,52,52,52,52,52,52,'117-172','48-159','95-157','100-118-147','35-90-110-158','22-61-67-111','15-18-101','5!-62','78-153','84-166','73-156','9-134','82-135','103-152','122-154','1-138','100-159','60-83','12-17','44-94','81g','4!-43-92','88-173','144-162','31-53','2-150','23-151','71-126','57-142','89-167','21-112','34-98','27-149','127-146','30-139','46-108','68bis','168bis','26#68']
    ind=random.randint(0,len(Nums)-1)
    sqrt = Nums[ind]
    return render(request,'main/sqrt(Cdf).html',locals())

@login_required(redirect_field_name='', login_url='/logout')
@user_passes_test(test_Serveur, login_url='/Fdp')
def Client(request):
    user=request.user
    serveur=True
    CDF=False
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
            CDF = True

    if user.is_staff or CDF:
        salle ="Nordique"

        serveur=False
        if user.is_staff:
            staff=True
            CDF =False

        sallelist=["Nordique","Egypte","Grèce","Aztèque"]

        Newsalle=request.POST.get('Room')
        if Newsalle != None:
            salle=Newsalle

    bool = False
    drinks = []
    rang = {0,1,2,3,4,5,6,7,8,9}
    drinksoldout=[]
    for drink in stocks.objects.all():
        if drink.room.name == salle:
            drinkName=drink.drinks.name
            drinks.append(drinkName)
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

    fd = []
    for degeul in food.objects.all():
        if salle == "Grèce":
            foodname=degeul.name
            fd.append(foodname)
            foodsoldout=[]
            if food.objects.filter(name = foodname)[0].is_soldout:
                foodsoldout.append(foodname)
            qte = request.POST.get('qtef,'+degeul.name)
            accepter = request.POST.get('Accepterf')
            if accepter != None and qte != None:
                bool = True
                qte, foodname  = qte.split(",")
                degeulname = food.objects.filter(name = foodname)[0]
                room = rooms.objects.filter(name = salle)[0]
                if int(qte) != 0:
                    for i in range(int(qte)):
                        demandeFood.save(demandeFood(food = degeulname,room = room))
    return render(request,'main/Client.html',locals())

@login_required(redirect_field_name='', login_url='/logout')
@user_passes_test(test_history, login_url='/Fdp')
def History(request):
    user=request.user
    groupe=""
    for group in user.groups.all():
        if group.name == "Serveur Salle Aztèque":
            roomuser = "Aztèque"
            serveur=True

        if group.name == "Serveur Salle Nordique":
            roomuser = "Nordique"
            serveur=True

        if group.name == "Serveur Salle Grèce":
            roomuser = "Grèce"
            serveur=True

        if group.name == "Serveur Salle Egypte":
            roomuser = "Egypte"
            serveur=True

        if group.name == "Réserve Zibar":
            roomuser = "Réserve Zibar"
            zibar=True

        if group.name == "CDF":
            groupe="CDF"
            CDF=True

    operation=[]

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
        st=stocks.objects.filter(drinks = drinkId,room = roomId)[0]
        st.drainZibar(int(quantitynb))
        st.set_accepter(False)

    if user.is_staff or groupe == "CDF":
        if user.is_staff:
            staff=True
            CDF=False
        for event in history.objects.all():
            if event.is_sale:
                if event.is_cancelled:
                        operation.append((event.id,event.date.strftime("%H:%M:%S"), event.room, event.drink, event.quantity, 'Vente annulée'))
                else:
                        operation.append((event.id,event.date.strftime("%H:%M:%S"), event.room, event.drink, event.quantity,'Vente'))
            else:
                if event.is_cancelled:
                    operation.append((event.id,event.date.strftime("%H:%M:%S"), event.room, event.drink, event.quantity, 'Recharge annulée'))
                else:
                    operation.append((event.id,event.date.strftime("%H:%M:%S"), event.room, event.drink, event.quantity, 'Rechargée'))
        return render(request, 'main/History.html',locals())

    for event in history.objects.all():
        if event.is_sale:
            if str(event.room) == roomuser:
                if event.is_cancelled:
                    operation.append((event.id,event.date.strftime("%H:%M:%S"), event.room, event.drink, event.quantity, 'Vente annulée'))
                else:
                    operation.append((event.id,event.date.strftime("%H:%M:%S"), event.room, event.drink, event.quantity,'Vente'))
        elif roomuser =="Réserve Zibar":
            if event.is_cancelled:
                operation.append((event.id,event.date.strftime("%H:%M:%S"), event.room, event.drink, event.quantity, 'Recharge annulée'))
            else:
                operation.append((event.id,event.date.strftime("%H:%M:%S"), event.room, event.drink, event.quantity, 'Rechargée'))

    operation=operation[:30]
    return render(request, 'main/History.html',locals())

@login_required(redirect_field_name='', login_url='/logout')
@user_passes_test(test_soldout, login_url='/Fdp')
def Soldout(request):
    user=request.user
    groupe=""
    for group in user.groups.all():
        if group.name == "Serveur Salle Aztèque":
            roomuser = "Aztèque"
            serveur=True

        if group.name == "Serveur Salle Nordique":
            roomuser = "Nordique"
            serveur=True

        if group.name == "Serveur Salle Grèce":
            roomuser = "Grèce"
            serveur=True

        if group.name == "Serveur Salle Egypte":
            roomuser = "Egypte"
            serveur=True

        if group.name == "Réserve Zibar":
            roomuser = "Réserve Zibar"
            zibar=True

        if group.name == "CDF":
            CDF=True

    if user.is_staff:
        staff=True
    Drinks=dk.objects.filter(is_soldout=True)
    btnAnnuler = request.POST.get('Annuler')
    zibar1=test_Zibar(request.user)
    if btnAnnuler != None:
        dk.objects.filter(name=btnAnnuler)[0].set_soldout(False)
    return render(request,'main/soldout.html',locals( ))


@login_required(redirect_field_name='', login_url='/logout')
@user_passes_test(test_Restal, login_url='/Fdp')
def Restal(request):
    user=request.user
    restal=True
    for group in user.groups.all():
        if group.name == "CDF":
            CDF=True
            restal=False
    if user.is_staff:
        staff=True
        restal=False

    demande = []
    preparation = []
    livraison = []

    btnAnnuler = request.POST.get('Annuler')
    if btnAnnuler != None:
        foodname, roomName = btnAnnuler.split(',')
        demandeFood.objects.filter(food__name = foodname,room__name = roomName).delete()
        food.objects.filter(name = foodname)[0].set_soldout(True)

    btnAccepter = request.POST.get('Accepter')
    if btnAccepter != None:
        foodname, roomName = btnAccepter.split(',')
        listfood = demandeFood.objects.filter(food__name = foodname,room__name = roomName)
        l = len(listfood)
        i = 0
        while True:
            if l < i:
                break
            if not(listfood[i].is_en_preparation):
                listfood[i].set_preparation(True)
                break
            i += 1

    btnTerminer = request.POST.get('Terminer')
    if btnTerminer != None:
        foodname, roomName = btnTerminer.split(',')
        listfood = demandeFood.objects.filter(food__name = foodname,room__name = roomName)
        l = len(listfood)
        i = 0
        while True:
            if l < i:
                break
            if not(listfood[i].is_en_livraison):
                listfood[i].set_livraison(True)
                break
            i += 1

    btnLivré = request.POST.get('Livré')
    if btnLivré != None:
        foodname, roomName = btnLivré.split(',')
        listfood = demandeFood.objects.filter(food__name = foodname,room__name = roomName)
        l = len(listfood)
        i = 0
        while True:
            if l < i:
                break
            if not(listfood[i].is_livre):
                listfood[i].set_preparation(False)
                listfood[i].set_livraison(False)
                listfood[i].set_livre(True)
                break
            i += 1

    for foods in demandeFood.objects.all():
        if foods.is_en_preparation  and not(foods.is_en_livraison) and not(foods.is_livre):
            preparation.append((foods.room.name,foods.food.name))
        elif foods.is_en_livraison and not(foods.is_livre):
            livraison.append((foods.room.name,foods.food.name))
        elif not(foods.is_livre):
            demande.append((foods.room.name,foods.food.name))

    return render(request, 'main/Restal.html', locals())

@login_required(redirect_field_name='', login_url='/logout')
@user_passes_test(test_Restal, login_url='/Fdp')
def HistoryRestal(request):
    user=request.user
    restal=True
    for group in user.groups.all():
        if group.name == "CDF":
            CDF=True
            restal=False
    if user.is_staff:
        staff=True
        restal=False

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

@login_required(redirect_field_name='', login_url='/logout')
@user_passes_test(test_Restal, login_url='/Fdp')
def SoldoutFood(request):
    restal=True
    user=request.user
    for group in user.groups.all():
        if group.name == "CDF":
            CDF=True
            restal=False
    if user.is_staff:
        staff=True
        restal=False
    foodsold=food.objects.filter(is_soldout=True)
    btnAnnuler = request.POST.get('Annuler')
    Cuist=test_Restal(request.user)
    if btnAnnuler != None:
        food.objects.filter(name=btnAnnuler)[0].set_soldout(False)
    return render(request,'main/soldoutFood.html',locals( ))
