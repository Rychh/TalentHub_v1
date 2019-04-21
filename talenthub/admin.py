from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from django.contrib.auth.models import User
from talenthub.models import *

admin.site.register(Offer)
admin.site.register(Category)
admin.site.register(Meeting)
admin.site.register(Profile)
admin.site.register(Argument)
admin.site.register(Review)
