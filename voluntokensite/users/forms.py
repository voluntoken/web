from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import VolunteerUser

class VolunteerUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = VolunteerUser
        fields = ('username', 'email')

class VolunteerUserChangeForm(UserChangeForm):

    class Meta:
        model = VolunteerUser
        fields = ('username', 'email')