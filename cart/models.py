from django.db import models
from userauths.models import User
from django.utils.html import mark_safe


class Cart(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_id = models.CharField(max_length=100, null=True, blank=True)
    product_title = models.CharField(max_length=100, null=True, blank=True)
    product_quantity = models.IntegerField()
    product_price = models.FloatField()
    product_category = models.CharField(max_length=100, null=True, blank=True)
    product_subtotal = models.FloatField(null=True, blank=True)
    product_image = models.CharField(max_length=100, null=True, blank=True, default='product.jpg')

    def __str__(self):
        return self.product_title

    def image(self):
        return mark_safe('<img src="{}" width="50" />'.format(self.product_image))
