from django import forms
from website.models import *
from django.contrib.auth import get_user_model
User = get_user_model()
class RegisterForm(forms.ModelForm):
    password = forms.PasswordInput()
    confirm_password = forms.PasswordInput()
    class Meta:
        model = Customer
        fields = ['fname','lname','email','username','address','password','confirm_password']
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValueError('username already taken')
        return username