import graphene
from .models import Address
from Orders.models import OrderBook


class AddEmailAddress(graphene.Mutation):
    class Arguments:
        id=graphene.ID(required=True)
        email=graphene.String(required=True)
    
    response=graphene.String()
    
    def mutate(root, info, id, email):
        b=OrderBook.objects.get(id=id, user=info.context.user)
        if b.book.book_type != "e_book":
            # raise error
            return "pp"
        b.email=email
        b.save()
        return AddEmailAddress(response="email, added")

class AddShippingAddress(graphene.Mutation):
    class Arguments:
        pass

class UseSameShippingAddress(graphene.Mutation):
    class Arguments:
        pass

class UseSameEmailAddress(graphene.Mutation):
    class Arguments:
        pass

