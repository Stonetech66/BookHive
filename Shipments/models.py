from django.db import models 

class Address(models.Model):
    country=models.CharField(max_length=250)
    state=models.CharField(max_length=250)
    zip_code=models.CharField(max_length=250)
    