from django.db import models
from userauths.models import User
from core.models import Product
from django.utils.html import mark_safe
from datetime import datetime


class WishList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Wish Lists'

    def __str__(self):
        return str(self.product.title)

    def image(self):
        return mark_safe('<img src="{}" width="50" />'.format(self.product.image.url))
