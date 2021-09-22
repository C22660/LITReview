from django.http import HttpResponse
from django.shortcuts import render

from LitReview.forms import SignupForm

def index(request):
    return render(request, "index.html")

def signup(request):

    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            return HttpResponse("Merci de votre inscription")
    else:
        form = SignupForm()

    return render(request, "accounts/signup.html", {'form': form})