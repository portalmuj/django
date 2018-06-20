from captcha.fields import CaptchaField
from django import forms

from .models import Offer, Employer, Form


class OfferForm(forms.ModelForm):
    captcha = CaptchaField()
    class Meta:
        model = Offer
        fields = ('position', 'description', 'branch')
        labels = {
            'position': 'Stanowisko',
            'description': 'Opis stanowiska',
            'branch': 'Branża'
        }



class EmployerForm(forms.ModelForm):
    captcha = CaptchaField()
    class Meta:
        model = Employer
        fields = ('companyName', 'description')
        labels = {
            'companyName': 'Nazwa firmy',
            'description': 'Opis firmy',
        }


from django.contrib.auth.models import User
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    passwordConfirm = forms.CharField(widget=forms.PasswordInput)
    labels = {
        'password': 'Hasło',
        'passwordConfirm': 'Powtórz hasło',
    }
    def clean_passwordConfirm(self):
        if 'password' in self.cleaned_data:
            password = self.cleaned_data['password']
            passwordConfirm = self.cleaned_data['passwordConfirm']
            if password == passwordConfirm:
                return passwordConfirm

        raise forms.ValidationError('Hasła różnią się.')


    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'passwordConfirm')
        labels = {
            'username': 'Login',
            'email': 'Adres email',
            'password': 'Hasło',
            'passwordConfirm': 'Powtórz hasło'
        }


class OfferResponseForm(forms.ModelForm):
    captcha = CaptchaField()
    class Meta:
        model = Form
        fields = ('forename', 'surname', 'email', 'phoneNumber', 'answer', 'file')
        labels = {
            'forename': 'Imię',
            'surname': 'Nazwisko',
            'email': 'Adres Email',
            'phoneNumber': 'Numer telefonu',
            'answer': 'Odpowiedź',
            'file': 'CV',
        }