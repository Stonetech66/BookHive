from graphql_jwt.decorators import login_required
import graphene
from Orders.models import Order
from Shipments.models import Address
from graphql.error import GraphQLError
from django.conf import settings
import requests
from .tasks import get_book_from_s3
class Checkout(graphene.Mutation):
    class Arguments:
        email_address=graphene.String(required=True)
        shipping_address=graphene.String()
        country=graphene.String()
        zip_code=graphene.String()
        state=graphene.String()
    payment_url=graphene.String()
    amount_to_be_charged=graphene.Float()

    @login_required
    def mutate(root, info, email_address=None, shipping_address=None, country=None, zip_code=None, state=None):
        try:
            o=Order.objects.get(user=info.context.user, completed=False)
        except:
            raise GraphQLError("Your cart is empty")
        print(o.email_address)
        if o.e_books() !=[]:
            if not email_address:
                raise GraphQLError('You are to provide an email address to deliver your e-books')
            else:
                o.email_address=email_address
        if  o.hard_copies() !=[] :
            if None in [shipping_address, country, zip_code, state]:
                raise GraphQLError('You are to provide a shipping address for the hard copy books')
            else:
                    address=Address.objects.create(user=info.context.user, state=state, zip_code=zip_code, address=shipping_address, country=country)
                    o.address=address
                    
        o.save()
        charge=o.sub_total_price()
        url='https://api.paystack.co/transaction/initialize'
        header={'authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}'}
        try:

            resp=requests.post(url, timeout=100, headers=header, json={'amount':charge*100, 'email':email_address, 'metadata':{'order_id':o.id, 'price':charge,'email':email_address, },})
            return Checkout(payment_url=resp.json(), amount_to_be_charged=charge)
        except Exception as e:
                    raise GraphQLError(e)
        

    



class Mutation(graphene.ObjectType):
    checkout=Checkout.Field()
