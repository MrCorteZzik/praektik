from django.contrib.auth.models import User
from django.db import models

class Product(models.Model):
    Categories = {
        'electronics' : 'Электроника',
        'clothes' : 'Одежда',
        'house_and_garden' : 'Дом и сад',
        'beauty' : 'Красота',
        'sport' : 'Спорт',
        'toys' : 'Игрушки',
        'books' : 'Книги',
        'auto' : 'Авто',
        'all' : 'Все категории',
    }

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=200)
    category = models.CharField(max_length=100, choices=Categories.items(), default='all')
    image = models.ImageField(upload_to='images/')
    price = models.IntegerField()
    stock = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)

class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_seller = models.BooleanField(default=False)

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(default='created', max_length=20)
    def order_total_price(self):
        res = 0
        for item in CartItem.objects.filter(order=self):
            res += item.cart_item_total_price()
        return res

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    status = models.BooleanField(default=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, default=-1)
    def cart_item_total_price(self):
        return self.product.price * self.quantity