from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .models import *
from django import forms


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['phone','password1','password2']

class LoginForm(AuthenticationForm):
    username = forms.CharField(label = 'Phone')

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['firstname','lastname','address','passport_id']

class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ['card_number','date','type']

class TransferForm(forms.Form):
    source = forms.CharField()
    destination = forms.CharField()
    amount = forms.IntegerField()

class CheckPhoneForm(forms.Form):
    phone = forms.CharField()

class CheckCardForm(forms.Form):
    phone = forms.CharField()
