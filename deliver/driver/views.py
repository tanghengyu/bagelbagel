from django.shortcuts import render
from django.views import View 
# Create your views here.
class DriverDashboardView(View):
    def get(self, request, *args, **kwargs):
        # Fetch current orders for the logged-in customer
        return render(request, 'driver/dashboard.html')