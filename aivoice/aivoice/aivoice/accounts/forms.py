from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    username = forms.CharField(max_length=150, required=True)
    otp = forms.CharField(max_length=6, required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'otp']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(RegisterForm, self).__init__(*args, **kwargs)

    def clean_otp(self):
        otp = self.cleaned_data.get('otp')
        email = self.cleaned_data.get('email')
        session_otp = self.request.session.get('otp')
        session_email = self.request.session.get('email')

        if not session_otp or not session_email:
            raise forms.ValidationError("OTP not found. Please request it again.")

        if email != session_email:
            raise forms.ValidationError("Email does not match OTP.")

        if otp != session_otp:
            raise forms.ValidationError("Invalid OTP.")

        return otp



class LoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email")
