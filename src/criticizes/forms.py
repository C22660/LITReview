from django import forms

from criticizes.models import Ticket

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

# formulaire depuis models.py
class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        # pour selectionner les champs à afficher :
        # fields = ["title", "description"]
        # pour exclure les champs à afficher :
        # exclude = ["title", "description"]
        fields = ["title",
                  "description",
                  "image",
                  "user"
                  ]

        # pour modifier le nom du champ affichier, au lieu de verbose_name dans models :
        # labels = {"title": "Titre",}

        # si on avait mis la date, on pourrais modifier le widget :
        # widgets = {"date": forms.SelecDateWidget(years=range(1998, 2040)}