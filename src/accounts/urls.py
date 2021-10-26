from django.urls import path, include

from accounts.views import signup
from django.contrib.auth import views as auth_views

# chemin des urls
app_name = "accounts"

urlpatterns = [
    path('', auth_views.LoginView.as_view(), name='login'),
    path('compte/', include('django.contrib.auth.urls')),
    path('compte/nouveau', signup, name='signup'),
]
