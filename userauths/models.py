from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.html import mark_safe


class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return str(self.username)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200, default='First name')
    last_name = models.CharField(max_length=200, blank=True, null=True, default='Last name')
    image = models.ImageField(upload_to='userprofile/', default='userprofile/default.png', blank=True, null=True)
    bio = models.TextField(blank=True, null=True, default='Bio')
    verified = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=100, blank=True, default='12345678')
    address = models.CharField(max_length=200, blank=True, null=True, default='Your address')
    country = models.CharField(max_length=200, blank=True, null=True, default='Your country')


    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.first_name
    
    def profile_image(self):
        return mark_safe(f"<img src='{self.image.url}' width='50'  height='50' style='border-radius:50%;'/>")

        profile_image.short_description = 'Profile Image'

    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    first_name = models.CharField(max_length=100, default='First name')
    last_name = models.CharField(max_length=100, default='Last name')
    address1 = models.CharField(max_length=255, default='Address 1')
    address2 = models.CharField(max_length=255, blank=True, null=True, default='Address 2')
    zipcode = models.CharField(max_length=20, blank=True, null=True, default='000')
    phone = models.CharField(max_length=20, null=True, default='Phone')
    city = models.CharField(max_length=255, blank=True, null=True, default='City')
    country = models.CharField(max_length=255, blank=True, null=True, default='Country')
    company_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField()
    additional_information = models.TextField(blank=True, null=True)
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Address'

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.address1

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    UserProfile.objects.get_or_create(user=instance)
    instance.userprofile.save()