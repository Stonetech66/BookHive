import graphene
from graphql import GraphQLError
from graphene_django import DjangoObjectType
from .models import OrderBook, Order, Book
from django.shortcuts import get_object_or_404
from Shipments.models import Address

class OrderBookType(DjangoObjectType):
    total_price=graphene.FloatField(source='total_price')
    class Meta:
        model=OrderBook
        interfaces=(graphene.relay.Node,)


    



class OrderType(DjangoObjectType):
    sub_total_price=graphene.FloatFIeld(source='sub_total_price')
    class Meta:
        model=Order
        fields=['order_type', 'sub_total_price', ]
        interfaces=(graphene.relay.Node,)
        exclude=('payments')




class AddBookToCart(graphene.Mutation):
    class Arguments:
        qty=graphene.Int(required=True)
        id=graphene.ID()


    def mutate(root, info, qty, id):
        try:
            book=get_object_or_404(Book, id=id)
            o, created=OrderBook.objects.get_or_create(book=book, completed=False)
            Order=Order.objects.get_or_create(completed=False)
            o.qty=qty
            o.save()
            Order.order_book.add(o)
            Order.save()
        except Exception as e:
            raise GraphQLError(e)

        return  AddBookToCart(success=True, failed=False)

class RemoveBook(graphene.Mutation):
    class Arguments:
        id=graphene.ID()

    success=graphene.Boolean()
    def mutate(root, info, qty, id):  
        try:
            book=get_object_or_404(Book, id=id)
            o=OrderBook.objects.get(book=book, completed=False)
            o.delete()
            o.save()
        except Exception as e:
            raise GraphQLError(e)

        return  RemoveBook(success=True)

class ClearCart(graphene.Mutation):
    response=graphene.String()

    def mutate(root, info):
        cart=Order.objects.get(user=info.context.user)
        cart.order_book =None
        cart.save()
        return ClearCart(response="cart cleared")


class Checkout(graphene.Mutation):
    class Arguments:
        pass
    payment_url=graphene.String()
    amount_to_be_charged=graphene.Float()
    def mutate(root, info):
        o=Order.objects.get(user=info.context.user, ordered=False)
        charge=o.get_total_price()
        return Checkout(payment_url="https://", amount_to_be_charged=charge)
    




class Mutations(graphene.Mutation):
    add_book=AddBookToCart.Field()
    remove_book=RemoveBook.Field()
    clear_cart=ClearCart.Field()
    checkout=Checkout.Field()



class Query(graphene.ObjectType):
    cart=graphene.relay.Node(OrderType)
    order_history=graphene.ConnectionField(OrderType)

    def resolve_cart(root, info):
        o, created= Order.objects.prefetch_related("order_book").get_or_create(user=info.context.user, completed=False)
        return o
    def resolve_order_history(root, info):
        return Order.objects.get(user=info.context.user, completed=True)