from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import coffeeShop, coffeeShopSearchDoc

@receiver(post_save, sender=coffeeShop)
def create_or_update_search_doc(sender, instance, created, **kwargs):
    if created:
        coffeeShopSearchDoc.objects.create(coffee_shop=instance)
        print(f"Created coffeeShopSearchDoc for {instance.name}")
    else:
        instance.SearchDoc.save()
        print(f"Updated coffeeShopSearchDoc for {instance.name}")