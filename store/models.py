from django.db import models
from django.core.validators import MinValueValidator


class Collection(models.Model):
    title = models.CharField(max_length=50, unique=True)


class Product(models.Model):
    title = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    inventory = models.PositiveIntegerField()
    last_update = models.DateField(auto_now=True)
    unit_price = models.DecimalField(
        max_digits=6, decimal_places=2, validators=[MinValueValidator(0.1)])
    collection = models.ForeignKey(
        Collection, on_delete=models.PROTECT, related_name='products')
