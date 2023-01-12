import graphene
from graphene_django import DjangoObjectType
from .models import Book, Category
from Users.models import User
from graphql import GraphQLError


class BookType(DjangoObjectType):
    rating=graphene.String(source='rating')
    class Meta:
        model=Book 



class UserType(DjangoObjectType):
    class Meta:
        model=User
        exclude=("password",)

class CategoryType(DjangoObjectType):
    class Meta:
        model=Category


class Query(graphene.ObjectType):
    books=graphene.List(BookType)
    book=graphene.Field(BookType, id=graphene.String(required=True))
    my_books=graphene.List(BookType, username=graphene.String(required=True))
    category=graphene.Field(CategoryType, id=graphene.Int(required=True))

     
    def resolve_books(root, info):
        return Book.objects.all()
    def resolve_book(root, info, id):
        return Book.objects.prefetch_related("category").select_related("author").get(id=id)
    def resolve_my_books(root, info, username):
        return Book.objects.filter(user__username=username).prefetch_related("category").select_related("author")
    def resolve_category(root, info, id):
        return Category.objects.get(id=id)


class booktype(graphene.Enum):
    e_book="e-book"
    hard_copy="hard-copy"

class CreateBook(graphene.Mutation):
    class Arguments:
        author=graphene.String(required=True)
        title=graphene.String(required=True)
        description=graphene.String(required=True)
        category=graphene.List(graphene.ID)
        free=graphene.Boolean(default_value=False)
        price=graphene.Float()
        discount_price=graphene.Float()
        booktype=booktype()

    
    book=graphene.Field(BookType)
    def mutate(root, info,image=None, price=None, discount_price=None,  **kwargs):
        try:
            c=[]
            for i in kwargs['category']:
                c.append(Category.objects.get(id=i))
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
        discount_price=graphene.Float()
        booktype=booktype()
    book=graphene.Field(BookType)
    def mutate(root, info,id, author, title, description, category,booktype, free, price=None, discount_price=None, ):
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

    response=graphene.String()

    def mutate(root, info, id):
        book=Book.objects.get(id=id)
        book.delete()
        book.save()
        return DeleteBook(response="Book sucessfuly deleted")

class Mutations(graphene.ObjectType):
    create_book=CreateBook.Field()
    update_book=UpdateBook.Field()
    delete_book=DeleteBook.Field()




