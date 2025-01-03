# import django
# from allauth.account import forms

# class CustomSignupForm(forms.SignupForm):
#     ROLE_CHOICES = [
#         ('Customer', 'Customer'),
#         ('Merchant', 'Merchant'),
#         ('Driver', 'Driver'),
#     ]
#     role = django.forms.ChoiceField(choices=ROLE_CHOICES, required=True, label="Role")

#     def save(self, request):
#         user = super().save(request)
#         role = self.cleaned_data['role']
#         # Create a profile with the selected role
#         from customer.models import Profile, ShoppingCartModel
#         profile = Profile.objects.create(user=user, role=role)
#         if role == 'Customer':
#             ShoppingCartModel.objects.create(customer=user)
#         elif role == 'Merchant':
#             # Optional: Create an empty menu or placeholder for merchant
#             profile.menu_items = "[]"
#         profile.save()
#         return user

from django import forms

class CustomSignupForm(forms.Form):  # Do not inherit SignupForm directly
    ROLE_CHOICES = [
        ('Customer', 'Customer'),
        ('Merchant', 'Merchant'),
        ('Driver', 'Driver'),
    ]
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True, label="Role")

    def signup(self, request, user):
        """
        This method is called after the user object is created.
        Delayed import prevents circular import issues.
        """
        from allauth.account.forms import SignupForm  # Import locally
        role = self.cleaned_data['role']
        from customer.models import Profile
        profile = Profile.objects.create(user=user, role=role)
        profile.save()
        return profile 