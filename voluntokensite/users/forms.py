# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


#Admin
#----------------------------------------------------------------------------------------------------------------------------------------------------
class CustomUserCreationForm_Admin(UserCreationForm):
    password1 = forms.CharField(label=("Password"),
        widget=forms.PasswordInput(attrs={'class': "form-control form-control-user"}))
    password2 = forms.CharField(label=("Password confirmation"),
        widget=forms.PasswordInput(attrs={'class': "form-control form-control-user"}),
        help_text=("Enter the same password as above, for verification."))

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email','user_type', 'volunteer_role','volunteer_token',  'parent_ngo',  'parent_business', 'is_public', 'is_active', 'volunteer_hour')

        widgets = {}
        for field in fields:
            widgets[field] = forms.TextInput(attrs={'class': "form-control form-control-user"})

class CustomUserChangeForm_Admin(UserChangeForm):

    class Meta(UserChangeForm):
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email','user_type', 'volunteer_role','volunteer_token', 'parent_ngo',  'parent_business', 'is_public', 'is_active', 'volunteer_hour')

        widgets = {}
        for field in fields:
            widgets[field] = forms.TextInput(attrs={'class': "form-control form-control-user"})

#----------------------------------------------------------------------------------------------------------------------------------------------------

#Volunteer
#----------------------------------------------------------------------------------------------------------------------------------------------------
class CustomUserCreationForm_Volunteer(UserCreationForm):
    password1 = forms.CharField(label=("Password"),
        widget=forms.PasswordInput(attrs={'class': "form-control form-control-user"}))
    password2 = forms.CharField(label=("Password confirmation"),
        widget=forms.PasswordInput(attrs={'class': "form-control form-control-user"}),
        help_text=("Enter the same password as above, for verification."))

    volunteer_donate = 'DO'
    volunteer_discount = 'DI'
    volunteer_choices = {
        (volunteer_donate,'Donator'),
        (volunteer_discount,'Discounter')
    }

    volunteer_role = forms.CharField(help_text='Choose whether you would like to donate your tokens or recieve discounts for them', widget=forms.Select(attrs={"class": "btn btn-primary btn-user btn-block"}, choices=volunteer_choices))

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email','volunteer_role')

        widgets = {}
        for field in fields:
            widgets[field] = forms.TextInput(attrs={'class': "form-control form-control-user"})

    def clean(self):
        self.instance.volunteer_token = 0
        self.instance.user_type = 'VO'
        return super(CustomUserCreationForm_Volunteer, self).clean()

class CustomUserChangeForm_Volunteer(UserChangeForm):

    password=None
    volunteer_donate = 'DO'
    volunteer_discount = 'DI'
    volunteer_choices = {
        (volunteer_donate,'Donator'),
        (volunteer_discount,'Discounter')
    }

    volunteer_role = forms.CharField(help_text='Choose whether you would like to donate your tokens or recieve discounts for them', widget=forms.Select(attrs={"class": "btn btn-primary btn-user btn-block"}, choices=volunteer_choices))

    class Meta(UserChangeForm):
        model = CustomUser
        fields = ('first_name', 'last_name', 'email','volunteer_role')

        widgets = {}
        for field in fields:
            widgets[field] = forms.TextInput(attrs={'class': "form-control form-control-user"})

#----------------------------------------------------------------------------------------------------------------------------------------------------


#NGO
#----------------------------------------------------------------------------------------------------------------------------------------------------
class CustomUserCreationForm_NGO(UserCreationForm):
    password1 = forms.CharField(label=("Password"),
        widget=forms.PasswordInput(attrs={'class': "form-control form-control-user"}))
    password2 = forms.CharField(label=("Password confirmation"),
        widget=forms.PasswordInput(attrs={'class': "form-control form-control-user"}),
        help_text=("Enter the same password as above, for verification."))

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'parent_ngo')

        widgets = {}
        for field in fields:
            widgets[field] = forms.TextInput(attrs={'class': "form-control form-control-user"})

    def clean(self):
        self.instance.user_type = 'NG'
        return super(CustomUserCreationForm_NGO, self).clean()

class CustomUserChangeForm_NGO(UserChangeForm):

    password=None
    class Meta(UserChangeForm):
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'parent_ngo')

        widgets = {}
        for field in fields:
            widgets[field] = forms.TextInput(attrs={'class': "form-control form-control-user"})
#----------------------------------------------------------------------------------------------------------------------------------------------------

#Business
#----------------------------------------------------------------------------------------------------------------------------------------------------
class CustomUserCreationForm_Business(UserCreationForm):
    password1 = forms.CharField(label=("Password"),
        widget=forms.PasswordInput(attrs={'class': "form-control form-control-user"}))
    password2 = forms.CharField(label=("Password confirmation"),
        widget=forms.PasswordInput(attrs={'class': "form-control form-control-user"}),
        help_text=("Enter the same password as above, for verification."))

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'parent_business')

        widgets = {}
        for field in fields:
            widgets[field] = forms.TextInput(attrs={'class': "form-control form-control-user"})

    def clean(self):
        self.instance.user_type = 'BU'
        return super(CustomUserCreationForm_Business, self).clean()

class CustomUserChangeForm_Business(UserChangeForm):

    password=None
    class Meta(UserChangeForm):
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'parent_business')

        widgets = {}
        for field in fields:
            widgets[field] = forms.TextInput(attrs={'class': "form-control form-control-user"})
#----------------------------------------------------------------------------------------------------------------------------------------------------
