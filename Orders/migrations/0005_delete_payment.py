# Generated by Django 4.1.1 on 2023-02-01 23:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Orders', '0004_remove_orderbook_email_address_order_email_address'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Payment',
        ),
    ]