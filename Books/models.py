from django.db import models
from Users.models import User
import uuid

_type=[
    ("e-book", "e-book"), 
    ("hard-book", "hard-book")
]
class Category(models.Model):
    name=models.CharField(unique=True, max_length=250)

    def clean(self):
        if Category.objects.filter(name__iexact=self.name).exists:
            raise ValueError({'name':'category with this name already exists'})
        return False


class Book(models.Model):
    id=models.UUIDField(editable=False, default=uuid.uuid4, primary_key=True)
    author=models.ForeignKey(User, related_name='books', null=True, on_delete=models.SET_NULL)
    title=models.CharField(max_length=250)
    image=models.ImageField()
    description=models.TextField()
    price=models.FloatField(null=True, blank=True)
    discount_price=models.FloatField(null=True, blank=True)
    is_free=models.BooleanField(default=False)
    category=models.ManyToManyField(Category, related_name='books')
    _type=models.CharField(choices=_type, max_length=250)
    date_uploaded=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def rating(self):
        pass





