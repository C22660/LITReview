from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.urls import reverse
from django.views.generic import ListView
from django.utils.decorators import method_decorator


from criticizes.forms import TicketForm, ReviewForm, UserFollowsForm
from criticizes.models import UserFollows, Ticket


# ------ page tickets.html ------
@login_required
def ticket_view(request):
    # Solution selon TH Udemy
    if request.method == "POST":
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            print(form.cleaned_data)
            print(request.user)
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return HttpResponseRedirect(reverse('criticizes:flux'))

    else:
        form = TicketForm()

    return render(request, "criticizes/tickets.html", {"form": form})


@login_required
def review_view(request, ticket_id=14):
    # Affiche le ticket concerné
    ticket_needing_answer = get_object_or_404(Ticket, id=ticket_id)

    # Affiche le formulaire de réponse (notation)
    # Solution selon TH Udemy
    if request.method == "POST":
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            print(form.cleaned_data)
            review = form.save(commit=False)
            review.ticket = ticket_needing_answer
            review.user = request.user
            review.save()
    else:
        form = ReviewForm()

    context = {
        "ticket_needing_answer": ticket_needing_answer,
        "form": form,
    }

    return render(request, "criticizes/criticism.html", context)


# @login_required
# def user_follow_view(request):
#     """
#     Affiche un champ de texte pour y indiquer le nom de l'utilisateur à suivre
#     """
#     # Solution selon TH Udemy
#     if request.method == "POST":
#         form = UserFollowsForm(request.POST)
#         if form.is_valid():
#
#             data = form.cleaned_data
#             print(data)
#             print(request.user)
#             follower = User.objects.get(username=request.user)
#             followed = User.objects.get(username=data.get('searched_user_name'))
#
#             relation = UserFollows(user=follower, followed_user=followed)
#             relation.save()
#             # redirect to a new URL if save (page success) ? ou voir redirect video 73 TH
#             # return HttpResponseRedirect(reverse('all-borrowed') )
#     else:
#         form = UserFollowsForm()
#
#     return render(request, "criticizes/followers.html", {"form": form})

# EN TEST REGROUPEMENT FOLLOWING-FOLLOWER DANS LA MËME FONCTION QUE FOLLOWER
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
            print(data)
            print(request.user)
            follower = User.objects.get(username=request.user)
            followed = User.objects.get(username=data.get('searched_user_name'))

            relation = UserFollows(user=follower, followed_user=followed)
            relation.save()
            # faire un

    else:
        form = UserFollowsForm()

    template = 'criticizes/followers.html'
    context = {"form": form, 'followed_by_user': followed_by_user, 'user_followed_by': user_followed_by}
    return render(request, template, context)

# # ------ page followers.html ------
# def list_followers(request):
#     """
#     Recherche, dans UserFollows les relations.
#     D'abord les abonnements de l'utilisateur connecté, puis ses abonnés
#     """
#     # users = UserFollows.objects.all()
#
#     pk_connected_user = request.user.pk
#     followed_by_user = UserFollows.objects.filter(followed_user=pk_connected_user)
#
#     user_followed_by = request.user.following.all()
#     template = 'criticizes/summary_followers.html'
#     # template = 'criticizes/followers.html'
#     context = {'followed_by_user': followed_by_user, 'user_followed_by': user_followed_by}
#     return render(request, template, context)


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
@method_decorator(login_required, name='dispatch')
class ListTickets(ListView):
    model = Ticket
    context_object_name = "tickets"
    template_name = 'criticizes/flux.html'

# ------ page posts.html ------
@method_decorator(login_required, name='dispatch')
class ListPosts(ListView):
    """
    N'affiche que les posts réalisés par l'utilisateur connecté
    """
    model = Ticket
    context_object_name = "posts"
    template_name = 'criticizes/posts.html'

    def get_queryset(self):
        # on récupère les données retrournées par le queryset
        queryset = super().get_queryset()

        return queryset.filter(user=self.request.user)

