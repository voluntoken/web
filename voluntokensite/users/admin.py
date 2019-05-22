### users/admin.py
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm_Admin, CustomUserChangeForm_Admin
from .models import CustomUser, total_hours_stub

admin.site.register(total_hours_stub)
#Custom User Admin Class to Display and Have Edit access to new Custom Fields
#----------------------------------------------------------------------------------------------------------------------------------------------------
class CustomUserAdmin(UserAdmin):
    # add_form = CustomUserCreationForm_Admin
    # form = CustomUserChangeForm_Admin
    model = CustomUser
    list_display = ['username', 'first_name', 'last_name', 'email','user_type', 'volunteer_role','volunteer_token', 'volunteer_hour', 'volunteer_hour_fund', 'parent_ngo', 'parent_business', 'is_active']
    fieldsets = (
            (None, {'fields': ('username', 'first_name', 'last_name', 'email','user_type', 'volunteer_role','volunteer_token', 'volunteer_hour', 'volunteer_hour_fund', 'parent_ngo', 'parent_business', 'is_active')}),
    )


admin.site.register(CustomUser, CustomUserAdmin)
#----------------------------------------------------------------------------------------------------------------------------------------------------
