from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class MenuItem(models.Model):
    name=models.CharField(max_length=128)
    description=models.TextField()
    image=models.ImageField(upload_to='menu_images/')
    price=models.DecimalField(max_digits=5, decimal_places=2)
    category=models.ManyToManyField('Category', related_name='item')

    def __str__(self):
        return self.name

class Category(models.Model):
    name=models.CharField(max_length=128)

    def __str__(self):
        return self.name
class Profile(models.Model):
    ROLE_CHOICES = [
        ('Customer', 'Customer'),
        ('Merchant', 'Merchant'),
        ('Driver', 'Driver'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    store_location = models.CharField(max_length=255, null=True, blank=True)
    menu_items = models.TextField(null=True, blank=True)
    vehicle_info = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.user.username
class OrderModel(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    items = models.ManyToManyField('MenuItem', related_name='order', blank=True)

    name=models.CharField(max_length=128, blank=True)
    email=models.CharField(max_length=128, blank=True)
    street=models.CharField(max_length=128, blank=True)
    city=models.CharField(max_length=128, blank=True)
    state=models.CharField(max_length=15, blank=True)
    zip_code = models.IntegerField(blank=True, null=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f'Order: {self.created_on.strftime("%b %d %I: %M %p")}'