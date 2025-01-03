from django.urls import path
from .views import Dashboard, OrderDetails, MerchantDashboard, AddCategoryView
app_name = 'merchant'
urlpatterns = [
    path('merchant_dashboard/', MerchantDashboard.as_view(), name='merchant_dashboard'),
    path('dashboard/', Dashboard.as_view(), name='dashboard'), 
    path('orders/<int:pk>', OrderDetails.as_view(), name='order-details'), 
    path('add_category/', AddCategoryView.as_view(), name = 'add_category')
]