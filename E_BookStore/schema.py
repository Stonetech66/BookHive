import graphene
from graphene_django import DjangoObjectType
import graphql_jwt
from Books.schema import Query as Book_query, Mutations as Book_mutation
from Orders.schema import Query as Order_query, Mutations as Order_mutation
from Shipments.schema import Mutation as Shipment_mutation
from Users.schema import Mutations as User_mutation, Query as User_query


class Mutations(Book_mutation,Order_mutation,Shipment_mutation,User_mutation,graphene.ObjectType):
    login=graphql_jwt.ObtainJSONWebToken.Field()
    refresh_token=graphql_jwt.Refresh.Field()
    verify_token=graphql_jwt.Verify.Field()


class Query(Book_query,Order_query,User_query,graphene.ObjectType):
    pass


schema=graphene.Schema(query=Query, mutation=Mutations)