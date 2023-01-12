import graphene
from graphene_file_upload.scalars import Upload
from graphene_django import DjangoObjectType
from .models import Book, Category
from Users.models import User
from graphql import GraphQLError
from graphene_django.filter import DjangoFilterConnectionField
from ..utils import validate_book, validate_image



class BookType(DjangoObjectType):
    rating=graphene.String(source='rating')
    class Meta:
        model=Book 
        filter_fields=("title", "author", "category")
        interfaces=(graphene.relay.Node,)
    
    



class UserType(DjangoObjectType):
    class Meta:
        model=User
        exclude=("password",)

class CategoryType(DjangoObjectType):
    class Meta:
        model=Category
        filter_fields=["name", "books"]
        interface=(graphene.relay.Node)


class Query(graphene.ObjectType):
    books=DjangoFilterConnectionField(BookType)
    book=graphene.relay.Node(BookType)
    categories=DjangoFilterConnectionField(CategoryType)
    category=graphene.relay.Node(CategoryType)

     
    def resolve_books(root, info):
        return Book.objects.all().select_related("author")

    def resolve_book(root, self, id):
        return Book.objects.get(id=id).select_related("author")
    
    def resolve_category(root, info, id):
        return Category.objects.get(id=id).prefetch_related("books")


class booktype(graphene.Enum):
    e_book="e-book"
    hard_copy="hard-copy"

class CreateBook(graphene.Mutation):
    class Arguments:
        author=graphene.String(required=True)
        title=graphene.String(required=True)
        description=graphene.String(required=True)
        category=graphene.List(graphene.ID)
        image=Upload(required=True)
        book_file=Upload()
        free=graphene.Boolean(required=True)
        price=graphene.Float()
        discount_price=graphene.Float()
        booktype=booktype()

    
    book=graphene.Field(BookType)
    def mutate(root, info,image, price=None, discount_price=None,book_file=None, **kwargs):
        try:
            c=[]
            for i in kwargs['category']:
                c.append(Category.objects.get(id=i))
            if book_file:
                if validate_book(book_file):
                    pass
            if validate_image(image):
                #upload image to s3 bucket
                pass
            #Upload in the background make use of s3 bucket
            book=Book.objects.create(author=kwargs['author'], title=kwargs['title'], 
            description=kwargs['description'],is_free=kwargs['free'], 
            price=price, discount_price=discount_price,
            book_type=kwargs['booktype'])
            book.category.set(c)
            book.save()
        except Exception as e:
            #raise exception
                print(e)
        return CreateBook(book=book)


class UpdateBook(graphene.Mutation):
    class Arguments:
        id=graphene.ID
        author=graphene.String()
        title=graphene.String()
        description=graphene.String()
        category=graphene.List(graphene.ID)
        free=graphene.Boolean()
        price=graphene.Float()
        book_file=Upload()
        image=Upload()
        discount_price=graphene.Float()
        booktype=booktype()
    book=graphene.Field(BookType)
    def mutate(root, info,id, author, title, description, category,booktype, free, book_file=None, image=None,price=None, discount_price=None, ):
        book=Book.objects.get(id=id) 
        c=[]
        for i in category:
            c.append(Category.objects.get(id=i))
        book.author=author
        book.title=title
        book.description=description
        book.is_free=free
        book.price=price
        book.discount_price=discount_price
        book.book_type=booktype
        book.set(c)
        book.save()
        return UpdateBook(book=book)


class DeleteBook(graphene.Mutation):
    class Arguments:
        id=graphene.ID()

    success=graphene.Boolean()

    def mutate(root, info, id):
        book=Book.objects.get(id=id)
        book.delete()
        book.save()
        return DeleteBook(success=True)

class Mutations(graphene.ObjectType):
    create_book=CreateBook.Field()
    update_book=UpdateBook.Field()
    delete_book=DeleteBook.Field()




