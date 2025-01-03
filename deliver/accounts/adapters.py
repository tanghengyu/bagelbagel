# adapters.py
from allauth.account.adapter import DefaultAccountAdapter
from django.shortcuts import resolve_url

class CustomAccountAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        user = request.user
        if hasattr(user, 'profile'):
            if user.profile.role == 'Customer':
                print('This is a customer')
                return resolve_url('customer:customer_profile')  # Replace with the customer profile URL
            elif user.profile.role == 'Merchant':
                return resolve_url('merchant:merchant_dashboard')  # Replace with the merchant dashboard URL
            elif user.profile.role == 'Driver':
                return resolve_url('driver:driver_dashboard')  # Replace with driver dashboard URL
        return super().get_login_redirect_url(request)