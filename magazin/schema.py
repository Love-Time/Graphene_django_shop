import base64

import graphene
from django import forms
from django.core.files.base import ContentFile
from graphene import Field
from graphene_django import DjangoObjectType
from graphene_file_upload.scalars import Upload
from graphql import GraphQLError

from .models import Category, Product
from .serializers import ProductSerializer



class UnauthorisedAccessError(GraphQLError):
    def __init__(self, message, *args, **kwargs):
        super(UnauthorisedAccessError, self).__init__(message, *args, **kwargs)


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ("id", "title", 'description', "products")


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('title', 'description', 'price', 'image', 'category')


class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = ('id', 'title', 'description', 'price', 'image', 'category')


class CreateProductMutation(graphene.Mutation):
    product = Field(ProductType)

    class Arguments:
        title = graphene.String(required=True)
        description = graphene.String(required=True)
        price = graphene.Int(required=True)
        category = graphene.Int(required=True)
        image = Upload()

    @classmethod
    def mutate(cls, root, info, **kwargs):
        if not info.context.user.is_staff:
            raise UnauthorisedAccessError(message="ИДИ НАХУЙ, тебе нельзя это делать")
        format, imgstr = kwargs['image'].split(';base64,')
        ext = format.split('/')[-1]
        kwargs['image'] = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)  # You can save this as file ins

        serializer = ProductSerializer(data=kwargs)
        if serializer.is_valid():
            data = serializer.save()
            return CreateProductMutation(product=data)
        return None


class Query(graphene.ObjectType):
    all_products = graphene.List(ProductType)
    all_categories = graphene.List(CategoryType)
    category_by_id = graphene.Field(CategoryType, id=graphene.Int(required=True))
    product_by_id = graphene.Field(ProductType, id=graphene.Int(required=True))
    products_by_ids = graphene.List(ProductType, ids=graphene.JSONString(required=True))

    def resolve_all_products(self, info):
        return Product.objects.select_related("category").all()

    def resolve_all_categories(self, info):
        return Category.objects.all().prefetch_related('products')

    def resolve_category_by_id(self, info, id):
        try:
            return Category.objects.get(id=id)
        except Category.DoesNotExist:
            return None

    def resolve_product_by_id(self, info, id):
        try:
            return Product.objects.get(id=id)
        except Product.DoesNotExist:
            return None

    def resolve_products_by_ids(self, info, ids):
        return Product.objects.filter(id__in=ids)


class Mutation(graphene.ObjectType):
    create_product = CreateProductMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
