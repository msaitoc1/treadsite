from django.contrib import admin
from .models import coffeeShop, Event, stat
# Register your models here.
admin.site.register(coffeeShop)
admin.site.register(Event)
admin.site.register(stat)