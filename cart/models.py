from django.db import models
from userauths.models import User
from django.utils.html import mark_safe

from core.models import Product

class Cart(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    product_quantity = models.IntegerField()
    product_subtotal = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.product.title

    def image(self):
        return mark_safe('<img src="{}" width="50" />'.format(self.product.image.url))
