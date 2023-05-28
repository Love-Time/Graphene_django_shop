from django.template.loader import render_to_string
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from magazin.models import Product, Category, Order, OrderProduct
from magazin.permissions import IsAdminUserOrReadOnly
from magazin.serializers import ProductSerializer, CategorySerializer, OrderSerializer
from users.service import send_activation_email


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [IsAdminUserOrReadOnly]

    @action(detail=True, methods=['get'])
    def category(self, request, pk=1):
        try:
            pk = int(pk)
        except ValueError:
            return Response({"error": "pk is not in"}, status=status.HTTP_400_BAD_REQUEST)
        queryset = Product.objects.filter(category_id=pk)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [IsAdminUserOrReadOnly]


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def create(self, request, *args, **kwargs):
        print("'fffffffffffffffffff", request.data)
        obj = Order.objects.create(user=request.user)
        ids = [obj['id'] for obj in request.data['data']]
        counts = [obj['count'] for obj in request.data['data']]
        products = Product.objects.filter(id__in = ids)
        data = OrderProduct.objects.bulk_create([OrderProduct(order=obj, count=counts[i] ,product=products[i], price=products[i].price) for i in range(len(products))])
        txt = ""
        price = 0
        for product in data:
            price+=product.price * product.count
            txt += f"{product.product.title} по {product.price} {product.count}шт за {product.price * product.count}\n"


        text_content = 'This is an important message.'
        html_content = render_to_string('mail.html', {'text': f"Заказ оформлен\n{txt}Итого: {price}", })
        send_activation_email(text_content, html_content, request.user.email)




        return Response("aaaa")

