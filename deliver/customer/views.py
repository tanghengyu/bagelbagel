from django.shortcuts import render, redirect, get_object_or_404
from django.views import View 
from django.core.mail import send_mail
from .models import MenuItem, Category, OrderModel, Profile, ShoppingCartModel
from django.contrib.auth.models import User
from django.contrib import messages
import json

# Create your views here.
class Index(View):
    def get(self, request, *args, **kwargs):
        # return render(request, 'customer/index.html')
        return render(request, 'customer/dev_index.html')
class About(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/about.html')
class Register(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/register.html')
    
    def post(self, request, *args, **kwargs):
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        role = request.POST.get("role")
        store_location = request.POST.get("store_location", None)
        menu_items = request.POST.get("menu_items", None)
        vehicle_info = request.POST.get("vehicle_info", None)
        print('grabbing information for {}'.format(username))
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("index")

        user = User.objects.create_user(username=username, email=email, password=password)
        profile = Profile.objects.create(
            user=user,
            role=role,
            store_location=store_location if role == "Merchant" else None,
            menu_items=menu_items if role == "Merchant" else None,
            vehicle_info=vehicle_info if role == "Driver" else None,
        )
        # Save role-specific data
        profile.save()
        
        messages.success(request, "Registration successful! Please check your email to activate your profile.")
        return redirect("login")
    
# from django.contrib.auth.views import LoginView

# class UserLoginView(LoginView):
#     template_name = 'customer/login.html'

#     def get_success_url(self):
#         """Redirect users after successful login."""
#         return self.request.GET.get('next', '/')
    
# from django.contrib.auth.views import LoginView

class UserLoginView(View):
    template_name = 'customer/login.html'
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/login.html') 

    # def get_success_url(self):
    #     """Redirect users after successful login."""
    #     return self.request.GET.get('next', '/')
    

class Order(View):
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
        return render(request, 'customer/order_dev.html', context)
    
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
        items = request.POST.getlist('items[]')
        for item in items:
            menu_item =  MenuItem.objects.get(pk__contains=int(item))
            item_data = {'id': menu_item.pk, 
                         'name': menu_item.name, 
                         'price': menu_item.price}
            
            order_items['items'].append(item_data)

        price = 0
        item_ids =[]
        for item in order_items['items']:
            price += item['price']
            item_ids.append(item['id'])
            

        order = OrderModel.objects.create(price=price, name=name, email=email, street=street, city=city, state=state, zip_code=zip_code
        )
        order.items.add(*item_ids)


        body = ('Thank you for your order! Your food is being prepared and will be delivered soon!\n'
                f'Your total price: ${price}\n'
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
            'price': price
        }

        return redirect('order-confirmation', pk=order.pk)

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
        print(request.body)
        data = json.loads(request.body)
        if data['isPaid']:
            order = OrderModel.objects.get(pk=pk)
            order.is_paid = True 
            order.save()
        return redirect('payment-submitted')

class OrderPayConfirmation(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/order_pay_confirmation.html')

class ShoppingCart(View):
    def get(self, request, *args, **kwargs):
            # shopping_cart_model = get_object_or_404(ShoppingCartModel, customer=request.user)

            return render(request, 'customer/shopping_cart.html')
    

    
