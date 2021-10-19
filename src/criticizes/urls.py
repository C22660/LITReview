from django.urls import path

from criticizes.views import ticket_view, review_view, user_follow_view, flux_ticket_review
from criticizes.views import delete_subscription, posts_ticket_review, update_review_view,\
    update_ticket_view, review_direct_view, review_view
# from criticizes.views import TicketView

# chemin des urls
app_name = "criticizes"

urlpatterns = [
    path('ticket/', ticket_view, name="ticket"),
    path('ticket_update/', update_ticket_view, name="ticket_update"),
    path('criticism/', review_view, name="criticism"),
    path('criticism_update/', update_review_view, name="criticism_update"),
    path('criticism_direct/', review_direct_view, name="criticism_direct"),
    path('followers/', user_follow_view, name="user_follow"),
    path('flux/', flux_ticket_review, name="flux"),
    path('delete/', delete_subscription, name="delete-subscription"),
    path('posts/', posts_ticket_review, name="posts"),
    path('review_view/', review_view, name="review_view"),
]

# path('followers/', list_followers, name="list_followers"),
# path('summary_followers/', list_followers, name="summary_followers"),
# path('flux/', ListTickets.as_view(), name="flux"),
