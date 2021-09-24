from django.urls import path

from criticizes.views import signup, ticket_view

# chemin des urls
app_name = "criticizes"

urlpatterns = [
    path('signup', signup, name='signup'),
    path('ticket/', ticket_view, name="ticket")
]
