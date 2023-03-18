from django import forms
from website.models import *

class RegisterForm(forms.ModelForm):
    password = forms.PasswordInput()
    confirm_password = forms.PasswordInput()
    class Meta:
        model = Customer
        fields = ['fname','lname','email','username','address']
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter()