from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
from userauths.models import User
from django_ckeditor_5.fields import CKEditor5Field

from taggit.managers import TaggableManager


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
    description = CKEditor5Field(null=True, blank=True, default='I am a vendor', config_name='extends') # noqa

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

    STATUS= (
        ("draft", 'Draft'),
        ("disabled", 'Disabled'),
        ("rejected", 'Rejected'),
        ("in_review", 'In review'),
        ("published", 'Published'),
    )

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
    description = CKEditor5Field(null=True, blank=True, default='This is a product', config_name='extends') # noqa

    price = models.DecimalField(max_digits=99999999, decimal_places=2, default='0.99') # noqa
    old_price = models.DecimalField(max_digits=99999999, decimal_places=2, default='1.99') # noqa

    specifications = CKEditor5Field(null=True, blank=True, default='Specification', config_name='extends') # noqa

    tags = TaggableManager(blank=True)

    product_status = models.CharField(choices=STATUS, max_length=10, default='in_review') # noqa

    status = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    digital = models.BooleanField(default=False)

    stock_count = models.PositiveIntegerField(blank=True, null=True)
    product_type = models.CharField(max_length=100, default="Ornganic", blank=True, null=True)
    manufactured = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    life = models.CharField(max_length=100, default="100 Days", blank=True, null=True)

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
        
    @classmethod    
    def get_status(self):
        return self.STATUS


class ProductImage(models.Model):
    image = models.ImageField(upload_to='product_images/', default='product.jpg') # noqa
    product = models.ForeignKey(
        Product, 
        on_delete=models.SET_NULL,
        null=True, 
        related_name='p_images')

    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Product Images"

    def __str__(self):
        return str(self.product.title)


########################### Product review, address ######################
########################### Product review, address ######################
########################### Product review, address ######################
########################### Product review, address ######################

class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='p_reviews')
    review = models.TextField(max_length=300)
    rating = models.IntegerField(choices=RATING, default=None)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Product Reviews'

    def __str__(self):
        return str(self.product.title)

    def get_rating(self):
        return self.rating


class Coupon(models.Model):
    code = models.CharField(max_length=50, blank=True)
    discount = models.IntegerField(default=1)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.code
