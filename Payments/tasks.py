# from ..utils import s3
import boto3
from django.conf import settings
from Orders.models import Order
from django.core.mail import  EmailMultiAlternatives
from celery import shared_task
import os
from django.conf import settings
from .models import Payment



@shared_task 
def Create_PaymentRecord(amount, order_id):
    order=Order.objects.get(id=order_id)
    Payment.objects.create(user=order.user, amount=amount)


@shared_task
def get_book_from_s3(order_id, email, fullname):
    order=Order.objects.get(id=order_id)
    text=f"Hello {fullname}. The books you ordered are attached below"
    html=f"<p>Hello {fullname} </p>. The books you ordered are attached below"
    subject="E-book Delivery"
    msg=EmailMultiAlternatives(subject, text, to=[email])
    e_books=order.e_books()
    if not e_books == []:
        for o in e_books():
            # file=s3.get_object(BUCKET=settings.AWS_BUCKET_NAME, Key=o.book.book_file_name )["Body"].read()
            file=os.path.join(settings.BASE_DIR/"k.html")
            msg.attach(f'{o.book.title}.pdf', file)
    msg.attach_alternative(html, "text/html")
    return msg.send(fail_silently=True)



