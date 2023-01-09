import graphene
from graphene_django import DjangoObjectType
from .models import Book
from Users.models import User


class BookType(DjangoObjectType):
    class Meta:
        model=Book 


class UserType(DjangoObjectType):
    class Meta:
        model=User
        exclude=("password",)

class Query(graphene.ObjectType):
    books=graphene.List(BookType)
    book=graphene.Field(BookType, id=graphene.String(required=True))
    my_books=graphene.List(BookType)
     
    def resolve_books(root, info):
        return Book.objects.all()
    def resolve_book(root, info, id):
        return Book.objects.prefetch_related("category").select_related("author").get(id=id)
    def resolve_my_books(root, info):
        return Book.objects.filter(user=info.context.user)

class booktype(graphene.Enum):
    e_book="e-book"
    hard_copy="hard-copy"

class BookMutation(graphene.Mutation):
    class Arguments:
        author=graphene.String(required=True)
        title=graphene.String(required=True)
        description=graphene.String(required=True)
        free=graphene.Boolean()
        price=graphene.Float()
        discount_price=graphene.Float()
        booktype=booktype()

    
    book=graphene.Field(BookType)
    # success=graphene.BooleanField()
    # failed=graphene.BooleanField()
    # failure_desciption=None

    @classmethod
    def mutate(cls, root, info, author, title, description, free, price, discount_price, booktype):
            book=Book.objects.create(author='author', title='title', 
            description='description', free='free', 
            price='price', discount_price='discount_price',
            book_type='booktype')
            return BookMutation(book=book)

        

class Mutations(graphene.ObjectType):
    upload_book=BookMutation.Field()




schema=graphene.Schema(query=Query, mutation=Mutations)