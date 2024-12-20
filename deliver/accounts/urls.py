from django.urls import path
from allauth.account.views import SignupView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='custom_signup'),
]