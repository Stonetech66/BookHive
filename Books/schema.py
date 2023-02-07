import graphene
from graphene_file_upload.scalars import Upload
from graphene_django import DjangoObjectType
from .models import Book, Genre, Rating
from graphql_jwt.decorators import login_required
from Users.models import User
from graphql import GraphQLError
from django.db.models import Avg
from graphene_django.filter import DjangoFilterConnectionField
from utils import validate_book, validate_image, upload_to_s3
from graphql_relay import from_global_id
from graphene import relay
from django.core.exceptions import PermissionDenied



class BookNode(DjangoObjectType):
    rating=graphene.Float()
    class Meta:
        model=Book 
        filter_fields=("title", "author", "genre", "book_type", "is_free")
        interfaces=(graphene.relay.Node,)

    
    def resolve_rating(root, info):
        x=root.ratings.aggregate(Avg('rating'))
        return  x['rating__avg']



class UserType(DjangoObjectType):
    class Meta:
        model=User
        exclude=("password",)

class GenreNode(DjangoObjectType):
    class Meta:
        model=Genre
        filter_fields=["name", "books"]
        interfaces=(graphene.relay.Node,)
    
 


class Query(graphene.ObjectType):
    books=DjangoFilterConnectionField(BookNode)
    book=graphene.relay.Node.Field(BookNode)
    genre=graphene.relay.Node.Field(GenreNode)
    genres=DjangoFilterConnectionField(GenreNode)

    def resolve_books(root, info):
        return Book.objects.all().select_related("user").prefetch_related("genre")



class booktype(graphene.Enum):
    e_book="e-book"
    hard_copy="hard-copy"

class CreateBook(graphene.Mutation):
    class Arguments:
        author=graphene.String(required=True)
        title=graphene.String(required=True)
        description=graphene.String(required=True)
        genre=graphene.List(graphene.ID)
        image=Upload(required=True)
        book_file=Upload()
        free=graphene.Boolean(required=True)
        price=graphene.Float()
        discount_price=graphene.Float()
        booktype=booktype()

    book=graphene.Field(BookNode)
    @login_required
    def mutate(root, info,image, price=None, discount_price=None,book_file=None, **kwargs):
        try:
            c=[]
            for i in kwargs['genre']:
                    c.append(Genre.objects.get(id=i))
            if book_file:
                if not validate_book(book_file):
                    raise GraphQLError('invalid book file')
                book_url=upload_to_s3(book_file)
                if not book_url:
                    raise GraphQLError('Failed to upload file')
            else:
                book_url=None
            if not validate_image(image):
                raise GraphQLError('invalid image')
            image_url=upload_to_s3(image)
            if not image_url:
                raise GraphQLError('Failed to upload image')
            book=Book.objects.create(author=kwargs['author'], title=kwargs['title'], 
            description=kwargs['description'],is_free=kwargs['free'], 
            price=price, discount_price=discount_price,
            book_type=kwargs['booktype'], book_url=book_url, image=image_url, user=info.context.user)
            book.genre.set(c)
            book.save()
        except Exception as e:
            raise GraphQLError(e)
        return CreateBook(book=book)


class UpdateBook(relay.ClientIDMutation):
    class Input:
        id=graphene.ID()
        author=graphene.String()
        title=graphene.String()
        description=graphene.String()
        genre=graphene.List(graphene.ID)
        free=graphene.Boolean()
        price=graphene.Float()
        book_file=Upload()
        image=Upload()
        discount_price=graphene.Float()
        booktype=booktype()
    book=graphene.Field(BookNode)
    @login_required
    def mutate_and_get_payload(root, info,id, author, title, description,booktype, free, book_file=None, image=None,price=None, genre=None ,discount_price=None, ):
        try:
            book=Book.objects.get(id=from_global_id(id)[1]) 
            user=info.context.user
            if not  user== book.user :
                raise GraphQLError('You are not authorized to this')
            if book_file:
                if not validate_book(book_file):
                    raise GraphQLError('invalid book file')
                book_url=upload_to_s3(book_file)
                if not book_url:
                    raise GraphQLError('Failed to upload file')
                book.book_url=book_url
            if image:
                if not validate_image(image):
                    raise GraphQLError('invalid image')
                image_url=upload_to_s3(image)
                if not image_url:
                    raise GraphQLError('failed to upload image')
                book.image=image_url
            c=[]
            if genre:
                for i in genre:
                    c.append(Genre.objects.get(id=i))
                book.set(c)
            book.author=author
            book.title=title
            book.description=description
            book.is_free=free
            book.price=price
            book.discount_price=discount_price
            book.book_type=booktype
            book.save()
            return UpdateBook(book=book)
        except Exception as e:
            raise GraphQLError(e)


class DeleteBook(relay.ClientIDMutation):
    class Input:
        id=graphene.ID()

    success=graphene.Boolean()

    @login_required
    def mutate_and_get_payload(root, info, id):
        try:
            book=Book.objects.get(id=from_global_id(id)[1])
            if not info.context.user == book.user:
                raise GraphQLError('Permission denied')
            book.delete()
            book.save()
        except Exception as e:
            raise GraphQLError("book does not exists")
        return DeleteBook(success=True)

class RateBook(relay.ClientIDMutation):
    class Input:
        id=graphene.ID(required=True)
        rating=graphene.Int(required=True)
        review=graphene.String(required=True)
    success=graphene.Boolean()
    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **kwargs):
        try:
            book=Book.objects.get(id=from_global_id(kwargs['id'])[1])
        except Exception as e:
            raise GraphQLError(e)
            if kwargs['rating'] > 5:
                raise GraphQLError("rating can't be greater than 5")
        try:
            Rating.objects.create(user=info.context.user, book=book, rating=kwargs['rating'], review=kwargs['review'])
            return RateBook(success=True)  
        except :
            raise GraphQLError("you can't rate a book more than once")




class Mutations(graphene.ObjectType):
    create_book=CreateBook.Field()
    update_book=UpdateBook.Field()
    delete_book=DeleteBook.Field()
    rate_book=RateBook.Field()



