from django.shortcuts import render
from django.views.generic import TemplateView 
# Create your views here.

class HomeView(TemplateView):
    template_name = 'index.html'


class CartView(TemplateView):
    template_name = 'cart.html'


class BlogView(TemplateView):
    template_name = 'blog.html'


class ContactView(TemplateView):
    template_name = 'contact.html'


class ShopView(TemplateView):
    template_name = 'shop.html'


class ServicesView(TemplateView):
    template_name = 'services.html'


class CheckoutView(TemplateView):
    template_name = 'checkout.html'


class AboutView(TemplateView):
    template_name = 'about.html'