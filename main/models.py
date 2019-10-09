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
    by_bottle = models.IntegerField()
    is_champagne = models.BooleanField()

    class Meta:
        verbose_name = "drinks"
        ordering = ['name']

    def __str__(self):
        return self.name

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
    drink = models.ForeignKey(drinks, on_delete = models.CASCADE)
    room = models.ForeignKey(rooms, on_delete = models.CASCADE)
    quantity = models.IntegerField()
    consommation = models.IntegerField()

    class Meta:
        verbose_name = "rooms"
        ordering = ['room','drink']

    def __str__(self):
        return str(self.room)+str(self.drink)

class history(models.Model):
    drink = models.CharField(max_length = 50)
    room = models.CharField(max_length = 30)
    date = models.DateTimeField(default=timezone.now)
    quantity = models.IntegerField()
    is_sale = models.BooleanField()
    is_cancelled = models.BooleanField()
