from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from django.contrib.auth.models import User
from talenthub.models import Profile, Offer, Category, Meeting


# Define a new User admin
class CategoryAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name']}),
    ]


admin.site.register(Offer)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Meeting)
