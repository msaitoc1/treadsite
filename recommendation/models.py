from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Metric(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

class CoffeeShop(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

class User(models.Model):  
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)

class CoffeeShopFeatureRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coffee_shop = models.ForeignKey(CoffeeShop, on_delete=models.CASCADE)
    metric = models.ForeignKey(Metric, on_delete=models.CASCADE)
    rating = models.IntegerField(
        default=0,  # Default to 0 for "not rated"
        validators=[
            MinValueValidator(1),  # Minimum value is 1
            MaxValueValidator(4),  # Maximum value is 4
        ]
    )

    class Meta:
        unique_together = ('user', 'coffee_shop', 'metric')  # Prevent duplicate rows