### users/admin.py
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm_Admin, CustomUserChangeForm_Admin
from .models import CustomUser

#Custom User Admin Class to Display and Have Edit access to new Custom Fields
#----------------------------------------------------------------------------------------------------------------------------------------------------
class CustomUserAdmin(UserAdmin):
    # add_form = CustomUserCreationForm_Admin
    # form = CustomUserChangeForm_Admin
    model = CustomUser
    list_display = ['username', 'first_name', 'last_name', 'email','user_type', 'volunteer_role','volunteer_token', 'parent_ngo', 'parent_business']
    fieldsets = (
            (None, {'fields': ('username', 'first_name', 'last_name', 'email','user_type', 'volunteer_role','volunteer_token', 'parent_ngo', 'parent_business')}),
    )


admin.site.register(CustomUser, CustomUserAdmin)
#----------------------------------------------------------------------------------------------------------------------------------------------------
