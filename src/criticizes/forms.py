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


        # ---- pour recupérer user, surgage de sav selon modèle Thierry C, avec passage en class
        # sur la vue ---
        # ---> msg erreur : TypeError: __init__() takes 1 positional argument but 2 were given
        # def __init__(self, *args, **kwargs):
        #     self.request = kwargs.pop('request')
        #     super().__init__(*args, **kwargs)
        #
        # def save(self, commit=True):
        #     instance = super().save(commit=False)
        #     # C'est ici, dans save() qu'on récupère l'utilisateur à partir de la request
        #     instance.user = self.request.user
        #     if commit:
        #         instance.save()
        #     return instance