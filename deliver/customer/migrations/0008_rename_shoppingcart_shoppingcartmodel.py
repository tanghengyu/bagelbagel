# Generated by Django 5.1.3 on 2024-12-16 18:41

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0007_alter_profile_user_alter_shoppingcart_customer'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ShoppingCart',
            new_name='ShoppingCartModel',
        ),
    ]
