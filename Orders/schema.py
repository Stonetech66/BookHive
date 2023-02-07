import graphene
from graphql import GraphQLError
from graphene_django import DjangoObjectType, DjangoConnectionField
from .models import OrderBook, Order, Book
from django.shortcuts import get_object_or_404
from Shipments.models import Address
from graphql_jwt.decorators import login_required
from graphene import relay
from graphql_relay import from_global_id
# from django.db.transaction import 
class OrderBookType(DjangoObjectType):
    total_price=graphene.Float(source='total_price')
    class Meta:
        model=OrderBook
        interfaces=(relay.Node,)


    



class OrderType(DjangoObjectType):
    sub_total_price=graphene.Float(source='sub_total_price')
    e_books=graphene.List(OrderBookType, source='e_books')
    hard_copies=graphene.List(OrderBookType, source='hard_copies')
    class Meta:
        model=Order
        interfaces=(relay.Node,)
        exclude=('payment',)
    






class AddBookToCart(relay.ClientIDMutation):
    class Input:
        qty=graphene.Int(required=True)
        id=graphene.ID()

    success=graphene.Boolean()
    @login_required
    def mutate_and_get_payload(root, info, qty, id):
        try:
            book=Book.objects.get(id=from_global_id(id)[1])
            o, created=OrderBook.objects.get_or_create(book=book, completed=False, user=info.context.user)
            order, created=Order.objects.get_or_create(completed=False, user=info.context.user)
            o.qty=qty
            o.order=order
            o.save()
        except Exception as e:
            raise GraphQLError(e)

        return  AddBookToCart(success=True)

class RemoveBook(relay.ClientIDMutation):
    class Input:
        id=graphene.ID()

    success=graphene.Boolean()
    @login_required
    def mutate_and_get_payload(root, info, id):  
        try:
            book=Book.objects.get(id=from_global_id(id)[1])
            o=OrderBook.objects.get(book=book, completed=False, user=info.context.user)
            o.delete()
            o.save()
        except Exception as e:
            raise GraphQLError(e)
 
        return  RemoveBook(success=True)

class ClearCart(graphene.Mutation):
    success=graphene.Boolean()

    @login_required
    def mutate(root, info):
        try:
            cart=Order.objects.get(user=info.context.user, completed=False)
            cart.order_book.delete()
            cart.save()
            return ClearCart(success=True)
        except Exception as e:
            raise GraphQLError(e)



class Mutations(graphene.ObjectType):
    add_book_to_cart=AddBookToCart.Field()
    remove_book_from_cart=RemoveBook.Field()
    clear_cart=ClearCart.Field()




class Query(graphene.ObjectType):
    cart=graphene.Field(OrderType)
    order_history=DjangoConnectionField(OrderType)

    @login_required
    def resolve_cart(root, info):
        o, created= Order.objects.prefetch_related("order_book").get_or_create(user=info.context.user, completed=False)
        return o
    @login_required
    def resolve_order_history(root, info):
            return Order.objects.filter(user=info.context.user, completed=True)