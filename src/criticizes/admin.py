from django.contrib import admin

# Register your models here.
from criticizes.models import Ticket
from criticizes.models import Review
from criticizes.models import UserFollows



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