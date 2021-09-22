from django import forms


class SignupForm(forms.Form):
    user_name = forms.CharField(max_length=10, required=True)
    password = forms.CharField(min_length=6, widget=forms.PasswordInput())
    cgu_accept = forms.BooleanField(initial=True)