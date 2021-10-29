from itertools import chain

from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib import messages
from django.db.models import Q

from criticizes.forms import TicketForm, ReviewForm, UserFollowsForm
from criticizes.models import UserFollows, Ticket, Review


# ------ Création d'un ticket (demande de critique), page tickets.html ------
@login_required
def ticket_view(request):
    """Permet la création d'un ticket."""
    if request.method == "POST":
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            # print(form.cleaned_data)
            # print(request.user)
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return HttpResponseRedirect(reverse('criticizes:flux'))

    else:
        form = TicketForm()

    return render(request, "criticizes/tickets.html", {"form": form})


# ------ Modification du ticket, page ticket_update.html ------
@login_required
def update_ticket_view(request, ticket_pk):
    """Permet la modification d'un ticket."""
    if ticket_pk != "":
        ticket_needing_update = get_object_or_404(Ticket, id=ticket_pk)

    if request.method == "POST":
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            new_datas = form.cleaned_data
            form.save(commit=False)
            ticket_needing_update.title = new_datas.get("title")
            ticket_needing_update.description = new_datas.get("description")
            if new_datas.get("image"):
                ticket_needing_update.image = new_datas.get("image")
            ticket_needing_update.user = request.user
            ticket_needing_update.save()

            return HttpResponseRedirect(reverse('criticizes:flux'))
    else:
        form = TicketForm(initial={"title": ticket_needing_update.title,
                                   "description": ticket_needing_update.description,
                                   "image": ticket_needing_update.image})

    context = {
        "form": form,
    }

    return render(request, "criticizes/tickets_update.html", context)


# ------ Suppression d'un ticket, page ticket_confirm_delete.html ------
def confirmation_delete_ticket(request, ticket_pk=""):
    """Affiche un message de confirmation de suppression du ticket."""

    # Recherche de la ligne correspondante à la PK dans la BD
    ticket_for_deletion = get_object_or_404(Ticket, id=ticket_pk)

    return render(request, "criticizes/ticket_confirm_delete.html",
                  {"ticket": ticket_for_deletion})


def delete_ticket(request, ticket_pk=""):
    """Supprime le ticket dans le table Ticket par la suppression de la PK de
    l'enregistrement."""

    if ticket_pk == "No":
        return redirect('criticizes:flux')

    else:
        # Recherche de la ligne correspondante à la PK dans la BD
        ticket_for_deletion = get_object_or_404(Ticket, id=ticket_pk)
        ticket_for_deletion.delete()

    return HttpResponseRedirect(reverse('criticizes:flux'))


# ------ Création de la review(en réponse à un ticket), page criticism.html ------
@login_required
def review_view(request, ticket_pk=""):
    """Permet la création d'une critique en réponse au ticket affiché."""
    ticket_needing_answer = get_object_or_404(Ticket, id=ticket_pk)
    # print(ticket_needing_answer)
    # Affiche le formulaire de réponse (notation)
    # Solution selon TH Udemy
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            # print(form.cleaned_data)
            review = form.save(commit=False)
            review.ticket = ticket_needing_answer
            review.user = request.user
            review.save()

            return HttpResponseRedirect(reverse('criticizes:flux'))
    else:
        form = ReviewForm()

    context = {
        "ticket_needing_answer": ticket_needing_answer,
        "form": form,
    }

    return render(request, "criticizes/criticism.html", context)


# ------ Modification de la review, page criticism_update.html ------
@login_required
def update_review_view(request, review_pk=""):
    """Permet la modification d'une critique."""
    if review_pk != "":
        # Récupère la review concernée
        review_needing_update = get_object_or_404(Review, id=review_pk)
        # Récupère la clé du ticket associé
        ticket_linked = review_needing_update.ticket.pk
        # Récupère le ticket concerné pour affichage
        ticket_needing_answer = get_object_or_404(Ticket, id=ticket_linked)

    # Affiche le formulaire de réponse (notation)
    # Solution selon TH Udemy
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            new_datas = form.cleaned_data
            form.save(commit=False)
            review_needing_update.headline = new_datas.get("headline")
            review_needing_update.rating = new_datas.get("rating")
            review_needing_update.body = new_datas.get("body")
            review_needing_update.save()

            return HttpResponseRedirect(reverse('criticizes:flux'))
    else:
        form = ReviewForm(initial={"headline": review_needing_update.headline,
                                   "rating": review_needing_update.rating,
                                   "body": review_needing_update.body})

    context = {
        "ticket_needing_answer": ticket_needing_answer,
        "form": form,
    }

    return render(request, "criticizes/criticism_update.html", context)


# ------ Création d'une critique, review(sans réponse à un ticket),
# page criticism_direct.html ------
@login_required
def review_direct_view(request):
    """Permet la création d'une critique en direct sans réponse à un ticket."""
    # Intègre les deux formulaires

    review_form = ReviewForm()
    ticket_form = TicketForm()

    # Affiche le formulaire de création du ticket
    if request.method == "POST":
        ticket_form = TicketForm(request.POST, request.FILES)
        review_form = ReviewForm(request.POST)
        if ticket_form.is_valid() and review_form.is_valid():
            ticket_datas = ticket_form.cleaned_data
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            ticket_recorded = Ticket.objects.last()
            review = review_form.save(commit=False)
            review.ticket = ticket_recorded
            review.user = request.user
            review.save()

            return HttpResponseRedirect(reverse('criticizes:flux'))

    else:
        ticket_form = TicketForm()
        review_form = ReviewForm()

    context = {
        "ticket_form": ticket_form,
        "review_form": review_form,
    }

    return render(request, "criticizes/criticism_direct.html", context)


