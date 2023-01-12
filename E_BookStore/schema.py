import graphene
from graphene_django import DjangoObjectType
from Books.schema import Query as Book_querys, Mutations as Book_mutations
class Mutations(Book_mutations,graphene.ObjectType):
    pass

class Query(Book_querys,graphene.ObjectType):
    pass


schema=graphene.Schema(query=Query, mutation=Mutations)