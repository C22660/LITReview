from django.urls import path

from criticizes.views import ticket_view, review_view, user_follow_view
# from criticizes.views import TicketView

# chemin des urls
app_name = "criticizes"

urlpatterns = [
    path('ticket/', ticket_view, name="ticket"),
    path('criticism/', review_view, name="review"),
    path('followers/', user_follow_view, name="review")
]
