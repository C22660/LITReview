from django.urls import path

from criticizes.views import ticket_view

# chemin des urls
app_name = "criticizes"

urlpatterns = [
    path('ticket/', ticket_view, name="ticket")
]
