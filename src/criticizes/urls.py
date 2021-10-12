from django.urls import path

from criticizes.views import ticket_view, review_view, user_follow_view, ListTickets
from criticizes.views import delete_subscription, ListPosts, update_review_view, update_ticket_view
# from criticizes.views import TicketView

# chemin des urls
app_name = "criticizes"

urlpatterns = [
    path('ticket/', ticket_view, name="ticket"),
    path('ticket_update/', update_ticket_view, name="ticket_update"),
    path('criticism/', review_view, name="review"),
    path('criticism_update/', update_review_view, name="criticism_update"),
    path('followers/', user_follow_view, name="user_follow"),
    path('flux/', ListTickets.as_view(), name="flux"),
    path('delete/', delete_subscription, name="delete-subscription"),
    path('posts/', ListPosts.as_view(), name="posts"),
]

# path('followers/', list_followers, name="list_followers"),
# path('summary_followers/', list_followers, name="summary_followers"),
