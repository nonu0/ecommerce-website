from django.shortcuts import render,redirect
from django.views.generic import TemplateView,CreateView,FormView
from authentication.forms import RegisterForm,LoginForm
from django.http import HttpResponseRedirect
from django.shortcuts import resolve_url
from django.conf import settings
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.auth import get_user_model,login,authenticate,logout
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from authentication.tokens import activation_token
from authentication.utils import RedirectURLMixin,RegisterLoginPagesMixin
User = get_user_model()
# Create your views here.

def activation_email(User,request):
        current_site = get_current_site(request)
        email_subject = 'Activate your account'
        email_body = render_to_string('activate-email.html',{
            'User':User,
            'domain':current_site,
            'uid':urlsafe_base64_encode(force_bytes(User.pk)),
            'token':activation_token.make_token(User) 
        })

        
        email = EmailMessage(subject=email_subject,body=email_body,
                             from_email=settings.EMAIL_FROM_USER,to=[User.email])
        print(email)
        email.send()

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
            activation_email(user,self.request)
            messages.add_message(self.request,'check email for verification link')
            return redirect('authentication:login')
        else:
            return ValidationError(self.request,'Passwords must match')


def activate_user(request,uidb64,token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        print('uid',uid)
        user = User.objects.get(pk=uid)
        print('User',user)
    except Exception as e:
        user=None

    if user and activation_token.check_token(user,token):
        user.email_verified=True
        user.save()

        messages.add_message(request,messages.SUCCESS,
        'Email verified,you can now login')
        return redirect('authentication:login')

    return render(request,'activate-failed.html',{'user':user})


class LoginView(RegisterLoginPagesMixin,RedirectURLMixin,FormView):
    redirect_authenticated_user = False
    template_name = 'authentication/login.html'
    form_class = LoginForm

    def dispatch(self, request, *args, **kwargs):
        
        if self.redirect_authenticated_user and self.request.user.is_authenticated:
            redirect_to = self.get_success_url()
            if redirect_to == self.request.path:
                raise ValueError(
                    "Redirection loop for authenticated user detected. Check that "
                    "your LOGIN_REDIRECT_URL doesn't point to a login page."
                )
            return HttpResponseRedirect(redirect_to)
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self,form):
        uname = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request,username=uname,password=password)
        if not user.is_verified:
            messages.add_message(self.request,'Email is not verified')
            return render(self.request,'authentication:activate_email.html')
        if user is not None and user.email_verified:
            login(self.request,user=user)
        else:
            return render(self.request,self.template_name,{'form':self.form_class,'error':'invalid credentials'})
        return super().form_valid(form)

    def get_default_redirect_url(self):
        """Return the default redirect URL."""
        if self.next_page:
            return resolve_url(self.next_page)
        else:
            return resolve_url(settings.LOGIN_REDIRECT_URL)
    