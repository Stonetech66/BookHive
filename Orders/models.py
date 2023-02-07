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
    completed=models.BooleanField(default=False)
    order=models.ForeignKey('Order', related_name='order_book', on_delete=models.CASCADE,null=True)

    def total_price(self):
        if not self.book.price:
            total= 0
        else:
            total= self.book.price * self.qty
        if self.book.discount_price:
            total=self.book.discount_price *self.qty
        return total

class Order(models.Model):
    id=models.UUIDField(editable=False, default=uuid.uuid4, primary_key=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart')
    completed=models.BooleanField(default=False)
    in_transit=models.BooleanField(default=False)
    delivered=models.BooleanField(default=False)
    date_created=models.DateTimeField(auto_now_add=True)
    email_address=models.EmailField(null=True, blank=True)
    address=models.ForeignKey(Address, related_name='order', on_delete=models.SET_NULL, null=True)

    def sub_total_price(self):
        total=0
        for i in self.order_book.all():
            total += i.total_price()
        return total

    def e_books(self):
        x=self.order_book.select_related("book").filter(book__book_type='e_book')
        if x.exists():
            return x
        return []
    
    def hard_copies(self):
        x=self.order_book.select_related("book").filter(book__book_type='hard_copy')
        if x.exists():
            return x
        return []
            
