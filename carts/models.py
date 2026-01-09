from django.db import models
from django.conf import settings   # ✅ THIS WAS MISSING
from store.models import Product, Variation


class Cart(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    is_ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.cart_id


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation = models.ManyToManyField(Variation, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        return self.product.price * self.quantity

    def __unicide__(self):   # ✅ Python 3
        return str(self.product)
