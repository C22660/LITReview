from django.http import HttpResponse
from django.shortcuts import render

from criticizes.forms import TicketForm


def ticket_view(request):
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
    else:
        form = TicketForm()

    return render(request, "criticizes/tickets.html", {"form": form})