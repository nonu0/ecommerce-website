from django.urls import path
from website.views import *


app_name = 'website'
urlpatterns = [
    path('',HomeView.as_view(),name='home'),
    path('cart',CartView.as_view(),name='cart'),
    path('shop',ShopView.as_view(),name='shop'),
    path('blog',BlogView.as_view(),name='blog'),
    path('contact',ContactView.as_view(),name='contact'),
    path('about',AboutView.as_view(),name='about'),
    path('user_profile',ProfileView.as_view(),name='profile'),
    path('services',ServicesView.as_view(),name='services'),
    path('add_to_cart/<int:pro_id>/',AddToCartView.as_view(), name='add_to_cart'),
    path('checkout',CheckoutView.as_view(),name='checkout'),
    path('product/<slug:slug>/',ProductDetailView.as_view(),name='product'),
    path('manage-cart/<int:prod_id>/',ManageCartView.as_view(),name='managecart'),
    path('emptycart/',EmptyCartView.as_view(),name='emptycart'),

]