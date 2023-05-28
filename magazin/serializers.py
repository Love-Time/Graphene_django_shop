from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from magazin.models import Product, Category, OrderProduct, Order


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        exclude = []

class OrderSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    def get_product(self, obj):
        data = list(OrderProduct.objects.filter(order_id=obj.id))
        return OrderProductSerializer(data, many=True).data


    class Meta:
        model = Order
        fields = "__all__"