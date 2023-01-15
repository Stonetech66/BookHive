from .models import User
from django.core.validators import validate_email
from graphene_django import DjangoObjectType
import graphene
from graphql import GraphQLError
from graphql_jwt.decorators import login_required

class UserType(DjangoObjectType):
    class Meta:
        model=User
        exclude=('password',)






class Signup(graphene.Mutation):
    class Arguments:
        email=graphene.String(required=True)
        first_name=graphene.String(required=True)
        last_name=graphene.String(required=True)
        password=graphene.String(required=True)
    user=graphene.Field(UserType)

    def mutate(root, info, **kwargs):
        try:
            validate_email(kwargs['email'])
        except:
            raise GraphQLError('invalid email')

        user=User(first_name=kwargs['first_name'], last_name=kwargs['last_name'], email=kwargs['email'])
        user.set_password(kwargs['password'])
        user.save()
        return Signup(user=user)

class Query(graphene.ObjectType):
    user_details=graphene.Field(UserType)

    @login_required
    def resolve_user_details(root, info):
        return info.context.user



class Mutations(graphene.ObjectType):
    signup=Signup.Field()


