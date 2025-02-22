from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('login/', views.login_page, name='login_page'),
    path('profile/', views.profile_page, name='profile_page'),
    path('registration/', views.registration_page, name='registration_page'),
    path("logout/", views.logout_page, name="logout"),
    path("product-add/", views.product_add_page, name="product_add_page"),
    path("product-list/", views.product_list_page, name="product_list_page"),
    path("product-detail/<int:product_id>/", views.product_detail, name="product_detail_page"),
    path('product-detail/', views.product_detail_empty, name='product_detail_empty'),
]