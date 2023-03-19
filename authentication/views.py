from django.shortcuts import render,redirect
from django.views.generic import TemplateView,CreateView,FormView
from authentication.forms import RegisterForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
User = get_user_model()
# Create your views here.

class RegisterView(FormView):
    template_name = 'authentication/register.html'
    form_class = RegisterForm

    def form_valid(self, form):
        uname = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        confirm_password = form.cleaned_data.get('confirm_password')
        
        if password == confirm_password:
            user = User.objects.create_user(email=email,username=uname,password=password)
            form.instance.user = user
            instance = form.save(commit=False)
            instance.customer
            form.save()
            return redirect('authentication:login')
        else:
            return ValidationError(self.request,'Passwords must match')
    




class LoginView(TemplateView):
    template_nme = 'login.html'