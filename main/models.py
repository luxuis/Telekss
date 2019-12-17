from django.db import models
from django.utils import timezone


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

    def drain(self,value,is_sale):
        self.quantity -= value
        self.save()
        h = history(drink = self.drinks,room = self.room, quantity = value, is_sale = is_sale)
        h.save()
        return None

    def set_conso(self,value):
        self.consommation += value
        self.save()
        return None

    def cancel_conso(self,value):
        self.consommation -= value
        self.save()
        return None

    def drainZibar(self,value):   #pour annulation recharge
        self.quantity -= value
        self.save()
        return None

    def refilClient(self,value):  #pour annulation vente
        self.quantity += value
        self.save()
        return None

class history(models.Model):
    drink = models.ForeignKey(drinks, on_delete = models.CASCADE)
    room = models.ForeignKey(rooms, on_delete = models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    quantity = models.IntegerField(default = 0)
    is_sale = models.BooleanField()
    is_cancelled = models.BooleanField(default = False)

    class Meta:
        verbose_name = "history"
        ordering = ['-date']

    def __str__(self):
        if self.is_sale:
            return str(self.id)+' '+str(self.date)+' '+str(self.room)+' '+str(self.drink)+' '+str(self.quantity)+' '+'Vente'
        elif self.is_cancelled:
            return str(self.id)+' '+str(self.date)+' '+str(self.room)+' '+str(self.drink)+' '+str(self.quantity)+' '+'Vente ANNULEE'
        else:
            return str(self.id)+' '+str(self.date)+' '+str(self.room)+' '+str(self.drink)+' '+str(self.quantity)+' '+'Recharge'

    def set_saled(self,bool):
        self.is_sale = bool
        self.save()
        return None

    def set_cancelled(self,bool):
        self.is_cancelled = bool
        self.save()
        return None
