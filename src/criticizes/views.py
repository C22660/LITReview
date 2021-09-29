from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from criticizes.forms import TicketForm

# sous forme de fonction
def ticket_view(request):
    # Solution selon TH Udemy
    if request.method == "POST":
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            print(form.cleaned_data)
            form.save()
            # pour éviter une sauvegarde automatique avec form.save() et que l'on veut pouvoir
            # ajouter une action (en fonction des champs existants, ex ici avec published
            # ticket_post = form.save(commit=False)
            # ticket_post.published = True
            # ticket_post.save()
#
#     # Solution source cours GB OpenclassRoom
#     # --> msg erreur : image = TicketForm.save(commit=False)
#     # ---> TypeError: save() missing 1 required positional argument: 'self'
#     # form = TicketForm()
#     # if request.method == "POST":
#     #     form = TicketForm(request.POST, request.FILES)
#     #     if form.is_valid():
#     #         image = TicketForm.save(commit=False)
#     #         image.uploader = request.user
#     #         image.save()
#
    else:
        form = TicketForm()

    return render(request, "criticizes/tickets.html", {"form": form})


# sous forme de class selon modèle Thierry C, suite surcharge sav() dans forms
# --> msg erreur TypeError: __init__() takes 1 positional argument but 2 were given
# class TicketView(CreateView):
#     form_class = TicketForm
#     template_name = 'criticizes/tickets.html'
#     success_url = reverse_lazy('criticizes/tickets.html')
#
#     def get_form_kwargs(self):
#         kwargs = super().get_form_kwargs()
#         kwargs['request'] = self.request
#         return kwargs