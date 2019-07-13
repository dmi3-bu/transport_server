from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Ticket

# admin.site.register(User, UserAdmin)
admin.site.register(Ticket)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fields = ('first_name', 'last_name', 'groups')
