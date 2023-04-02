from django import forms
from website.models import Order

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['shipping_address', 'phone', 'email', 'ordered_by']
            

