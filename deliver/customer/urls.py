from django.urls import path
from .views import CustomerProfileView, ShoppingCartView,RemoveFromCartView, MerchantIndexView, MerchantOrderView, OrderDetailView
app_name = 'customer'
urlpatterns = [
    path('profile/', CustomerProfileView.as_view(), name='customer_profile'),
    path('mechant_index/', MerchantIndexView.as_view(), name='merchant_index'),
    path('merchant_menu/<int:merchant_id>/', MerchantOrderView.as_view(), name='merchant_menu'),
    path('shopping_cart/', ShoppingCartView.as_view(), name='customer_shopping_cart'),
    path('remove-from-cart/<int:item_id>/', RemoveFromCartView.as_view(), name='remove_from_cart'),
    path('order-details/<int:item_id>/', OrderDetailView.as_view(), name='order_details')

]