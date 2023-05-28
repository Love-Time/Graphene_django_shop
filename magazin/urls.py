from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from graphene_file_upload.django import FileUploadGraphQLView
from rest_framework import routers

from magazin.schema import schema
from magazin.views import ProductViewSet, CategoryViewSet, OrderViewSet

router = routers.DefaultRouter()
router.register(r'product', ProductViewSet)
router.register(r'category', CategoryViewSet)
router.register(r'order', OrderViewSet)



urlpatterns = [
    path('api/v1/', include(router.urls)),
    path("graphql", csrf_exempt(FileUploadGraphQLView.as_view(graphiql=True, schema=schema)))

]

