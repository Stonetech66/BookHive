from django.db import models 
from Users.models import User


class Address(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    country=models.CharField(max_length=250)
    state=models.CharField(max_length=250)
    address=models.CharField(max_length=250)
    zip_code=models.CharField(max_length=250)
    default=models.BooleanField(default=False)
    date_created=models.DateTimeField(auto_now_add=True)
    
    