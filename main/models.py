from django.db import models
from django.utils import timezone

# La BDD est encore la même que celle de l'année dernière donc on peut la changer si c'est nécessaire

class food(models.Model):
    name = models.CharField(max_length = 100)

    class Meta:
        verbose_name = "food"
        ordering = ['name']

    def __str__(self):
        return self.name

class drinks(models.Model):
    name = models.CharField(max_length = 50)
    container_size = models.IntegerField()
    threshold = models.IntegerField()
    by_bottle = models.BooleanField()
    is_champagne = models.BooleanField()
    is_soldout = models.BooleanField(default=False)

    class Meta:
        verbose_name = "drinks"
        ordering = ['name']

    def __str__(self):
        return self.name

    def set_soldout(self,bool):
        self.is_soldout = bool
        self.save()
        return None


class rooms(models.Model):
    name = models.CharField(max_length = 30)
    is_bar = models.BooleanField()
    drinks = models.ManyToManyField(drinks, through = 'stocks')

    class Meta:
        verbose_name = "rooms"
        ordering = ['name']

    def __str__(self):
        return self.name

class stocks(models.Model):
    drinks = models.ForeignKey(drinks, on_delete = models.CASCADE)
    room = models.ForeignKey(rooms, on_delete = models.CASCADE)
    quantity = models.IntegerField()
    consommation = models.IntegerField()
    is_accepter  = models.BooleanField(default = False)

    class Meta:
        verbose_name = "stocks"
        ordering = ['room','drinks']

    def __str__(self):
        return str(self.room)+' '+str(self.drinks)

    def set_accepter(self,bool):
        self.is_accepter = bool
        self.save()
        return None


    def refil(self,value):
        self.quantity += value
        self.save()
        return None

class history(models.Model):
    drink = models.CharField(max_length = 50)
    room = models.CharField(max_length = 30)
    date = models.DateTimeField(default=timezone.now)
    quantity = models.IntegerField()
    is_sale = models.BooleanField()
    is_cancelled = models.BooleanField()

    class Meta:
        verbose_name = "history"
        ordering = ['room','drink']

    def __str__(self):
        return str(self.room)+' '+str(self.drink)


### Permission ###
from django.contrib.auth.models import Permission,Group,User
# from django.contrib.auth import get_user_model
# User = get_user_model()
from django.contrib.contenttypes.models import ContentType
import os

class Permission_serveur_salle_1(Permission):
    name = 'Permission serveur salle 1'
    code = 'Permission_serveur_salle_1'

class Serveur_salle_1(models.Model):
    bucque = models.CharField(max_length = 30)
    fams = models.IntegerField()
    proms = models.IntegerField(default = 218)
    is_Zi = models.BooleanField(default = False)

    class Meta:
        permissions = [('can_use_salle_1','Can use salle 1')]
        verbose_name = "Serveur de la Salle 1"
        ordering = ['fams','proms']


# print(User.objects.filter( groups__name='Serveur salle 1').exists())


#     def get_DATA():
#         cwd = os.getcwd()
#         with open(cwd + "\\main\\serveur_salle_1.csv") as file:
#             data = file.readlines()
#             for line in data:
#                 print(line)
#                 linesplit = line.split(';')
#                 if len(linesplit) == 2:
#                     bucque = linesplit[0]
#                     fams = linesplit[1]
#                     Serveur_salle_1(bucque = bucque, fams = fams)
#
# Serveur_salle_1.get_DATA()