# ------ Suppression d'une critique, page review_confirm_delete.html ------
def confirmation_delete_review(request, review_pk=""):
    """Affiche un message de confirmation de suppression de la critique."""

    # Recherche de la ligne correspondante à la PK dans la BD
    review_for_deletion = get_object_or_404(Review, id=review_pk)

    return render(request, "criticizes/criticism_confirm_delete.html",
                  {"review": review_for_deletion})


def delete_review(request, review_pk=""):
    """Supprime la critique dans le table Review par la suppression de la PK de
    l'enregistrement."""

    # # Recherche de la ligne correspondante à la PK dans la BD
    if review_pk == "No":
        return redirect('criticizes:flux')
        # return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    #     print(review_pk)
    #     next = request.META.get('HTTP_REFERER', None) or '/'
    #     response = HttpResponseRedirect(next)
    #     return response
    else:
        review_for_deletion = get_object_or_404(Review, id=review_pk)
        review_for_deletion.delete()

    return HttpResponseRedirect(reverse('criticizes:flux'))


# ------ Suivi d'un utilisateur, page followers.html ------
@login_required
def user_follow_view(request):
    """Affiche un champ de texte pour y indiquer le nom de l'utilisateur à
    suivre, ainsi que les abonnements et les abonnés sur la page
    followers.html."""
    # Pour alimenter abonnements et abonnés (sections 2 et 3)
    pk_connected_user = request.user.pk
    followed_by_user = request.user.following.all()
    user_followed_by = UserFollows.objects.filter(followed_user=pk_connected_user)

    # Pour afficher la saisie de l'utilisateurs à suivre (section 1)
    if request.method == "POST":
        form = UserFollowsForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            # print(data)
            # print(request.user)
            follower = User.objects.get(username=request.user)
            followed = User.objects.get(username=data.get('searched_user_name'))
            # recherche des enregistrement qui ont pour user follower
            datas_followers_models = UserFollows.objects.filter(user=follower)
            # si parmi ces lignes, followed = followed_user, alors print
            for data in datas_followers_models:
                if data.followed_user.pk == followed.pk:
                    # source https://docs.djangoproject.com/fr/3.2/ref/contrib/messages/
                    messages.add_message(request, messages.INFO, "L'utilisateur est déjà suivi.")
                    # pour éviter le popup "ressoumètre le formulaire"
                    return HttpResponseRedirect(request.path)
                else:
                    relation = UserFollows(user=follower, followed_user=followed)

            relation.save()

    else:
        form = UserFollowsForm()

    template = 'criticizes/followers.html'
    context = {"form": form, 'followed_by_user': followed_by_user,
               'user_followed_by': user_followed_by}
    return render(request, template, context)


def delete_subscription(request):
    """Supprime l'abonnement dans le table UserFollows par la suppression de la
    PK de l'enregistrement collecté depuis la page html et de la donnée issue
    de def list_followers."""
    pk_in_database = request.POST.get('primary_key_of_subscription')
    # Recherche de la ligne correspondante à la PK dans la BD
    recording_in_UserFollows = UserFollows.objects.get(pk=pk_in_database)
    # suppression dans la BD
    recording_in_UserFollows.delete()
    return redirect('criticizes:user_follow')


# ------ page flux.html ------
@login_required
def flux_ticket_review(request):
    # User connecté :
    pk_connected_user = request.user.pk
    # Utilisateurs suivis par le user connecté :
    followed_by_user = request.user.following.all()
    # Création d'une liste avec les PK des utilisateurs suivis
    users_followed = []
    for i in followed_by_user:
        users_followed.append(i.followed_user.pk)

    # Combinaison des deux filtres, tickets de User et de ceux des utilisateurs suivis
    tickets = Ticket.objects.filter(Q(user=pk_connected_user) | Q(user__in=users_followed))
    # J'isole les tickets de l'utilisateur connecté pour pouvoir les récupérer dans les critiques
    # dans le cas où une personne non suivie par l'utilisateur y a répondu
    tickets_from_user_connected = []
    tickets_2 = Ticket.objects.filter(user=pk_connected_user)
    for t in tickets_2:
        tickets_from_user_connected.append(t.pk)
    # Combinaisons des filtres dans les critiques
    reviews = Review.objects.filter(Q(user=pk_connected_user) | Q(user__in=users_followed) |
                                    Q(ticket__in=tickets_from_user_connected))

    # création d'une liste des tickets ayant reçus une critique.
    # cette liste est utilisée dans ticket_snippet.html pour n'afficher le bouton
    # "créer une critique" que pour les tickets qui ne sont pas dedans
    tickets_followed = []
    for ticket in reviews:
        tickets_followed.append(ticket.ticket.pk)

    tickets_and_reviews = sorted(chain(tickets, reviews),
                                 key=lambda instance: instance.time_created, reverse=True)

    paginator = Paginator(tickets_and_reviews, 6)
    page = request.GET.get('page')

    page_obj = paginator.get_page(page)

    template = 'criticizes/flux.html'
    context = {'page_obj': page_obj, 'tickets_followed': tickets_followed}

    return render(request, template, context=context)


# ------ page posts.html ------
@login_required
def posts_ticket_review(request):
    tickets = Ticket.objects.filter(user=request.user)
    reviews = Review.objects.filter(user=request.user)

    tickets_and_reviews = sorted(chain(tickets, reviews),
                                 key=lambda instance: instance.time_created, reverse=True)

    paginator = Paginator(tickets_and_reviews, 6)
    page = request.GET.get('page')

    page_obj = paginator.get_page(page)

    template = 'criticizes/posts.html'
    context = {'page_obj': page_obj}
    return render(request, template, context=context)
