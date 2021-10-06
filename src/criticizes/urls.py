from django.urls import path

from criticizes.views import ticket_view, review_view, user_follow_view, ListTickets, list_followers
from criticizes.views import delete_subscription
# from criticizes.views import TicketView

# chemin des urls
app_name = "criticizes"

urlpatterns = [
    path('ticket/', ticket_view, name="ticket"),
    path('criticism/', review_view, name="review"),
    path('followers/', user_follow_view, name="user_follow"),
    path('flux/', ListTickets.as_view(), name="flux"),
    path('summary_followers/', list_followers, name="summary_followers"),
    path('delete/', delete_subscription, name="delete-subscription"),
]

# path('followers/', list_followers, name="list_followers"),
