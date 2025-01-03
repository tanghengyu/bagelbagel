from django.shortcuts import render, get_object_or_404, redirect
from django.views import View 
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin # validate the request based on 
# login requried 
from django.utils.timezone import datetime
from django.contrib import messages  # Import the messages module

from customer.models import OrderModel, Profile, MenuItem, Category
# Create your views here.


class MerchantDashboard(LoginRequiredMixin,  UserPassesTestMixin, View):
    def get(self, request, *args, **kwargs):
        # get the current date 
        today=datetime.today()
        merchant = get_object_or_404(Profile, user=request.user, role='Merchant')
        orders = OrderModel.objects.filter(created_on__year=today.year, created_on__month=today.month, created_on__day__lte=today.day,
                                           merchant=merchant)

        # loop through the orders and add the price values 
        total_revenue = 0
        for order in orders:
            total_revenue+= order.price 

        # categories = Category.objects.all()
        categories = Category.objects.filter(merchant=merchant)
        # pass total number of orders and total revenus into template 
        context = {
            'merchant': merchant,
            'orders': orders, 
            'total_revenue': total_revenue,
            'total_orders': len(orders), 
            'categories': categories
        }
        return render(request, 'merchant/dashboard.html', context)
    
    def post(self, request, *args, **kwargs):
        # Get the logged-in merchant's profile
        try:
            merchant = Profile.objects.get(user=request.user, role='Merchant')

            # Process the form data to create a new menu item
            name = request.POST['name']
            description = request.POST['description']
            price = request.POST['price']
            image = request.FILES['image']
            category = Category.objects.get(id=request.POST['category'], merchant=merchant)

            menu_item = MenuItem.objects.create(
                name=name,
                description=description,
                price=price,
                image=image, 
                merchant=merchant
            )
            menu_item.category.add(category)  # Add category to the menu item
            menu_item.save()
            messages.success(request, "Menu item added successfully!")
        except Exception as e:
            # Add an error message if something goes wrong
            messages.error(request, f"Failed to add menu item: {str(e)}")

    
        return redirect('merchant:merchant_dashboard')

    def test_func(self):
        # validate if the users are allowed to view the dashbaord or not for user passes
        return self.request.user.profile.role =='Merchant'

class AddCategoryView(LoginRequiredMixin, UserPassesTestMixin,View):
    def post(self, request, *args, **kwargs):
        merchant = request.user.profile
        if merchant.role != 'Merchant':
            messages.error(request, "You do not have permission to add a category.")
            return redirect('merchant:merchant_dashboard')
        

        new_cat_name = request.POST.get('categoryName')
        try: 
            new_category = Category.objects.create(name=new_cat_name, merchant =merchant)
            new_category.save()
            messages.success(request, "Category added successfully!")

        except Exception as e:
            messages.error(request, f"Error adding category: {str(e)}")

        return redirect('merchant:merchant_dashboard')

    def test_func(self):
        # validate if the users are allowed to view the dashbaord or not for user passes
        return self.request.user.profile.role =='Merchant'
    

class Dashboard(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, *args, **kwargs):
        # get the current date 
        today=datetime.today()
        orders = OrderModel.objects.filter(created_on__year=today.year, created_on__month=today.month, created_on__day__lte=today.day)

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
        #return self.request.user.groups.filter(name='Staff').exists()
        return self.request.user.profile.role =='Merchant'
    
class OrderDetails(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, pk, *args, **kwargs):
        order = OrderModel.objects.get(pk=pk)
        context = {
            'order': order
        }
        return render(request, 'merchant/order_details.html', context)
    
    def post(self, request, pk, *args, **kwargs):
        order = OrderModel.objects.get(pk=pk)
        order.ready_for_pickup=True 
        order.save()

        context = {'order': order}

        return render(request, 'merchant/order_details.html', context )
    
    def test_func(self):
        # validate if the users are allowed to view the dashbaord or not for user passes
        # return self.request.user.groups.filter(name='Merchant').exists()
        return self.request.user.profile.role =='Merchant'