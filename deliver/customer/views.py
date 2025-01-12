from django.shortcuts import render, redirect, get_object_or_404
from django.views import View 
from django.core.mail import send_mail
from .models import MenuItem, Category, OrderModel, Profile, ShoppingCartModel, CartItem, Message
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin # validate the request based on 

import json

# Create your views here.
class Index(View):
    def get(self, request, *args, **kwargs):
        # return render(request, 'customer/index.html')
        return render(request, 'customer/dev_index.html')
class About(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/about.html')
    


# class Register(View):
#     def get(self, request, *args, **kwargs):
#         return render(request, 'customer/register.html')
    
#     def post(self, request, *args, **kwargs):
#         username = request.POST.get("username")
#         email = request.POST.get("email")
#         password = request.POST.get("password")
#         role = request.POST.get("role")
#         store_location = request.POST.get("store_location", None)
#         menu_items = request.POST.get("menu_items", None)
#         vehicle_info = request.POST.get("vehicle_info", None)
#         print('grabbing information for {}'.format(username))
#         if User.objects.filter(username=username).exists():
#             messages.error(request, "Username already exists.")
#             return redirect("index")

#         user = User.objects.create_user(username=username, email=email, password=password)
#         profile = Profile.objects.create(
#             user=user,
#             role=role,
#             store_location=store_location if role == "Merchant" else None,
#             menu_items=menu_items if role == "Merchant" else None,
#             vehicle_info=vehicle_info if role == "Driver" else None,
#         )
#         # Save role-specific data
#         profile.save()
        
#         messages.success(request, "Registration successful! Please check your email to activate your profile.")
#         return redirect("login")
    
# from django.contrib.auth.views import LoginView

# class UserLoginView(LoginView):
#     template_name = 'customer/login.html'

#     def get_success_url(self):
#         """Redirect users after successful login."""
#         return self.request.GET.get('next', '/')
    
# from django.contrib.auth.views import LoginView

# class UserLoginView(View):
#     template_name = 'customer/login.html'
#     def get(self, request, *args, **kwargs):
#         return render(request, 'customer/login.html') 

    # def get_success_url(self):
    #     """Redirect users after successful login."""
    #     return self.request.GET.get('next', '/')
    
class MerchantIndexView(View):
    def get(self, request, *args, **kwargs):
        merchants = Profile.objects.filter(role='Merchant')
        context = {'merchants': merchants}
        return render(request, 'customer/merchant_index.html', context)

class MerchantOrderView(UserPassesTestMixin, View):
    def get(self, request, merchant_id, *args, **kwargs):
        # Get the merchant profile
        merchant = get_object_or_404(Profile, id=merchant_id, role='Merchant')

        # Get menu items specific to this merchant
        # menu_items = MenuItem.objects.filter(merchant=merchant)
        categories = Category.objects.filter(merchant=merchant)
        # for category in categories:
        #     for curr_item in category.item.all():
        #         print(curr_item.name)

        # Pass the merchant and menu items to the template
        context = {
            'merchant': merchant,
            'categories': categories
        }
        return render(request, 'customer/merchant_menu.html', context)
    def post(self, request, *args, **kwargs):

        shopping_cart, created = ShoppingCartModel.objects.get_or_create(customer=request.user)

        # Process the items added to the cart
        for item_id, quantity in request.POST.items():
            if item_id.startswith('quantity['):
                menu_item_id = item_id.split('[')[1].strip(']')
                menu_item = get_object_or_404(MenuItem, id=menu_item_id)
                quantity = int(quantity)

                if quantity > 0:
                    # Add or update the cart item
                    cart_item, created = CartItem.objects.get_or_create(cart=shopping_cart, menu_item=menu_item)
                    cart_item.quantity = quantity
                    cart_item.save()
                else:
                    # Remove the item from the cart if the quantity is 0
                    CartItem.objects.filter(cart=shopping_cart, menu_item=menu_item).delete()

        return redirect('customer:customer_shopping_cart')

    def test_func(self):
        return self.request.user.profile.role =='Customer'


class Order(UserPassesTestMixin, View):
    def get(self, request, *args, **kwargs):
        
        # get every item from each category
        bagels  = MenuItem.objects.filter(category__name__contains='Bagels')

        schmears  = MenuItem.objects.filter(category__name__contains='Schmears')

        drinks  = MenuItem.objects.filter(category__name__contains='Drinks')


        # pass into the contexts
        context = {'bagels': bagels, 
                   'schmears': schmears, 
                   'drinks': drinks} 
        
        # render teh template 
        # return render(request, 'customer/order_dev.html', context)
        return render(request, 'customer/order.html', context)
    def test_func(self):
        return self.request.user.profile.role =='Customer'

    def post(self, request, *args, **kwargs):

        shopping_cart, created = ShoppingCartModel.objects.get_or_create(customer=request.user)

        # Process the items added to the cart
        for item_id, quantity in request.POST.items():
            if item_id.startswith('quantity['):
                menu_item_id = item_id.split('[')[1].strip(']')
                menu_item = get_object_or_404(MenuItem, id=menu_item_id)
                quantity = int(quantity)

                if quantity > 0:
                    # Add or update the cart item
                    cart_item, created = CartItem.objects.get_or_create(cart=shopping_cart, menu_item=menu_item)
                    cart_item.quantity = quantity
                    cart_item.save()
                else:
                    # Remove the item from the cart if the quantity is 0
                    CartItem.objects.filter(cart=shopping_cart, menu_item=menu_item).delete()

        return redirect('customer:customer_shopping_cart')



from django.http import JsonResponse
class OrderConfirmation(View):
    def get(self, request, pk, *args, **kwargs):
        order = OrderModel.objects.get(pk=pk)

        context = {
            'pk': order.pk, 
            'items': order.items, 
            'price': order.price
        }
        return render(request, 'customer/order_confirmation.html', context)
    
    def post(self, request, pk, *args, **kwargs):
        order = OrderModel.objects.get(pk=pk)
        print('Is this executed')
        order.is_paid = True
        order.save()
        return redirect('payment-submitted')


    # def post(self, request, pk, *args, **kwargs):
    #     if request.content_type != 'application/json':
    #         return JsonResponse({'error': 'Invalid Content-Type. Expected application/json.'}, status=400)

    #     try:
    #         data = json.loads(request.body)
    #         print("Parsed data:", data)

    #         # Process the data
    #         if data.get('isPaid'):
    #             order = OrderModel.objects.get(pk=pk)
    #             order.is_paid = True
    #             order.save()
    #             return JsonResponse({'message': 'Order marked as paid successfully.'})
    #         else:
    #             return JsonResponse({'error': 'isPaid flag is missing or false.'}, status=400)

    #     except json.JSONDecodeError as e:
    #         print("JSON decode error:", str(e))
    #         return JsonResponse({'error': 'Invalid JSON format.'}, status=400)

    #     except Exception as e:
    #         print("Unexpected error:", str(e))
    #         return JsonResponse({'error': 'An unexpected error occurred.'}, status=500)
    #     return redirect('payment-submitted')

class OrderPayConfirmation(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/order_pay_confirmation.html')


from django.contrib.auth.mixins import LoginRequiredMixin # validate the request based on 

class CustomerProfileView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        # current_orders = get_object_or_404(OrderModel, customer=request.user)
        curr_customer = Profile.objects.get(user=request.user, role='Customer')
        current_orders = OrderModel.objects.filter(customer=curr_customer).order_by('created_on')

        # orders = OrderModel.objects.filter(created_on__year=today.year, created_on__month=today.month, created_on__day__lte=today.day,
        #                                    merchant=merchant)
        

        shopping_cart = get_object_or_404(ShoppingCartModel, customer=request.user)
        shopping_cart_total_price = shopping_cart.calculate_total_price()
        cart_items = shopping_cart.cart_items.all() if shopping_cart else [] 
        if len(cart_items) > 0:
            for curr_item in cart_items:
                curr_item.total_price = curr_item.item_total_price()
        curr_customer = get_object_or_404(Profile, user=request.user, role='Customer')
        notifications = Message.objects.filter(recipient=curr_customer, is_read=False)
        notifications_count = notifications.count()
        context = {
            'notifications': notifications,
            'notifications_count': notifications_count,
            'current_orders': current_orders,
            'shopping_cart_items': cart_items,
            'shopping_cart_total_price': shopping_cart_total_price
        }
        return render(request, 'customer/customer_profile.html', context)
        
        # # Fetch current orders for the logged-in customer
        # current_orders = OrderModel.objects.filter(email=request.user.email, is_paid=True).order_by('-created_on')

        # # Fetch the shopping cart for the logged-in customer
        # shopping_cart = ShoppingCartModel.objects.filter(customer=request.user).first()
        # shopping_cart_items = shopping_cart.cart_items.all() if shopping_cart else []
        # total_price = shopping_cart.calculate_total_price() if shopping_cart else 0

        # context = {
        #     'current_orders': current_orders,
        #     'shopping_cart_items': shopping_cart_items,
        #     'total_price': total_price,
        # }
        # return render(request, 'customer/customer_profile.html', context)
class OrderDetailView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        pass
        curr_order = OrderModel.object.filter(pk=pk)
        # curr_order


class CancelOrderView(LoginRequiredMixin, View):
    def post(self, request, order_id, *args, **kwargs):
        print(f"Canceling order ID: {order_id}")  # Debug output
        
        curr_order = get_object_or_404(OrderModel, pk=order_id)
        print(f'previous status {curr_order.status}')
        curr_order.status = 'Cancelled'
        curr_order.save()
        print(f'current status {curr_order.status}')

        return JsonResponse({'success': True, 'order_id': curr_order.pk})
        # messages.success(request, f"Order #{curr_order.pk} has been successfully canceled.")
        # return JsonResponse({'success': True, 'order_id': curr_order.pk})


class ShoppingCartView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        # shopping_cart = ShoppingCartModel.objects.filter(customer=request.user).first()
        shopping_cart = get_object_or_404(ShoppingCartModel, customer=request.user)
        cart_items = shopping_cart.cart_items.all() if shopping_cart else [] 
        total_price = shopping_cart.calculate_total_price() if shopping_cart else 0
        for curr_item in cart_items:
            curr_item.total_price = curr_item.item_total_price()

        context = {
            'cart_items': cart_items,
            'total_price': total_price,
        }
        return render(request, 'customer/shopping_cart.html', context)
    def post(self, request, *args, **kwargs):
        name=request.POST.get('name')
        email=request.POST.get('email')
        street=request.POST.get('street')
        city=request.POST.get('city')
        state=request.POST.get('state')
        zip_code=request.POST.get('zip_code')

        order_items = {
            'items': [], 


        }

        item_ids_list = []            
        shopping_cart = get_object_or_404(ShoppingCartModel, customer=request.user)
        cart_items = shopping_cart.cart_items.all() if shopping_cart else [] 
        order_total_price = shopping_cart.calculate_total_price()
        for cart_item in cart_items:
            order_items['items'].append({'id': cart_item.menu_item.pk, 
                                         'name': cart_item.menu_item.name, 
                                         'price': cart_item.menu_item.price,
                                         })
            #order_total_price += cart_item.quantity * cart_item.menu_item.price
            
            item_ids_list.append(cart_item.menu_item.pk)  
        order_merchant = cart_item.menu_item.merchant
        order_customer = Profile.objects.get(user=request.user, role='Customer')

        order = OrderModel.objects.create(price=order_total_price, name=name, email=email, street=street, city=city, state=state, zip_code=zip_code, 
                                          merchant=order_merchant, customer = order_customer
        )
        order.items.add(*item_ids_list)


        body = ('Thank you for your order! Your food is being prepared and will be delivered soon!\n'
                f'Your total price: ${order_total_price}\n'
        )

        # User hitting the submit button send the confirmation 
        send_mail(
            'Thank you for Your Order!',
            body,
            'orderconfirmation@bagelbagel.com', 
            [email],
            fail_silently=False
        )

        context = {
            'items': order_items['items'],
            'price': order_total_price
        }

        for cart_item in cart_items:
            cart_item.delete()
        # items = request.POST.getlist('items[]')
        # for item in items:
        #     menu_item =  MenuItem.objects.get(pk__contains=int(item))
        #     item_data = {'id': menu_item.pk, 
        #                  'name': menu_item.name, 
        #                  'price': menu_item.price}
            
        #     order_items['items'].append(item_data)

        # price = 0
        # item_ids =[]
        # for item in order_items['items']:
        #     price += item['price']
        #     item_ids.append(item['id'])
        
        # Create a notification for the merchant
        Message.objects.create(
            sender=order_customer,  # The customer who placed the order
            recipient=order_merchant,  # The merchant receiving the notification
            order=order,
            message=f"New order #{order.id} has been placed by {order_customer.user.username}."
        )
        return redirect('order-confirmation', pk=order.pk)


class RemoveFromCartView(LoginRequiredMixin, View):
    def post(self, request, item_id, *args, **kwargs):
        # Remove a specific item from the cart
        shopping_cart = ShoppingCartModel.objects.filter(customer=request.user).first()
        if shopping_cart:
            cart_item = get_object_or_404(shopping_cart.cart_items, id=item_id)
            cart_item.delete()
        return redirect('customer:customer_shopping_cart')

class MarkNotificationReadView(LoginRequiredMixin, View):
    def post(self, request, notification_id, *args, **kwargs):
        notification = get_object_or_404(Message, pk=notification_id, recipient=request.user.profile)
        notification.is_read = True
        notification.save()
        return JsonResponse({'success': True})