from django.shortcuts import render,redirect
from django.views.generic import TemplateView ,ListView,View
from website.models import Cart, Product,CartItem
from django.core.paginator import Paginator
# Create your views here.
class EMixin(object):
    def dispatch(self, request, *args, **kwargs):
        cart_id = self.request.session.get('cart_id', None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            if request.user.is_authenticated and request.user.customer:
                cart_obj.customer = request.user.customer
                cart_obj.save()
        return super().dispatch(request, *args, **kwargs)

class HomeView(TemplateView):
    template_name = 'index.html'


class CartView(TemplateView):
    template_name = 'cart.html'


class BlogView(TemplateView):
    template_name = 'blog.html'


class ContactView(TemplateView):
    template_name = 'contact.html'



class ShopView(EMixin, ListView):
    model = Product
    template_name = 'shop.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_products = Product.objects.all()
        paginator = Paginator(all_products, 12)
        page_number = self.request.GET.get('page')
        product_list = paginator.get_page(page_number)
        context['product_list'] = product_list
        return context



class ProductDetailView(EMixin, TemplateView):
    # model = Product
    template_name = 'product-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url_slug = self.kwargs['slug']
        product = Product.objects.get(slug=url_slug)
        # product.view_count += 1
        product.save()
        context['product'] = product
        return context


class AddToCartView(TemplateView):
    template_name = 'added-to-cart.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get product id
        product_id = self.kwargs['pro_id']
        # get object from id
        product_obj = Product.objects.get(id=product_id)
        # check if there is a cart 
        cart_id = self.request.session.get('cart_id',None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            this_product_in_cart = cart_obj.cartitem_set.filter(
                product=product_obj
            )
            # product already in cart
            if this_product_in_cart.exists():
                cartitem = this_product_in_cart.last()
                cartitem.quantity += 1
                cartitem.rate = product_obj.price
                cartitem.sub_total += product_obj.price
                cartitem.save()

            # product is not in cart
            else:
                cartitem = CartItem.objects.create(
                    cart = cart_obj,rate=product_obj.price,product=product_obj,quantity=1,sub_total=product_obj.price
                )
                cart_obj.total += product_obj.price
                cart_obj.save()

        else:
            cart_obj = Cart.objects.create(total=0)
            self.request.session['cart_id'] = cart_obj.id
            cartitem = CartItem.objects.create(
                cart=cart_obj, rate=product_obj.price, product=product_obj, quantity=1, sub_total=product_obj.price)
            cart_obj.total += product_obj.price
            cart_obj.save()
        return context
    
class CartView(TemplateView):
    template_name = 'cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get('cart_id', None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
        else:
            cart = None
        context['cart'] = cart
        return context
    
class ManageCartView(View):
    def get(self,request,**kwargs):
        product_id = self.kwargs['prod_id']
        action = request.GET.get('action')
        product_obj = CartItem.objects.get(id=product_id)
        cart_obj = product_obj.cart
        if action == 'inc':
            product_obj.quantity += 1
            product_obj.sub_total += product_obj.rate
            product_obj.save()
            cart_obj.total += product_obj.rate
            cart_obj.save()
        elif action == 'dec':
            product_obj.quantity -= 1
            product_obj.sub_total -= product_obj.rate
            product_obj.save()
            cart_obj.total -=product_obj.rate
            cart_obj.save()
            if product_obj.quantity == 0:
                product_obj.delete()
        elif action == 'rmv':
            cart_obj.total -= product_obj.sub_total
            cart_obj.save()
            product_obj.delete()
        else:
            pass
        return redirect('website:cart')


class EmptyCartView(View):
    def get(self,request,**kwargs):
        cart_id = request.session.get('cart_id',None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
            cart.cartitem_set.all().delete()
            cart.total = 0
            cart.save()
            return redirect('website:cart')





class ServicesView(TemplateView):
    template_name = 'services.html'


class CheckoutView(TemplateView):
    template_name = 'checkout.html'


class AboutView(TemplateView):
    template_name = 'about.html'


#     from django.shortcuts import render, redirect
# from django.views.generic import TemplateView, ListView, DetailView, View, CreateView, FormView
# from django.contrib.auth import authenticate, login, logout
# from django.urls import reverse_lazy
# from django.db.models import Q
# from django.core.paginator import Paginator
# from .forms import *
# from .models import *


# # Create your views here.
# class EMixin(object):
#     def dispatch(self, request, *args, **kwargs):
#         cart_id = self.request.session.get('cart_id', None)
#         if cart_id:
#             cart_obj = Cart.objects.get(id=cart_id)
#             if request.user.is_authenticated and request.user.customer:
#                 cart_obj.customer = request.user.customer
#                 cart_obj.save()
#         return super().dispatch(request, *args, **kwargs)


# class HomeView(TemplateView):
#     template_name = 'home.html'

# class AddedToCart(TemplateView):
#     template_name = 'added-to-cart'



# class AllProductsView(EMixin, TemplateView):
#     template_name = 'all-products.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['all_categories'] = Category.objects.all()
#         return context


# class ProductDetailView(EMixin, TemplateView):
#     # model = Product
#     template_name = 'product-detail.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         url_slug = self.kwargs['slug']
#         product = Product.objects.get(slug=url_slug)
#         # product.view_count += 1
#         product.save()
#         context['product'] = product
#         return context


# class AddToCartView(EMixin, TemplateView):
#     template_name = 'added-to-cart.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         #get id
#         item_id = self.kwargs['pro_id']
#         #get object
#         product_obj = Product.objects.get(id=item_id)
#         # #check if cart exist
#         cart_id = self.request.session.get('cart_id', None)
#         if cart_id:
#             cart_obj = Cart.objects.get(id=cart_id)
#             this_product_in_cart = cart_obj.cartitem_set.filter(
#                 product=product_obj)
#             # item already in cart
#             if this_product_in_cart.exists():
#                 cartitem = this_product_in_cart.last()
#                 cartitem.quantity += 1
#                 cartitem.rate = product_obj.price
#                 cartitem.sub_total += product_obj.price
#                 cartitem.save()
#                 cart_obj.total += product_obj.price
#                 cart_obj.save()
#             # new item added in cart
#             else:
#                 cartitem = CartItem.objects.create(
#                     cart=cart_obj, rate=product_obj.price, product=product_obj, quantity=1, sub_total=product_obj.price)
#                 cart_obj.total += product_obj.price
#                 cart_obj.save()
#         else:
#             cart_obj = Cart.objects.create(total=0)
#             self.request.session['cart_id'] = cart_obj.id
#             cartitem = CartItem.objects.create(
#                 cart=cart_obj, rate=product_obj.price, product=product_obj, quantity=1, sub_total=product_obj.price)
#             cart_obj.total += product_obj.price
#             cart_obj.save()
#         return context


# class CartView(EMixin, TemplateView):
#     template_name = 'cart.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         cart_id = self.request.session.get('cart_id', None)
#         if cart_id:
#             cart = Cart.objects.get(id=cart_id)
#         else:
#             cart = None
#         context['cart'] = cart
#         return context


# class ManageCartView(EMixin, View):
#     def get(self, request, **kwargs):
#         print('manage cart view')
#         cp_id = self.kwargs['cp_id']
#         action = request.GET.get('action')
#         print(cp_id, action)
#         cp_obj = CartItem.objects.get(id=cp_id)
#         cart_obj = cp_obj.cart
#         if action == 'inc':
#             cp_obj.quantity += 1
#             cp_obj.sub_total += cp_obj.rate
#             cp_obj.save()
#             cart_obj.total += cp_obj.rate
#             cart_obj.save()
#         elif action == 'dcr':
#             cp_obj.quantity -= 1
#             cp_obj.sub_total -= cp_obj.rate
#             cp_obj.save()
#             cart_obj.total -= cp_obj.rate
#             cart_obj.save()
#             if cp_obj.quantity == 0:
#                 cp_obj.delete()
#         elif action == 'rmv':
#             cart_obj.total -= cp_obj.sub_total
#             cart_obj.save()
#             cp_obj.delete()
#         else:
#             pass
#         return redirect('website:cart')


# class EmptyCartView(EMixin, TemplateView):
#     def get(self, request, *args, **kwargs):
#         cart_id = request.session.get('cart_id', None)
#         if cart_id:
#             cart = Cart.objects.get(id=cart_id)
#             cart.cartitem_set.all().delete()
#             cart.total = 0
#             cart.save()
#         return redirect('website:cart')


# class CheckoutView(EMixin, CreateView):
#     template_name = 'checkout.html'
#     form_class = CheckoutForm
#     success_url = reverse_lazy('website:home')

#     def dispatch(self, request, *args, **kwargs):
#         if request.user.is_authenticated and request.user.customer:
#             pass
#         else:
#             return redirect('/login?next=/checkout')
#         return super().dispatch(request, *args, **kwargs)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         cart_id = self.request.session.get('cart_id', None)
#         if cart_id:
#             cart_obj = Cart.objects.get(id=cart_id)
#         else:
#             cart_obj = None
#         context['cart'] = cart_obj
#         return context

#     def form_valid(self, form):
#         cart_id = self.request.session.get('cart_id', None)
#         if cart_id:
#             cart_obj = Cart.objects.get(id=cart_id)
#             form.instance.cart = cart_obj
#             form.instance.sub_total = cart_obj.total
#             form.instance.total = cart_obj.total
#             form.instance.order_status = 'Order Received'
#             del self.request.session['cart_id']

#         else:
#             return redirect('website:cart')
#         return super().form_valid(form)


# class RegisterView(CreateView):
#     template_name = 'register.html'
#     form_class = RegisterForm
#     success_url = reverse_lazy('website:store')

#     def form_valid(self, form):
#         user_name = form.cleaned_data.get('username')
#         password = form.cleaned_data.get('password')
#         email = form.cleaned_data.get('email')
#         user = User.objects.create_user(user_name, email, password)
#         form.instance.user = user
#         login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
#         return super().form_valid(form)

#     def get_success_url(self):
#         if 'next' in self.request.GET:
#             next_url = self.request.GET.get('next')
#             return next_url
#         else:
#             return self.success_url


# class LoginView(FormView):
#     template_name = 'login.html'
#     form_class = LoginForm
#     success_url = reverse_lazy('website:store')

#     def form_valid(self, form):
#         uname = form.cleaned_data.get('username')
#         pword = form.cleaned_data['password']
#         usr = authenticate(username=uname, password=pword)
#         if usr is not None and usr.customer:
#             login(self.request, usr)
#         else:
#             return render(self.request, self.template_name, {'form': self.form_class, 'error': 'invalid credentials'})
#         return super().form_valid(form)

#     def get_success_url(self):
#         if 'next' in self.request.GET:
#             next_url = self.request.GET.get('next')
#             return next_url
#             print('next url')
#         else:
#             return self.success_url
#             print('success url')


# class LogoutView(View):
#     def get(self, request):
#         logout(request)
#         return redirect('website:home')


# class ProfileView(TemplateView):
#     template_name = 'profile.html'

#     def dispatch(self, request, *args, **kwargs):
#         if request.user.is_authenticated and Customer.objects.filter(user=request.user).exists():
#             pass
#         else:
#             return redirect('/login?next=/checkout')
#         return super().dispatch(request, *args, **kwargs)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         customer = self.request.user.customer
#         context['customer'] = customer
#         orders = Order.objects.filter(cart__customer=customer).order_by('-id')
#         context['orders'] = orders
#         return context


# class OrderDetailView(DetailView):
#     template_name = 'order_detail.html'
#     model = Order
#     context_object_name = 'order_obj'

#     def dispatch(self, request, *args, **kwargs):
#         if request.user.is_authenticated and Customer.objects.filter(user=request.user).exists():
#             order_id = self.kwargs['pk']
#             order = Order.objects.get(id=order_id)
#             if request.user.customer != order.cart.customer:
#                 return redirect('website:profile')
#             pass
#         else:
#             return redirect('/login?next=/checkout')
#         return super().dispatch(request, *args, **kwargs)


# class AdminLoginView(FormView):
#     template_name = 'adminpages/admin-login.html'
#     form_class = AdminLoginForm
#     success_url = reverse_lazy('website:admin-home')

#     def form_valid(self, form):
#         uname = form.cleaned_data.get('username')
#         pword = form.cleaned_data['password']
#         usr = authenticate(username=uname, password=pword)
#         if usr is not None and Admin.objects.filter(user=usr).exists():
#             login(self.request, usr)
#         else:
#             return render(self.request, self.template_name, {'form': self.form_class, 'error': 'invalid credentials'})
#         return super().form_valid(form)


# class AdminRequiredMixin(object):
#     def dispatch(self, request, *args, **kwargs):
#         if request.user.is_authenticated and Admin.objects.filter(user=request.user).exists():
#             pass
#         else:
#             return redirect('/admin-login')
#         return super().dispatch(request, *args, **kwargs)


# class AdminHomeView(AdminRequiredMixin, TemplateView):
#     template_name = 'adminpages/admin-home.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['pending_orders'] = Order.objects.filter(
#             order_status='Order Received').order_by('-id')
#         return context


# class AdminOrderDetailView(AdminRequiredMixin, DetailView):
#     template_name = 'adminpages/admin-order-detail.html'
#     model = Order
#     context_object_name = 'ord_obj'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['allstatus'] = ORDER_STATUS
#         return context


# class AdminOrderListView(AdminRequiredMixin, ListView):
#     template_name = 'adminpages/admin-order-list.html'
#     queryset = Order.objects.all().order_by('-id')
#     context_object_name = 'allorders'


# class AdminOrderStatusChangeView(AdminRequiredMixin, View):
#     def post(self, request, *args, **kwargs):
#         order_id = self.kwargs['pk']
#         order_obj = Order.objects.get(id=order_id)
#         new_status = request.POST.get('status')
#         order_obj.order_status = new_status
#         order_obj.save()
#         print(new_status)
#         return redirect(reverse_lazy('website:admin-order-detail', kwargs={'pk': order_id}))


# class SearchView(TemplateView):
#     template_name = 'search.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         kw = self.request.GET['keyword']
#         results = Product.objects.filter(
#             Q(title__icontains=kw) | Q(description__icontains=kw))
#         context['results'] = results
#         print(kw)
#         return context
