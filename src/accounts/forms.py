from django import forms

# formulaire depuis le Form de django
class SignupForm(forms.Form):
    user_name = forms.CharField(label="Nom d'utilisateur", min_length=4, max_length=10, required=True)
    password = forms.CharField(label="Mot de passe", min_length=6, widget=forms.PasswordInput())
    confirmation_password = forms.CharField(label="Confirmer mot de passe", min_length=6, widget=forms.PasswordInput())
    cgu_accept = forms.BooleanField(initial=True)

    def clean_confirmation_password(self):
        password = self.cleaned_data.get("password")
        confirmation_password = self.cleaned_data.get("confirmation_password")
        if password != confirmation_password:
            raise forms.ValidationError("Le mot de passe et sa confirmation doivent être identiques.")
        return password, confirmation_password