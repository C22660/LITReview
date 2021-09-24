from django.http import HttpResponse
from django.shortcuts import render

from criticizes.forms import SignupForm, TicketForm



def signup(request):

    if request.method == "POST":
        form = SignupForm(request.POST)
        # Autre façon de récupérer le password avant form.is_valid
        # password = request.POST.get('password')

        if form.is_valid():
            # Une façon de récupérer le password après form.is_valid
            # password = form.cleaned_data['password']
            # print(form.cleaned_data)
            return HttpResponse("Merci de votre inscription")

    else:
        form = SignupForm()

    # dans ce return, on retourne le formulaire qui contient les données
    return render(request, "criticizes/signup.html", {'form': form})


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