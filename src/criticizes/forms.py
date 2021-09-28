from django import forms

from criticizes.models import Ticket


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