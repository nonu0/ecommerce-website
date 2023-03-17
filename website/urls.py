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
    path('services',ServicesView.as_view(),name='services'),
    path('checkout',CheckoutView.as_view(),name='checkout'),
]