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