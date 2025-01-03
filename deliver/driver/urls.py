from django.urls import path
from .views import DriverDashboardView
app_name = 'driver'
urlpatterns = [
    path('dashboard/', DriverDashboardView.as_view(), name='driver_dashboard'),
]