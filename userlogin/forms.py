from django import forms
from django.contrib.auth.models import User
from internal.models import Employee


class LoginForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)


class UserForm(forms.ModelForm):
    #password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'last_name', 'email')
        widgets = {
            'password': forms.PasswordInput(),
        }


class UserExtendedForm(forms.ModelForm):
    class Meta:
        model = Employee
        exclude = ['user', 'is_active']