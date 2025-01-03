"""
URL configuration for deliver project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings 
from django.conf.urls.static import static

from accounts.views import Index as main_index
from customer.views import Index, About, Order, OrderConfirmation, OrderPayConfirmation

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    # path('accounts/', include('accounts.urls')),
    path('', main_index.as_view(), name='index'),
    path('customer/', include('customer.urls')),
    path('merchant/', include('merchant.urls')),
    path('driver/', include('driver.urls')),
    path('about/', About.as_view(), name='about'),
    path('order/', Order.as_view(), name='order'), 
    # path('shopping_cart/', ShoppingCart.as_view(), name='shopping_cart'),
    path('order-confirmation/<int:pk>', OrderConfirmation.as_view(), name='order-confirmation'),
    path('payment-confirmation/', OrderPayConfirmation.as_view(), name='payment-submitted'),
    # path('register/', Register.as_view(), name='register'), 
    # path('login/', UserLoginView.as_view(),name='login')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
