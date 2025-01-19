from django.shortcuts import render, get_object_or_404, redirect
from django.views import View 
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin # validate the request based on 
# login requried 
from django.utils.timezone import datetime
from django.contrib import messages  # Import the messages module

from customer.models import OrderModel, Profile, MenuItem, Category, Message
# Create your views here.


class MerchantDashboard(LoginRequiredMixin,  UserPassesTestMixin, View):
    def get(self, request, *args, **kwargs):
        # get the current date 
        today=datetime.today()
        merchant = get_object_or_404(Profile, user=request.user, role='Merchant')
        orders = OrderModel.objects.filter(created_on__year=today.year, created_on__month=today.month, created_on__day__lte=today.day,
                                           merchant=merchant).order_by('-created_on')[:10]

        # loop through the orders and add the price values 
        total_revenue = 0
        for order in orders:
            total_revenue+= order.price 


        menu_items = MenuItem.objects.filter(merchant=merchant)
        notifications = Message.objects.filter(recipient=merchant, is_read=False)
        notifications_count = notifications.count()
        # categories = Category.objects.all()
        categories = Category.objects.filter(merchant=merchant)
        # pass total number of orders and total revenus into template 
        context = {
            'merchant': merchant,
            'notifications': notifications,
            'notifications_count': notifications_count,
            'orders': orders, 
            'total_revenue': total_revenue,
            'total_orders': len(orders), 
            'categories': categories, 
            'menu_items': menu_items
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
    

class ChangeItemStatusView(LoginRequiredMixin, UserPassesTestMixin, View):
    def post(self, request, item_id, *args, **kwargs):
        menu_item = get_object_or_404(MenuItem, pk=item_id, merchant=request.user.profile)
        is_available = request.POST.get('is_available') == 'True'
        menu_item.is_available = is_available
        menu_item.save()
        return redirect('merchant:merchant_dashboard')

    def test_func(self):
        return self.request.user.profile.role == 'Merchant'
class DeleteMenuItem(LoginRequiredMixin, UserPassesTestMixin, View):
    def post(self, request, item_id, *args, **kwargs):
        menu_item = get_object_or_404(MenuItem, pk=item_id, merchant=request.user.profile)

        menu_item.delete()
        return redirect('merchant:merchant_dashboard')

    def test_func(self):
        # Restrict access to only merchants
        return self.request.user.profile.role == 'Merchant'
class AcceptOrderView(LoginRequiredMixin, View):
    def post(self, request, order_id, *args, **kwargs):
        order = get_object_or_404(OrderModel, pk=order_id, merchant=request.user.profile)
        order.status = 'Under Preparation'
        order.save()

        # Mark the related notification as read
        Message.objects.filter(order=order).update(is_read=True)
        order_merchant = Profile.objects.get(user=request.user, role='Merchant')
        
        Message.objects.create(
            sender=order_merchant,  # The customer who placed the order
            recipient=order.customer,  # The merchant receiving the notification
            order=order,
            message=f"Your order #{order.id} has been accepted by {order.merchant.user.username}."
        )
        # Notify all available drivers
        available_drivers = Profile.objects.filter(role='Driver')
        for driver in available_drivers:
            Message.objects.create(
                sender=request.user.profile,  # Merchant sending the notification
                recipient=driver,  # Driver receiving the notification
                order=order,
                message=f"New order #{order.id} from {order.merchant.user.username} is available for delivery.",
                requires_action=True
            )
        return redirect('merchant:merchant_dashboard')


class DeclineOrderView(LoginRequiredMixin, View):
    def get(self, request, order_id, *args, **kwargs):
        order = get_object_or_404(OrderModel, pk=order_id, merchant=request.user.profile)
        order.status = 'Cancelled'
        order.save()

        # Mark the related notification as read
        Message.objects.filter(order=order).update(is_read=True)

        return redirect('merchant:merchant_dashboard')
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
        order.status = 'Ready for Pickup'
        order.save()
        Message.objects.create(
            sender=request.user.profile,  # Merchant sending the notification
            recipient=order.driver,  # Driver receiving the notification
            order=order,
            message=f"Order #{order.id} from {order.merchant.user.username} is ready for pick up."
        )
        context = {'order': order}

        return render(request, 'merchant/order_details.html', context )
    
    def test_func(self):
        # validate if the users are allowed to view the dashbaord or not for user passes
        # return self.request.user.groups.filter(name='Merchant').exists()
        return self.request.user.profile.role =='Merchant'
from django.http import JsonResponse
class MarkNotificationReadView(View):
    def post(self, request, notification_id, *args, **kwargs):
        # Retrieve the notification
        notification = get_object_or_404(Message, pk=notification_id, recipient=request.user.profile)
        
        # Mark the notification as read
        notification.is_read = True
        notification.save()

        # Respond with success
        return JsonResponse({'success': True})

class ChangeOrderStatusView(View):
    def post(self, request, pk, *args, **kwargs):
        # Fetch the order
        order = get_object_or_404(OrderModel, pk=pk)

        # Ensure the order is currently "Ready for Pickup"
        if order.status != 'Ready for Pickup':
            return redirect(request.META.get('HTTP_REFERER', '/'))

        # Determine if the user is authorized (merchant or driver)
        if request.user.profile.role == 'Merchant' and order.merchant == request.user.profile:
            order.status = 'Order On the Way'
            order.save()

        else:
            return redirect(request.META.get('HTTP_REFERER', '/'))

        # Notify the customer about the status change
        Message.objects.create(
            sender=request.user.profile,
            recipient=order.customer,
            order=order,
            message=f"Your order #{order.id} is now on the way.",
            requires_action=False
        )

        return redirect('merchant:order-details', pk=pk)

from django.utils.dateparse import parse_date

class ViewOrderHistoryView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        curr_merchant = Profile.objects.get(user=request.user, role='Merchant')

        # Get the start and end dates from the query parameters
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        # Filter orders based on the date range
        all_orders = OrderModel.objects.filter(merchant=curr_merchant).order_by('-created_on')
        if start_date:
            all_orders = all_orders.filter(created_on__date__gte=parse_date(start_date))
        if end_date:
            all_orders = all_orders.filter(created_on__date__lte=parse_date(end_date))

        context = {
            'all_orders': all_orders,
            'start_date': start_date,
            'end_date': end_date,
        }
        return render(request, 'merchant/order_history.html', context)



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