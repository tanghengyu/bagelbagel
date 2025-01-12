from django.contrib import admin
from .models import MenuItem, Category, OrderModel, ShoppingCartModel, CartItem, Profile, Message
# Register your models here.
admin.site.register(MenuItem)
admin.site.register(Category)
admin.site.register(OrderModel)
admin.site.register(ShoppingCartModel)
admin.site.register(CartItem)
admin.site.register(Profile)
admin.site.register(Message)

class OrderModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_on', 'price', 'status', 'is_paid', 'ready_for_pickup')
    list_filter = ('status', 'is_paid', 'ready_for_pickup')
    search_fields = ('name', 'email', 'status')