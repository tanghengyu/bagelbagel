# Generated by Django 5.1.3 on 2025-01-03 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0009_remove_profile_menu_items_cartitem_total_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='init_menu_items',
            field=models.TextField(blank=True, null=True),
        ),
    ]
