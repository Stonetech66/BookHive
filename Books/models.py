from django.db import models
from Users.models import User
import uuid
from django.core.exceptions import ValidationError

_type=[
    ("e_book", "e_book"), 
    ("hard_book", "hard_book")
]
class Genre(models.Model):
    name=models.CharField(unique=True, max_length=250)

    def clean(self):
        if Genre.objects.filter(name__iexact=self.name):
            raise ValidationError("Genre already exists")


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
    book_url=models.CharField(null=True, blank=True, max_length=100)
    book_file_name=models.CharField(null=True, max_length=100)
    genre=models.ManyToManyField(Genre, related_name='books')
    book_type=models.CharField(choices=_type, max_length=250)
    date_uploaded=models.DateTimeField(auto_now_add=True)
    copies_sold=models.IntegerField(default=0)

    def __str__(self):
        return self.title




class Rating(models.Model):
    user=models.ForeignKey(User, related_name='ratings', on_delete=models.CASCADE)
    book=models.ForeignKey(Book, related_name='ratings', on_delete=models.CASCADE)
    rating=models.IntegerField()
    review=models.TextField(null=True, blank=True)
    date_created=models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together= ("user", "book")



