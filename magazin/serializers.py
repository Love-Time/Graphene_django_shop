from rest_framework.serializers import ModelSerializer

from magazin.models import Product


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        field = "__all__"