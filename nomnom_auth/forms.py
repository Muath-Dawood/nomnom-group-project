from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm,
)

User = get_user_model()

class LoginForm(AuthenticationForm):
    username = forms.EmailField(label='Email', max_length=254)

    def clean_username(self):
        # Ensure the email exists in the User model
        email = self.cleaned_data.get('username')
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("No user with this email address.")
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add bootstrap classes to form fields
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
        })


class RegistrationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['first_name'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['last_name'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['address'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['profile_pic'].widget.attrs.update({
            'class': 'form-control',
        })

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password1', 'password2', 'address', 'profile_pic']
