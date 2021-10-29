"""LitReview URL Configuration.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from LitReview import settings
# from .views import index, signup, ticket_view


urlpatterns = [
    path('administration-application/', admin.site.urls),
    path('', include('criticizes.urls')),
    path('', include('accounts.urls')),
]
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# urlpatterns = [
#     path('', index, name="index"),
#     path('administration-application/', admin.site.urls),
#     path('LitReview/', include('criticizes.urls')),
# ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# path('signup', signup, name='signup'),
# path('ticket/', ticket_view, name="ticket")
