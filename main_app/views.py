from django.contrib.auth import authenticate
from django.shortcuts import render, redirect, get_object_or_404
from pyexpat.errors import messages
from django.contrib import messages
from django.contrib.auth import login, logout
from .models import Seller, Product
from django.contrib.auth.models import User

def product_add_page(request):
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
def home_page(request):
    return render(request, 'index.html')

def profile_page(request):
    return render(request, 'profile_page.html')

def login_page(request):
    if request.user.is_authenticated:
        return redirect("profile_page")

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
        return redirect("profile_page")

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


def product_detail_empty(request):
    return redirect('product_list_page')