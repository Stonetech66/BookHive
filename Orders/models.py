from django.db import models
from Users.models import User
from Books.models import Book
from Shipments.models import Address
import uuid
class OrderBook(models.Model):
    id=models.UUIDField(editable=False, default=uuid.uuid4, primary_key=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='book_order')
    book=models.ForeignKey(Book, on_delete=models.CASCADE, related_name='orders')
    qty=models.IntegerField(default=1)
    date_created=models.DateTimeField(auto_now_add=True)
    email=models.EmailField(null=True, blank=True)
    address=models.JSONField()
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
    in_transit=models.BooleanField(default=False)
    delivered=models.BooleanField(default=False)
    date_created=models.DateTimeField(auto_now_add=True)

    def get_total_price(self):
        total=0
        for i in self.order_book:
            total += i.sub_total_price()
        return total
            