from django.urls import path, include

from accounts.views import signup

# chemin des urls
app_name = "accounts"

urlpatterns = [
    path('compte/', include('django.contrib.auth.urls')),
    path('compte/signup', signup, name='signup'),
]
