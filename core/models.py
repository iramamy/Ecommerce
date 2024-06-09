from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe

from userauths.models import User


STATUS_CHOICE = (
    ("process", 'Processing'),
    ("shipped", 'Shipped'),
    ("delivered", 'Delivered'),
)

STATUS= (
    ("draft", 'Draft'),
    ("disabled", 'Disabled'),
    ("rejected", 'Rejected'),
    ("in_review", 'In review'),
    ("published", 'Published'),
)

RATING= (
    (1, '★'),
    (2, '★★'),
    (3, '★★★'),
    (4, '★★★★'),
    (5, '★★★★★'),
)

def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class Category(models.Model):
    cid = ShortUUIDField(
        unique=True, 
        length=10, 
        max_length=30, 
        prefix='cat',
        alphabet='abcdefgh12345'
        )
    title = models.CharField(max_length=100, default='This is a category')
    image = models.ImageField(upload_to='category/', default='category.jpg')

    class Meta:
        verbose_name_plural = 'categories'

    def category_image(self):
        return mark_safe("<img src='%s' width='50'  height='50' />" % (self.image.url)) # noqa

    def __str__(self):
        return str(self.title)


class Tags(models.Model):
    pass


class Vendor(models.Model):
    vid = ShortUUIDField(
        unique=True, 
        length=10, 
        max_length=30, 
        prefix='ven',
        alphabet='abcdefgh12345'
        )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    title = models.CharField(max_length=100, default="Nestify")
    image = models.ImageField(upload_to=user_directory_path, default='vendor.jpg') # noqa
    cover_image = models.ImageField(upload_to=user_directory_path, default='vendor.jpg') # noqa
    description = models.TextField(null=True, blank=True, default='I am a vendor') # noqa

    address = models.CharField(max_length=100, default='123 Street Road')
    contact = models.CharField(max_length=100, default='+123 (456) 789')
    chat_resp_time = models.CharField(max_length=100, default='100')

    shipping_on_time = models.CharField(max_length=100, default='100')
    authentic_rating = models.CharField(max_length=100, default='100')
    days_return = models.CharField(max_length=100, default='100')
    warranty_period = models.CharField(max_length=100, default='100')

    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    

    class Meta:
        verbose_name = 'Vendor'
        verbose_name_plural = 'Vendors'

    def vendor_image(self):
        return mark_safe("<img src='%s' width='50'  height='50' />" % (self.image.url)) # noqa

    def __str__(self):
        return str(self.title)


class Product(models.Model):

    pid = ShortUUIDField(
        unique=True, 
        length=10, 
        max_length=30, 
        alphabet='abcdefgh12345'
        )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True) # noqa

    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='category',
        )

    vendor = models.ForeignKey(
        Vendor, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='vendor'
        )

    title = models.CharField(max_length=100, default="Title here")
    image = models.ImageField(upload_to=user_directory_path, default='product.jpg') # noqa
    description = models.TextField(null=True, blank=True, default='This is a product') # noqa

    price = models.DecimalField(max_digits=99999999, decimal_places=2, default='0.99') # noqa
    old_price = models.DecimalField(max_digits=99999999, decimal_places=2, default='1.99') # noqa

    specifications = models.TextField(null=True, blank=True, default='Specification') # noqa

    # tags = models.ForeignKey(Tags, on_delete=models.SET_NULL, null=True)

    product_status = models.CharField(choices=STATUS, max_length=10, default='in_review') # noqa

    status = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    digital = models.BooleanField(default=False)

    sku = ShortUUIDField(
        unique=True, 
        length=4, 
        max_length=10, 
        prefix='sku',
        alphabet='1234567890'
        )

    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    def product_image(self):
        return mark_safe("<img src='%s' width='50'  height='50' />" % (self.image.url)) # noqa

    def __str__(self):
        return str(self.title)

    def get_percentage(self):
        new_price = (self.price / self.old_price) * 100
        return new_price


class ProductImage(models.Model):
    image = models.ImageField(upload_to='product_images/', default='product.jpg') # noqa
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='p_images') # noqa
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Product Images"

    def __str__(self):
        return str(self.product.title)


########################### Cart, Order, OrderItems ######################
########################### Cart, Order, OrderItems ######################
########################### Cart, Order, OrderItems ######################
########################### Cart, Order, OrderItems ######################
########################### Cart, Order, OrderItems ######################


class CartOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=99999999, decimal_places=2, default='0.99') # noqa
    paid_status = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)
    product_status = models.CharField(choices=STATUS_CHOICE, default='processing', max_length=30) # noqa

    class Meta:
        verbose_name_plural = 'Cart Orders'

class CartOrderItem(models.Model):
    order = models.ForeignKey(CartOrder, on_delete=models.CASCADE)
    invoice_number = models.CharField(max_length=200)
    product_status = models.CharField(max_length=200)
    quantity = models.IntegerField(default=0)
    item = models.CharField(max_length=200)
    image = models.CharField(max_length=200)

    price = models.DecimalField(max_digits=99999999, decimal_places=2, default='0.99') # noqa
    total = models.DecimalField(max_digits=99999999, decimal_places=2, default='0.99') # noqa

    class Meta:
        verbose_name_plural = 'Cart Order Items'

    def order_image(self):
        return mark_safe("<img src='/media/%s' width='50'  height='50' />" % (self.image.url)) # noqa



########################### Product review, wishlist, address ######################
########################### Product review, wishlist, address ######################
########################### Product review, wishlist, address ######################
########################### Product review, wishlist, address ######################

class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    review = models.TextField(max_length=300)
    rating = models.IntegerField(choices=RATING, default=None)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Product Reviews'

    def __str__(self):
        return str(self.product.title)

    def get_rating(self):
        return self.rating


class WishList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Wish Lists'

    def __str__(self):
        return str(self.product.title)

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=150, null=True)
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Address'
