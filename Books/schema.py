import graphene
from graphene_django import DjangoObjectType
from .models import Book

class BookType(DjangoObjectType):
    class Meta:
        model=Book 
        fields=("id", "title", "description", "image", "is_free", "price", "discount_price", "author", "category", "_type")

class Query(graphene.ObjectType):
    all_books=graphene.List(BookType)
    get_book=graphene.Field(BookType)
     
    def resolve_all_books(root, info):
        return Book.objects.all()
    def resolve_get_book(root, info, id):
        return Book.objects.prefetch_related("category").select_related("author").get(id=id)

schema=graphene.Schema(query=Query)