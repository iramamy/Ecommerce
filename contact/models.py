from django.db import models

class ContactUs(models.Model):
    first_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    subject = models.CharField(max_length=300)
    message = models.TextField()

    class Meta:
        verbose_name_plural = 'ContactUs'

    def __str__(self):
        return f"{self.first_name} - {self.subject}"

    