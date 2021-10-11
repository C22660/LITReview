from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db import models
from django.urls import reverse

from PIL import Image



class Ticket(models.Model):
    # Your Ticket model definition goes here
    title = models.CharField(max_length=128, verbose_name="Titre")
    # title = models.CharField(max_length=128, verbose_name="Titre")
    # ajout slug facultatif (balk=True signifie Facultatif)?
    # slug = models.SlugField(max_length=128, unique=True, blank=True)
    description = models.TextField(max_length=2048, blank=True)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # pour éviter que tous les tickets ne soient supprimer si user supprimer, on peut utiliser
    # on_delete=models.SET_NULL, null=True, blank=True au lieu de on_delete=models.CASCADE
    image = models.ImageField(null=True, blank=True, upload_to='ticket_images')
    time_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    IMAGE_MAX_SIZE = (100, 150)

    def __str__(self):
        return self.title

    # Adaptation du format de l'image à un max définit en IMAGE_MAX_SIZE
    def resize_image(self):
        image = Image.open(self.image)
        image.thumbnail(self.IMAGE_MAX_SIZE)
        image.save(self.image.path)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.resize_image()

    # # après validation d'un ticket, réoriente la page vers la page flux
    # def get_absolute_url(self):
    #     return reverse('criticizes:flux')


class Review(models.Model):
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        # validates that rating must be between 0 and 5
        validators=[MinValueValidator(0), MaxValueValidator(5)])
    headline = models.CharField(max_length=128)
    body = models.CharField(max_length=8192, blank=True)
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ticket

    # si ajout du slug surcharge de la fonction save (video 141, minute 11)


class UserFollows(models.Model):
    # Your UserFollows model definition goes here
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name='following')
    followed_user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                      related_name='followed_by')

    class Meta:
        # ensures we don't get multiple UserFollows instances
        # for unique user-user_followed pairs
        unique_together = ('user', 'followed_user', )

        # A TESTER (sauf si retour ano) (& ajouter ne property si besoin vid TH 54 4')  :
        # def already_followed(self):
        #     if self.unique_together:
        #         return "Utilisateur déjà suivi"
