import graphene
from graphene_django import DjangoObjectType
import graphql_jwt
from Books.schema import Query as Book_querys, Mutations as Book_mutations


class Mutations(Book_mutations,graphene.ObjectType):
    login=graphql_jwt.ObtainJSONWebToken.Field()
    refresh_token=graphql_jwt.Refresh.Field()
    verify_token=graphql_jwt.Verify.Field()


class Query(Book_querys,graphene.ObjectType):
    pass


schema=graphene.Schema(query=Query, mutation=Mutations)