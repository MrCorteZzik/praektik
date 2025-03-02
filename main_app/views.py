from django.contrib.auth import authenticate
from django.shortcuts import render, redirect, get_object_or_404
from pyexpat.errors import messages
from django.contrib import messages
from django.contrib.auth import login, logout
from .models import Seller, Product, CartItem, Order
from django.contrib.auth.models import User

def home_page(request):
    if request.user.is_authenticated:
        if Seller.objects.get(user_id=request.user.id).is_seller:
            return render(request, 'index.html', {'is_seller': True})
        else:
            return render(request, 'index.html', {'is_seller': False})
    else:
        return render(request, 'index.html', {'is_seller': False})

def not_authenticated_profile_page(request):
    return render(request, 'not_authenticated_profile_page.html')

def profile_page(request, user_id):
    return render(request, 'profile_page.html')

def login_page(request):
    if request.user.is_authenticated:
        return redirect("home_page")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home_page")
        else:
            messages.error(request, "Неверный логин или пароль!")

    return render(request, "login_page.html")

def registration_page(request):
    if request.user.is_authenticated:
        return redirect("home_page")

    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")
        is_seller = request.POST.get("is_seller")

        if password != password2:
            messages.error(request, "Пароли не совпадают!")
            return render(request, "registration_page.html")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Пользователь с таким именем уже существует!")
            return render(request, "registration_page.html")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Пользователь с таким email уже существует!")
            return render(request, "registration_page.html")

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        if is_seller == "on":
            seller = Seller.objects.create(user=user, is_seller=True)
            seller.save()
        else:
            seller = Seller.objects.create(user=user, is_seller=False)
            seller.save()

        login(request, user)
        return redirect("home_page")

    return render(request, "registration_page.html")

def logout_page(request):
    logout(request)
    return redirect('home_page')

def product_add_page(request):
    if not request.user.is_authenticated:
        return redirect("login_page")

    user = Seller.objects.get(user_id=request.user.id)
    if not user.is_seller:
        messages.error(request, "Вы не можете добавлять товары!")
        return redirect("home_page")
    else:
        if request.method == "POST":
            name = request.POST.get("name")
            description = request.POST.get("description")
            category = request.POST.get("category")
            price = request.POST.get("price")
            stock = request.POST.get("stock")

            product = Product.objects.create(name=name, description=description, price=price, stock=stock, category=category, seller_id=request.user.id)
            product.save()

            messages.success(request, "Товар успешно добавлен!")
        return render(request, "product_add_page.html")

def product_list_page(request):
    products = Product.objects.all()
    if not request.user.is_authenticated:
        return redirect("login_page")
    else:
        return render(request, 'product_list_page.html', {'products': products})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        return render(request, 'product_detail_page.html', {'product': product})
    else:
        return redirect("login_page")

def cart_page(request):
    if not request.user.is_authenticated:
        return redirect("login_page")

    cart_items = CartItem.objects.filter(user_id=request.user.id, status=True)

    if cart_items.exists():
        return render(request, 'cart_page.html', {'cart_items': cart_items})
    else:
        return render(request, 'cart_page.html', {'cart_items': None})

def product_add_to_cart(request, product_id):
    if not request.user.is_authenticated:
        return redirect("login_page")

    product = get_object_or_404(Product, id=product_id)

    if product.stock == 0:
        messages.error(request, "Недостаточно товара в наличии!")
        return redirect("product_detail_page", product_id=product_id)
    if CartItem.objects.filter(user=request.user, product=product, status=True).exists():
        cart_item = CartItem.objects.filter(user=request.user, product=product, status=True)
        for item in cart_item:
            item.quantity += 1
            item.save()
    else:
        cart_item = CartItem.objects.create(user=request.user, product=product)
        cart_item.save()

    return redirect("cart_page")


def product_remove_from_cart(request, product_id):
    if not request.user.is_authenticated:
        return redirect("login_page")

    product = get_object_or_404(Product, id=product_id)

    cart_item = CartItem.objects.get(user=request.user, product=product, status=True)
    cart_item.delete()

    return redirect("cart_page")

def product_remove_one_from_cart(request, product_id):
    if not request.user.is_authenticated:
        return redirect("login_page")

    product = get_object_or_404(Product, id=product_id)

    cart_item = CartItem.objects.get(user=request.user, product=product, status=True)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect("cart_page")

def product_add_one_to_cart(request, product_id):
    if not request.user.is_authenticated:
        return redirect("login_page")

    product = get_object_or_404(Product, id=product_id)

    cart_item = CartItem.objects.get(user=request.user, product=product, status=True)
    if cart_item.quantity < product.stock:
        cart_item.quantity += 1
        cart_item.save()
    else:
        messages.error(request, "Недостаточно товара в наличии!")

    return redirect("cart_page")

def order_page(request):
    if not request.user.is_authenticated:
        return redirect("login_page")

    if Order.objects.filter(user=request.user, status='created').exists():
        order = Order.objects.get(user=request.user, status='created')
        return render(request, 'order_page.html', {'order': order})
    else:
        order = Order.objects.create(user=request.user)
        CartItem.objects.filter(user=request.user, status=True).update(order=order)
        order.save()
        return render(request, 'order_page.html', {'order': order})


def order_success_page(request, order_id):
    if not request.user.is_authenticated:
        return redirect("login_page")

    order = get_object_or_404(Order, id=order_id)
    order.status = 'in_progress'
    order.save()

    cart_items = CartItem.objects.filter(order=order)

    products = []
    for item in cart_items:
        products.append(item.product)

    for product in products:
        product.stock -= CartItem.objects.get(user=request.user, product=product, status=True).quantity
        product.save()

    CartItem.objects.filter(user=request.user).update(status=False)

    return render(request, 'order_success_page.html', {'order': order})

def seller_page(request, seller_id):
    products = Product.objects.filter(seller_id=Seller.objects.get(user_id=seller_id).id)
    return render(request, 'seller_page.html', {'products': products, 'seller_id': seller_id})

def product_edit_page(request, product_id):
    user = Seller.objects.get(user_id=request.user.id)
    if not user.is_seller:
        messages.error(request, "Вы не можете редактировать товары!")
        return redirect("home_page")
    else:
        product = get_object_or_404(Product, id=product_id)
        if request.method == "POST":
            name = request.POST.get("product_name")
            description = request.POST.get("product_description")
            category = request.POST.get("product_category")
            price = request.POST.get("product_price")
            stock = request.POST.get("product_stock")

            product.name = name
            product.description = description
            product.category = category
            product.price = price
            product.stock = stock
            product.save()

            messages.success(request, "Товар успешно изменен!")
            return redirect("seller_page", seller_id=user.id)
        return render(request, 'product_edit_page.html', {'product': product})