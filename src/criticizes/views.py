from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.models import User

from criticizes.forms import TicketForm, ReviewForm, UserFollowsForm
from criticizes.models import UserFollows

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
            # form.save()
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
