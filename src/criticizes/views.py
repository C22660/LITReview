from itertools import chain

from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.core.files.uploadedfile import UploadedFile
from django.db.models import Value, CharField
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.urls import reverse
from django.views.generic import ListView, UpdateView
from django.utils.decorators import method_decorator
from django.contrib import messages


from criticizes.forms import TicketForm, ReviewForm, UserFollowsForm
from criticizes.models import UserFollows, Ticket, Review


# ------ Création d'un ticket (demande de critique), page tickets.html ------
@login_required
def ticket_view(request):
    """
    Permet la création d'un ticket
    """
    # Solution selon TH Udemy
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
def update_ticket_view(request, ticket_id=42):
    """
    Permet la modification d'un ticket
    """
    ticket_needing_update = get_object_or_404(Ticket, id=ticket_id)

    if request.method == "POST":
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            new_datas = form.cleaned_data
            form.save(commit=False)
            print(UploadedFile.name)
            ticket_needing_update.title = new_datas.get("title")
            ticket_needing_update.description = new_datas.get("description")
            ticket_needing_update.image = new_datas.get("image")
            # ticket_needing_update.image = request.FILES("image")
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

# ------ Création de la review(en réponse à un ticket), page criticism.html ------
@login_required
def review_view(request, ticket_id=33):
    """
    Permet la création d'une critique en réponse au ticket affiché
    """
    # Affiche le ticket concerné
    ticket_needing_answer = get_object_or_404(Ticket, id=ticket_id)
    print(ticket_needing_answer)
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
def update_review_view(request, review_id=1):
    """
    Permet la modification d'une critique
    """
    # Récupère la review concernée
    review_needing_update = get_object_or_404(Review, id=review_id)
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

# ------ Création d'une critique, review(sans réponse à un ticket), page criticism_direct.html ------
@login_required
def review_direct_view(request):
    """
    Permet la création d'une critique en direct sans réponse à un ticket
    """
    # Intègre les deux formulaires

    review_form = ReviewForm()
    ticket_form = TicketForm()

    # Affiche le formulaire de création du ticket
    if request.method == "POST":
        ticket_form = TicketForm(request.POST, request.FILES)
        review_form = ReviewForm(request.POST)
        if ticket_form.is_valid() and review_form.is_valid():
            ticket_datas = ticket_form.cleaned_data
            print(ticket_datas)
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            ticket_recorded = Ticket.objects.last()
            print(ticket_recorded)
            print(review_form.cleaned_data)
            review = review_form.save(commit=False)
            review.ticket = ticket_recorded
            review.user = request.user
            review.save()

            return HttpResponseRedirect(reverse('criticizes:flux'))

    else:
        ticket_form = TicketForm()
        review_form = ReviewForm()


    # # Affiche le formulaire de réponse (notation)
    # # Solution selon TH Udemy
    # if request.method == "POST":
    #     review_form = ReviewForm(request.POST)
    #     if review_form.is_valid():
    #         print(review_form.cleaned_data)
    #         # review = review_form.save(commit=False)
    #         # review.ticket = ticket_needing_answer
    #         # review.user = request.user
    #         # review.save()
    # else:
    #     review_form = ReviewForm()

    context = {
        "ticket_form": ticket_form,
        "review_form": review_form,
    }

    return render(request, "criticizes/criticism_direct.html", context)


# ------ Suivi d'un utilisateur, page followers.html ------
@login_required
def user_follow_view(request):
    """
    Affiche un champ de texte pour y indiquer le nom de l'utilisateur à suivre,
    ainsi que les abonnements et les abonnés sur la page followers.html
    """
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
    context = {"form": form, 'followed_by_user': followed_by_user, 'user_followed_by': user_followed_by}
    return render(request, template, context)


def delete_subscription(request):
    """
    Supprime l'abonnement dans le table UserFollows par la suppression de la PK de l'enregistrement
    collecté depuis la page html et de la donnée issue de def list_followers
    """
    pk_in_database = request.POST.get('primary_key_of_subscription')
    # Recherche de la ligne correspondante à la PK dans la BD
    recording_in_UserFollows = UserFollows.objects.get(pk=pk_in_database)
    # suppression dans la BD
    recording_in_UserFollows.delete()
    return redirect('criticizes:user_follow')


# ------ page flux.html ------
# Class mais ici, juste avec les tickets
# @method_decorator(login_required, name='dispatch')
# class ListTickets(ListView):
#     model = Ticket
#     context_object_name = "tickets"
#     template_name = 'criticizes/flux.html'

@login_required
def flux_ticket_review(request):
    tickets = Ticket.objects.all()
    reviews = Review.objects.all()

    tickets_and_reviews = sorted(chain(tickets, reviews), key=lambda instance: instance.time_created,
                                 reverse=True)

    paginator = Paginator(tickets_and_reviews, 6)
    page = request.GET.get('page')

    page_obj = paginator.get_page(page)

    template = 'criticizes/flux.html'
    context = {'page_obj': page_obj}
    return render(request, template, context=context)
    # template = 'criticizes/flux.html'
    # context = {'tickets_and_reviews': tickets_and_reviews}
    # return render(request, template, context=context)

# ------ page posts.html ------
# @method_decorator(login_required, name='dispatch')
# class ListPosts(ListView):
#     """
#     N'affiche que les posts réalisés par l'utilisateur connecté
#     """
#     model = Ticket
#     context_object_name = "posts"
#     template_name = 'criticizes/posts.html'
#
#     def get_queryset(self):
#         # on récupère les données retrournées par le queryset
#         queryset = super().get_queryset()
#
#         return queryset.filter(user=self.request.user)
@login_required
def posts_ticket_review(request):
    tickets = Ticket.objects.filter(user=request.user)
    reviews = Review.objects.filter(user=request.user)

    tickets_and_reviews = sorted(chain(tickets, reviews), key=lambda instance: instance.time_created,
                                 reverse=True)

    paginator = Paginator(tickets_and_reviews, 6)
    page = request.GET.get('page')

    page_obj = paginator.get_page(page)

    template = 'criticizes/flux.html'
    context = {'page_obj': page_obj}
    return render(request, template, context=context)
    # template = 'criticizes/flux.html'
    # context = {'tickets_and_reviews': tickets_and_reviews}
    # return render(request, template, context=context)

