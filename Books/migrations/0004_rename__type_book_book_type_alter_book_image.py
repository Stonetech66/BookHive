# Generated by Django 4.1.1 on 2023-01-09 23:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Books', '0003_book_book_url_book_user_alter_book_author_orderbook_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='_type',
            new_name='book_type',
        ),
        migrations.AlterField(
            model_name='book',
            name='image',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]
