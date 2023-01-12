import graphene
from graphene_django import DjangoObjectType
from .models import OrderBook, Order, Book
from django.shortcuts import get_object_or_404

class OrderBookType(DjangoObjectType):
    class Meta:
        model=OrderBook
        exclude=['completed', ]


class OrderType(DjangoObjectType):
    class Meta:
        model=Order
        exclude=["completed", ]



class Query(graphene.ObjectType):
    cart=graphene.Field(OrderType)

    def resolve_cart(root, info):
        return Order.objects.get_or_create(user=info.context.user, completed=False)


class AddBookToCart(graphene.Mutation):
    class Arguments:
        qty=graphene.Int(required=True)
        id=graphene.ID()
    success=graphene.BooleanField()
    error=graphene.BooleanField()
    order=graphene.Field(OrderBookType)

    def mutate(root, info, qty, id):
        book=get_object_or_404(Book, id=id)
        o, created=OrderBook.objects.get_or_create(book=book, completed=False)
        Order=Order.objects.get_or_create(completed=False)
        o.qty=qty
        o.save()
        Order.order_book.add(o)
        Order.save()

        return  AddBookToCart(success=True, failure=False)

class RemoveBook(graphene.Mutation):
    class Arguments:
        id=graphene.ID()
    success=graphene.BooleanField()
    error=graphene.BooleanField()

    def mutate(root, info, qty, id):  
        book=get_object_or_404(Book, id=id)
        o=OrderBook.objects.get(book=book, completed=False)
        Order=Order.objects.get_or_create(completed=False)
        o.delete()
        o.save()

        return  RemoveBook(success=True, failure=False)

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

