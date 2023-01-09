from django.db import models
from Users.models import User
import uuid
from django.core.exceptions import ValidationError

_type=[
    ("e-book", "e-book"), 
    ("hard-book", "hard-book")
]
class Category(models.Model):
    name=models.CharField(unique=True, max_length=250)

    def clean(self):
        if Category.objects.filter(name__iexact=self.name):
            raise ValidationError("Category already exists")


class Book(models.Model):
    id=models.UUIDField(editable=False, default=uuid.uuid4, primary_key=True)
    user=models.ForeignKey(User, related_name='books', null=True, on_delete=models.SET_NULL)
    author=models.CharField(max_length=250)
    title=models.CharField(max_length=250)
    image=models.ImageField(blank=True)
    description=models.TextField()
    price=models.FloatField(null=True, blank=True)
    discount_price=models.FloatField(null=True, blank=True)
    is_free=models.BooleanField(default=False)
    book_url=models.URLField(null=True, blank=True)
    category=models.ManyToManyField(Category, related_name='books')
    book_type=models.CharField(choices=_type, max_length=250)
    date_uploaded=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def rating(self):
        pass

class OrderBook(models.Model):
    id=models.UUIDField(editable=False, default=uuid.uuid4, primary_key=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='book_order')
    book=models.ForeignKey(Book, on_delete=models.CASCADE, related_name='orders')
    qty=models.IntegerField(default=1)
    date_created=models.DateTimeField(auto_now_add=True)
    completed=models.BooleanField(default=False)

    def sub_total_price(self):
        total=self.book.price
        if self.book.discount_price:
            total=self.book.discount_price
        return total

class Order(models.Model):
    id=models.UUIDField(editable=False, default=uuid.uuid4, primary_key=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart')
    completed=models.BooleanField(default=False)
    order_book=models.ManyToManyField(OrderBook, related_name='order')
    date_created=models.DateTimeField(auto_now_add=True)






