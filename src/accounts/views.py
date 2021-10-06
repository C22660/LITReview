from django.shortcuts import render
from django.contrib.auth.models import User

from accounts.forms import SignupForm

# Create your views here.

def signup(request):

    if request.method == "POST":
        form = SignupForm(request.POST)
        # Autre façon de récupérer le password avant form.is_valid
        # password = request.POST.get('password')

        if form.is_valid():
            # Une façon de récupérer le password après form.is_valid
            # password = form.cleaned_data['password']
            # print(form.cleaned_data)
            username = form.cleaned_data['user_name']
            password = form.cleaned_data['password']

            User.objects.create_user(username=username, password=password)

            # inscription = form.save()
            # form.save()
            # return HttpResponse("Merci de votre inscription")

    else:
        form = SignupForm()

    # dans ce return, on retourne le formulaire qui contient les données
    return render(request, "accounts/signup.html", {'form': form})
