from django.contrib import admin

# Register your models here.
from criticizesApp.models import Ticket
from criticizesApp.models import Review
from criticizesApp.models import UserFollows



# admin.site.register(Ticket)
# admin.site.register(Review)
# admin.site.register(UserFollows)

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    pass

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    pass

@admin.register(UserFollows)
class UserFollowsAdmin(admin.ModelAdmin):
    pass