import graphene
from .models import Address
from Orders.models import OrderBook, Order
from django.core.validators import validate_email
from graphql import GraphQLError
from graphql_jwt.decorators import login_required

class AddEmailAddress(graphene.Mutation):
    class Arguments:
        id=graphene.ID(required=True, description='id of the orderbook')
        emails=graphene.List(graphene.String)
    success=graphene.Boolean()
    
    def mutate(root, info, id, emails):
        try:
            for i in emails:
                validate_email(i)
        except:
            raise GraphQLError('invalid email provided')

        o=OrderBook.objects.select_related("book__book_type").get(id=id, user=info.context.user, completed=False)
        if o.book.book_type != "e_book" or o.qty != emails:
            raise Exception("invalid number of email provided")
        o.emails={"emails":emails}
        o.save()
        return AddEmailAddress(success=True)


class AddShippingAddress(graphene.Mutation):
    class Arguments:
        address=graphene.String(required=True)
        country=graphene.String(required=True)
        zip_code=graphene.String(required=True)
    success=graphene.Boolean()
    
    def mutate(root, info, address, zip_code, country):
        o=Order.objects.prefetch_related("order_book").get(user=info.context.user, completed=False)
        if not o.order_book.filter(book__book_type='hard_copy').exists():
            raise Exception("no hard-copy book to deliver")
        add=Address.objects.create(user=info.context.user, zip_code=zip_code, country=country, address=address)
        o.address=add
        o.save()
        return AddShippingAddress(success=True)


class Mutation(graphene.ObjectType):
    add_email_address=AddEmailAddress.Field()
    add_shipping_address=AddShippingAddress.Field()