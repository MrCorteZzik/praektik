from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('login/', views.login_page, name='login_page'),
    path('profile/', views.not_authenticated_profile_page, name='not_authenticated_profile_page'),
    path('profile/<int:user_id>/', views.profile_page, name='profile_page'),
    path('registration/', views.registration_page, name='registration_page'),
    path("logout/", views.logout_page, name="logout"),
    path("seller/product-add/", views.product_add_page, name="product_add_page"),
    path("product-list/", views.product_list_page, name="product_list_page"),
    path("product-detail/<int:product_id>/", views.product_detail, name="product_detail_page"),
    path('cart/', views.cart_page, name='cart_page'),
    path('cart/add/<int:product_id>', views.product_add_to_cart, name='product_add_to_cart'),
    path('cart/remove/<int:product_id>', views.product_remove_from_cart, name='product_remove_from_cart'),
    path('cart/remove-one/<int:product_id>', views.product_remove_one_from_cart, name='product_remove_one_from_cart'),
    path('cart/add-one/<int:product_id>', views.product_add_one_to_cart, name='product_add_one_to_cart'),
    path('cart/order/', views.order_page, name='order_page'),
    path('cart/order/success/<int:order_id>', views.order_success_page, name='order_success_page'),
    path('seller/<int:seller_id>/', views.seller_page, name='seller_page'),
    path('seller/product-edit/<int:product_id>/', views.product_edit_page, name='product_edit_page'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)