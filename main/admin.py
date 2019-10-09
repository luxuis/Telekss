from django.contrib import admin
from .models import drinks,rooms,history,stocks,food

class stocksAdmin(admin.ModelAdmin):
    list_display   = ('drink', 'room', 'quantity',)
    list_filter    = ('room', 'drink',)
    ordering       = ('room', 'drink',)

class historyAdmin(admin.ModelAdmin):
    list_display   = ('drink', 'room', 'quantity',)
    list_filter    = ('room', 'drink',)
    date_hierarchy = 'date'
    ordering       = ('date',)

class drinksAdmin(admin.ModelAdmin):
    list_display   = ('name', 'container_size', 'threshold','by_bottle','is_champagne',)
    list_filter    = ('name','is_champagne',)
    ordering       = ('name',)

class roomsAdmin(admin.ModelAdmin):
    list_display   = ('name', 'is_bar',)
    list_filter    = ('name','is_bar',)
    ordering       = ('name',)

class foodAdmin(admin.ModelAdmin):
    list_display   = ('name',)
    ordering       = ('name',)

admin.site.register(drinks, drinksAdmin)
admin.site.register(rooms, roomsAdmin)
admin.site.register(history, historyAdmin)
admin.site.register(stocks, stocksAdmin)
admin.site.register(food, foodAdmin)
