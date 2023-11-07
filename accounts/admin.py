from django.contrib import admin

from accounts.models import User


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser']
    list_display_links = ['id', 'email']
    list_filter = ['is_active', 'is_staff', 'is_superuser']
    search_fields = ['email', 'first_name', 'last_name']
