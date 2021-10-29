from django.urls import path

from criticizes.views import ticket_view, review_view, user_follow_view, flux_ticket_review
from criticizes.views import delete_subscription, posts_ticket_review, update_review_view,\
    update_ticket_view, review_direct_view, confirmation_delete_ticket,\
    delete_ticket, confirmation_delete_review, delete_review

# chemin des urls
app_name = "criticizes"

urlpatterns = [
    path('ticket/', ticket_view, name="ticket"),
    path('ticket_update/', update_ticket_view, name="ticket_update"),
    path('ticket_update/<ticket_pk>', update_ticket_view, name="ticket_update"),
    path('confirmation_delete_ticket/<ticket_pk>', confirmation_delete_ticket,
         name="confirmation_delete_ticket"),
    path('delete_ticket/<ticket_pk>', delete_ticket, name="delete_ticket"),
    path('confirmation_delete_review/<review_pk>', confirmation_delete_review,
         name="confirmation_delete_review"),
    path('delete_review/<review_pk>', delete_review, name="delete_review"),
    path('criticism/<ticket_pk>', review_view, name="criticism"),
    path('criticism_update/', update_review_view, name="criticism_update"),
    path('criticism_update/<review_pk>', update_review_view, name="criticism_update"),
    path('criticism_direct/', review_direct_view, name="criticism_direct"),
    path('followers/', user_follow_view, name="user_follow"),
    path('flux/', flux_ticket_review, name="flux"),
    path('delete/', delete_subscription, name="delete-subscription"),
    path('posts/', posts_ticket_review, name="posts"),
    path('review_view/', review_view, name="review_view"),
]
