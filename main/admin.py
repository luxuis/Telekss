from django.contrib import admin
from .models import drinks,rooms,history,stocks,food

class stocksAdmin(admin.ModelAdmin):
    list_display   = ('drink', 'room', 'quantity')
    list_filter    = ('room', 'drink',)
    ordering       = ('room', 'drink',)


admin.site.register(drinks)
admin.site.register(rooms)
admin.site.register(history)
admin.site.register(stocks, stocksAdmin)
admin.site.register(food)
