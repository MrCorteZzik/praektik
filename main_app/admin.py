from django.contrib import admin
from .models import Product, Seller
from django.contrib.auth.admin import UserAdmin

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'category', 'image', 'price', 'stock', 'created_at', 'seller')
    list_filter = ('category', 'created_at')
    search_fields = ('id', 'name')

@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'is_seller')
    search_fields = ('id', 'user')

