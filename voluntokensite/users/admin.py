from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import VolunteerUserCreationForm, VolunteerUserChangeForm
from .models import VolunteerUser

class VolunteerUserAdmin(UserAdmin):
    add_form = VolunteerUserCreationForm
    form = VolunteerUserChangeForm
    model = VolunteerUser
    list_display = ['email', 'username',]

admin.site.register(VolunteerUser, VolunteerUserAdmin)