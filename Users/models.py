from django.db import models
# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Permission
import uuid
from django.contrib import auth
from django.core.exceptions import PermissionDenied

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, password, first_name:str=None, last_name:str=None,):

        if not email:
            raise TypeError("Users must have an email")
        
        # if not first_name:
        #     raise TypeError("Users must have a Firstname")
        
        # if not last_name:
        #     raise TypeError("Users must have a lastname")
        
        user= self.model(email=self.normalize_email(email), first_name= first_name, last_name=last_name)
        user.set_password(password)
        user.save(using=self.db)
        return user


    def create_superuser(self, email, password,first_name:str=None, last_name:str=None, ):

        user=self.create_user(email=email, password=password, first_name=first_name, last_name=last_name)
        user.is_superuser=True
        user.is_staff= True
        user.save(using=self.db)
        
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email=models.EmailField(unique=True, max_length=255)
    first_name= models.CharField(max_length=100, null=True)
    last_name=models.CharField(max_length=100, null=True)
    id= models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    is_active= models.BooleanField(default=True)
    is_staff= models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)
    objects= UserManager()
    USERNAME_FIELD="email"

    @property
    def fullname(self):
        return f"{self.first_name} {self.last_name}"
    
    def __str__(self):
        return self.email


