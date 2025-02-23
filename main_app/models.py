from django.contrib.auth.models import User
from django.db import models

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=200)
    category = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/')
    price = models.IntegerField()
    stock = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)

class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_seller = models.BooleanField(default=False)

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    def total_price(self):
        return self.product.price * self.quantity

class Checkout(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart_items = models.ManyToManyField(CartItem)
    def total_price(self):
        return sum(item.total_price() for item in self.cart_items.all())