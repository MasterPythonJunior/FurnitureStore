from django import forms
from .models import *
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=50, help_text='Максимум 50 символов',
                               widget=forms.TextInput(attrs={
                                   'class': 'form-control',
                                   'placeholder': 'Имя пользователя',
        'style': 'padding:12px;width:100%;border:none;background:transparent;'
                               }))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Пороль',
        'style': 'padding:12px;width:100%;border:none;background:transparent;'
    }))


class RegistrationForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Пароль',
        'style': 'padding:12px;width:100%;border:none;background:transparent;'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Подтвердите пароль',
        'style': 'padding:12px;width:100%;border:none;background:transparent;'
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Имя пользователя',
        'style': 'padding:12px;width:100%;border:none;background:transparent;'
    }))
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Ваше имя',
        'style': 'padding:12px;width:100%;border:none;background:transparent;'
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Ваша Фамилия',
        'style': 'padding:12px;width:100%;border:none;background:transparent;'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Ваша почта',
        'style': 'padding:12px;width:100%;border:none;background:transparent;'
    }))

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'username',
            'password1',
            'password2')


class UserFirstNameForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('first_name',)
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),

        }




class UserLastNameForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('last_name',)
        widgets = {
            'last_name': forms.TextInput(attrs={
                'class': 'form-control'
            })
        }


class UserCityForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('city',)
        widgets = {
            'city': forms.Select(attrs={
                'class': 'form-select mb-4'
            })
        }


class UserPhoneForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone_number',)
        widgets = {
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control'
            })
        }


class ShippingForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ('address', 'city')
        widgets = {
            'city': forms.Select(attrs={
                'class': 'form-select mb-4',
                'style': 'padding:12px;width:100%;border:none;background:transparent;'

            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Укажите адрес, улица, дом, подъезд',
                'style': 'padding:12px;width:100%;border:none;background:transparent;'

            })
        }


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('first_name', 'last_name', 'email', 'phone_number')
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите ваше имя',
                'required': False
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите вашу фамилию',
                'required': False
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ваша почта',
                'required': False
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите ваш номер телефона'
            })
        }
