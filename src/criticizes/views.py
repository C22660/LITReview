from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views.generic import ListView


from criticizes.forms import TicketForm, ReviewForm, UserFollowsForm
from criticizes.models import UserFollows, Ticket


# sous forme de fonction
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

    else:
        form = TicketForm()

    return render(request, "criticizes/tickets.html", {"form": form})


@login_required
def review_view(request):
    # Solution selon TH Udemy
    if request.method == "POST":
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    else:
        form = ReviewForm()

    return render(request, "criticizes/criticism.html", {"form": form})


@login_required
def user_follow_view(request):
    """
    Affiche un champ de texte pour y indiquer le nom de l'utilisateur à suivre
    """
    # Solution selon TH Udemy
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
            # redirect to a new URL if save (page success) ? ou voir redirect video 73 TH
            # return HttpResponseRedirect(reverse('all-borrowed') )
    else:
        form = UserFollowsForm()

    return render(request, "criticizes/followers.html", {"form": form})


def list_followers(request):
    """
    Recherche, dans UserFollows les relations.
    D'abord les abonnements de l'utilisateur connecté, puis ses abonnés
    """
    # users = UserFollows.objects.all()

    pk_connected_user = request.user.pk
    followed_by_user = UserFollows.objects.filter(followed_user=pk_connected_user)

    user_followed_by = request.user.following.all()
    template = 'criticizes/summary_followers.html'
    # template = 'criticizes/followers.html'
    context = {'followed_by_user': followed_by_user, 'user_followed_by': user_followed_by}
    return render(request, template, context)


def delete_subscription(request):
    """
    Supprime l'abonnement dans le table UserFollows par la suppression de la PK de l'enregistrement
    collecté depuis la page html et de la donnée issue de def list_followers
    """
    pk_in_database = request.POST.get('primary_key_of_subsciption')
    # Recherche de la ligne correspondante à la PK dans la BD
    recording_in_UserFollows = UserFollows.objects.get(pk=pk_in_database)
    # suppression dans la BD
    recording_in_UserFollows.delete()
    return redirect('criticizes:summary_followers')


class ListTickets(ListView):
    model = Ticket
    context_object_name = "tickets"
    template_name = 'criticizes/flux.html'
