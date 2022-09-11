from django.db import models
from django.core.validators import MinValueValidator
from uuid import uuid4


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


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    created_at = models.DateField(auto_now_add=True)


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)])
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name='items')

    class Meta:
        unique_together = [['cart', 'product']]
