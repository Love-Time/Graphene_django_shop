from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
User = get_user_model()

class Category(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(null=True, blank=True, verbose_name="Описание")

class Product(models.Model):
    title = models.CharField(max_length=100, verbose_name="Товар")
    description = models.TextField(null=True, blank=True, verbose_name="Описание")
    price = models.PositiveIntegerField(verbose_name="Цена")
    image = models.ImageField(upload_to="product/image/%Y/%m/",null=True, blank=True, verbose_name="Изображение")
    category = models.ForeignKey(Category, blank=True, null=True, verbose_name="Категория", on_delete=models.SET_NULL, related_name="products")

class OrderProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey("Order", on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    count = models.PositiveIntegerField()


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ManyToManyField(Product, related_name='order', through=OrderProduct)

