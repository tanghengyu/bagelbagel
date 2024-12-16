from django.shortcuts import render
from django.views import View 
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin # validate the request based on 
# login requried 
from django.utils.timezone import datetime
from customer.models import OrderModel
# Create your views here.

class Dashboard(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, *args, **kwargs):
        # get the current date 
        today=datetime.today()
        orders = OrderModel.objects.filter(created_on__year=today.year, created_on__month=today.month, created_on__day=today.day)

        # loop through the orders and add the price values 
        total_revenue = 0
        for order in orders:
            total_revenue+= order.price 

        # pass total number of orders and total revenus into template 
        context = {
            'orders': orders, 
            'total_revenue': total_revenue,
            'total_orders': len(orders)
        }
        return render(request, 'merchant/dashboard.html', context)
    
    def test_func(self):
        # validate if the users are allowed to view the dashbaord or not for user passes
        return self.request.user.groups.filter(name='Staff').exists()