from pyexpat import model
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django import forms
 
class CustomUserForm(UserCreationForm):
  username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter User Name'}))
  email=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Email Address'}))
  password1=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter Your Password'}))
  password2=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter Confirm Password'}))
  class Meta:
    model=User
    fields=['username','email','password1','password2']




# forms.py

# from django import forms

# class PaymentForm(forms.Form):
#     PAYMENT_METHOD_CHOICES = [
#         ('ATM', 'Card'),
#         ('UPI', 'UPI'),
#         ('COD', 'Cash on Delivery'),
#     ]
#     payment_method = forms.ChoiceField(choices=PAYMENT_METHOD_CHOICES, widget=forms.RadioSelect)
#     card_number = forms.CharField(max_length=16, required=False)
#     expiry_date = forms.CharField(max_length=5, required=False)
#     cvv = forms.CharField(max_length=3, required=False)
#     upi_id = forms.CharField(max_length=50, required=False)
#     email = forms.EmailField()


# forms.py

from django import forms

class PaymentForm(forms.Form):
    PAYMENT_CHOICES = [
        ('ATM', 'Credit/Debit Card'),
        ('UPI', 'UPI'),
        ('COD', 'Cash on Delivery'),
    ]
    payment_method = forms.ChoiceField(choices=PAYMENT_CHOICES, widget=forms.RadioSelect)
    card_number = forms.CharField(required=False, max_length=16)
    expiry_date = forms.CharField(required=False, max_length=5)
    cvv = forms.CharField(required=False, max_length=3)
    upi_id = forms.CharField(required=False)

