from django.urls import path
from .views import CustomerProfileView
app_name = 'customer'
urlpatterns = [
    path('profile/', CustomerProfileView.as_view(), name='customer_profile'),
]