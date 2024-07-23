from django.db import models
from userauths.models import User
from django.utils.html import mark_safe
# Create your models here.

STATUS_CHOICE = (
    ("processing", 'Processing'),
    ("shipped", 'Shipped'),
    ("delivered", 'Delivered'),
)

class Payment(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100)
    amount_paid = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.payment_id


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    invoice_number = models.CharField(max_length=200)

    price = models.DecimalField(
        max_digits=99999999,
        decimal_places=2,
        default='0.99')

    paid_status = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)

    product_status = models.CharField(
        choices=STATUS_CHOICE,
        default='processing',
        max_length=30)

    payement = models.ForeignKey(
        Payment,
        on_delete=models.SET_NULL,
        blank=True,
        null=True)

    class Meta:
        verbose_name_plural = 'Orders'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_status = models.CharField(max_length=200)
    quantity = models.IntegerField(default=0)
    item = models.CharField(max_length=200)
    image = models.CharField(max_length=200)

    price = models.DecimalField(max_digits=99999999, decimal_places=2, default='0.99') # noqa
    total = models.DecimalField(max_digits=99999999, decimal_places=2, default='0.99') # noqa

    class Meta:
        verbose_name_plural = 'Order Items'

    def item_image(self):
        return mark_safe('<img src="{}" width="50" />'.format(self.image)) # noqa
    
    def __str__(self):
        return self.order.user.username
