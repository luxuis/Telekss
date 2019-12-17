from django.contrib import admin
from .models import drinks,rooms,history,stocks

class stocksAdmin(admin.ModelAdmin):
    list_display   = ('drinks', 'room', 'quantity','is_accepter')
    list_filter    = ('room', 'drinks',)
    ordering       = ('room', 'drinks',)

class historyAdmin(admin.ModelAdmin):
    list_display   = ('drink', 'room', 'quantity','date','is_sale','is_cancelled')
    list_filter    = ('room', 'drink',)
    date_hierarchy = 'date'
    ordering       = ('date',)

class drinksAdmin(admin.ModelAdmin):
    list_display   = ('name', 'container_size', 'threshold','by_bottle','is_champagne','is_soldout')
    list_filter    = ('name','is_champagne',)
    ordering       = ('name',)

class roomsAdmin(admin.ModelAdmin):
    list_display   = ('name', 'is_bar',)
    list_filter    = ('name','is_bar',)
    ordering       = ('name',)



admin.site.register(drinks, drinksAdmin)
admin.site.register(rooms, roomsAdmin)
admin.site.register(history, historyAdmin)
admin.site.register(stocks, stocksAdmin)
