from django.db import models
from Users.models import User
from Orders.models import Order
import uuid
class Payment(models.Model):
    id=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    ref_code=models.CharField(max_length=250)
    user=models.ForeignKey(User, related_name='payments', on_delete=models.CASCADE)
    order=models.OneToOneField(Order, related_name='payment', on_delete=models.CASCADE)
    amount=models.FloatField()
    date_created=models.DateTimeField(auto_now_add=True)