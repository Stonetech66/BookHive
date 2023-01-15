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
    image=models.CharField(max_length=250, null=True, blank=True)
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
       return  None



class Rating(models.Model):
    user=models.ForeignKey(User, related_name='ratings', on_delete=models.CASCADE)
    book=models.ForeignKey(Book, related_name='ratings', on_delete=models.CASCADE)
    rating=models.IntegerField(default=0)
    review=models.TextField(null=True, blank=True)
    date_created=models.DateTimeField(auto_now_add=True)



