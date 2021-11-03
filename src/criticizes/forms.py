from django import forms
from django.contrib.auth.models import User

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
                   "body": forms.Textarea(attrs={'rows': 4})}


class UserFollowsForm(forms.Form):
    searched_user_name = forms.CharField(label="Nom d'utilisateur", min_length=4, max_length=10,
                                         required=True)

    def clean_searched_user_name(self):
        # video 109 TH
        data = self.cleaned_data.get('searched_user_name')
        print(self.cleaned_data)
        try:
            followed = User.objects.get(username=data)
        except User.DoesNotExist:
            raise forms.ValidationError("L'utilisateur est introuvable.")

        return data
