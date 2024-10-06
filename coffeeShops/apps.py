from django.apps import AppConfig

class CoffeeShopsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'


    name = 'coffeeShops'
    def ready(self):
        import coffeeShops.signals