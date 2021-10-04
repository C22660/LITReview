from sqlite3 import IntegrityError

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404

from criticizes.models import Ticket, Review, UserFollows


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

# RadioSelect options
RATING_OPTIONS = [
    ("0", "0"),
    ("1", "1"),
    ("2", "2"),
    ("3", "3"),
    ("4", "4"),
    ("5", "5")
]

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["headline",
                  "rating",
                  "body",
                  ]
        # Modification du nom des champ afficher :
        labels = {"headline": "Titre", "rating": "Note", "body": "Commentaire"}

        # Modification du widget de la notation :
        widgets = {"rating": forms.RadioSelect(choices=RATING_OPTIONS),
                   "body": forms.Textarea(attrs={'rows':4, 'cols':40})}


class UserFollowsForm(forms.Form):
    searched_user_name = forms.CharField(label="Nom d'utilisateur", min_length=4, max_length=10,
                                         required=True)

    def clean_searched_user_name(self):
        # video 109 TH
        data = self.cleaned_data.get('searched_user_name')
        try:
            followed = User.objects.get(username=data)
        except User.DoesNotExist:
            raise forms.ValidationError("L'utilisateur est introuvable.")
        except IntegrityError:
            raise forms.ValidationError("L'utilisateur est déjà suivi.")

    #     if password != confirmation_password:
    #     raise forms.ValidationError("Le mot de passe et sa confirmation doivent être identiques.")
    # return password, confirmation_password
        # #Check date is not in past.
        # if data < datetime.date.today():
        #     raise ValidationError(_('Invalid date - renewal in past'))
        #
        # #Check date is in range librarian allowed to change (+4 weeks).
        # if data > datetime.date.today() + datetime.timedelta(weeks=4):
        #     raise ValidationError(_('Nom invalide - Utilisateur non trouvé'))
        #       -> au lieu de raise, voir get_object_or_404 video 74 TH
        # # Remember to always return the cleaned data.
        return data

