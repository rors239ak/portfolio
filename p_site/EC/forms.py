from django import forms
from .models import Product
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'description', 'photo', 'price', 'stock']

class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='必須')

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")