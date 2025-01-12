from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class MenuItem(models.Model):
    
    name=models.CharField(max_length=128)
    description=models.TextField()
    image=models.ImageField(upload_to='menu_images/')
    price=models.DecimalField(max_digits=5, decimal_places=2)
    category=models.ManyToManyField('Category', related_name='item')
    is_available=models.BooleanField(default=True)
    merchant = models.ForeignKey(
        'Profile',
        on_delete=models.CASCADE,
        related_name='menu_items',
        limit_choices_to={'role': 'Merchant'}, 
        null=True, 
        blank=True
    )

    def __str__(self):
        return self.name

class Category(models.Model):
    name=models.CharField(max_length=128)
    merchant = models.ForeignKey(
        'Profile',
        on_delete=models.CASCADE,
        related_name='categories',
        limit_choices_to={'role': 'Merchant'}, 
        null=True, 
        blank=True
    )
    def __str__(self):
        return self.name

class Profile(models.Model):
    ROLE_CHOICES = [
        ('Customer', 'Customer'),
        ('Merchant', 'Merchant'),
        ('Driver', 'Driver'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    store_location = models.CharField(max_length=255, null=True, blank=True)
    # menu_items = models.TextField(null=True, blank=True)
    vehicle_info = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"

class OrderModel(models.Model):
    STATUS_CHOICES = [
    ('Pending', 'Pending'),
    ('Under Preparationp', 'Under Preparation'),    
    ('Ready for Pickup', 'Ready for Pickup'),
    ('Delivered', 'Delivered'),
    ('Completed', 'Completed'),
    ('Cancelled', 'Cancelled'),
    ]
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
    ready_for_pickup = models.BooleanField(default=False)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending',
    )
    # New Field: Merchant the order belongs to
    merchant = models.ForeignKey(
        'customer.Profile',  # Assuming Profile is in the same app
        on_delete=models.CASCADE,
        related_name='orders',
        limit_choices_to={'role': 'Merchant'},  # Restrict to Merchant roles
        null=True,
        blank=True
    )
    customer =  models.ForeignKey(
        'customer.Profile', # Assuming Profile is in the same app
        on_delete=models.CASCADE,
        related_name='orders_cust',
        limit_choices_to={'role': 'Customer'},  # Restrict to Merchant roles
        null=True,
        blank=True
    )
    def __str__(self):
        return f'Order: {self.created_on.strftime("%b %d %I: %M %p")}'
# class Notification(models.Model):
#     merchant = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='notifications')
#     order = models.ForeignKey('OrderModel', on_delete=models.CASCADE, related_name='notifications')
#     message = models.CharField(max_length=255)
#     is_read = models.BooleanField(default=False)
#     created_on = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Notification for {self.merchant.user.username}: {self.message}"

class Message(models.Model):
    sender = models.ForeignKey(
        'Profile',
        on_delete=models.CASCADE,
        related_name='sent_notifications',
        help_text="The user sending the notification"
    )
    recipient = models.ForeignKey(
        'Profile',
        on_delete=models.CASCADE,
        related_name='received_notifications',
        help_text="The user receiving the notification"
    )
    order = models.ForeignKey(
        'OrderModel',
        on_delete=models.CASCADE,
        related_name='notifications',
        null=True,
        blank=True,
        help_text="Associated order for the notification"
    )
    message = models.CharField(max_length=255, help_text="Notification message")
    is_read = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification from {self.sender.user.username} to {self.recipient.user.username}: {self.message}"

    
class ShoppingCartModel(models.Model):
    customer = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name="shopping_cart",
        limit_choices_to={'profile__role': 'Customer'}  # Restrict association to Customer role
    )
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now_add=True)

    # price = models.DecimalField(max_digits=7, decimal_places=2)
    # quantity = models.PositiveIntegerField(default=1)

    # is_empty = models.BooleanField(default=True)


    def __str__(self):
        return f"ShoppingCart for {self.customer.username}"

    def calculate_total_price(self):
        """
        Calculates the total price of all items in the cart.
        """
        return sum(item.quantity * item.menu_item.price for item in self.cart_items.all())
    
    def calculate_total_quantity(self):
        return sum(item.quantity for item in self.cart_items.all())
    
    def is_empty(self):
        return len(self.cart_items.all()) == 0
    
class CartItem(models.Model):
    """
    Represents an individual item in a shopping cart.
    """
    cart = models.ForeignKey(ShoppingCartModel, on_delete=models.CASCADE, related_name="cart_items")
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=5, decimal_places=2, default = 0.00)

    def item_total_price(self): return self.quantity * self.menu_item.price

    def __str__(self):
        return f"{self.quantity} x {self.menu_item.name} in {self.cart.customer.username}'s cart"


# Signal to automatically create a ShoppingCart for Customer users
@receiver(post_save, sender=Profile)
def create_shopping_cart_for_customer(sender, instance, created, **kwargs):
    if created and instance.role == 'Customer':
        ShoppingCartModel.objects.get_or_create(customer=instance.user)