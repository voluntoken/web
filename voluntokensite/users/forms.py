# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


#admin

class CustomUserCreationForm_Admin(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email','user_type', 'volunteer_role','volunteer_token',  'parent_ngo',  'parent_business')

class CustomUserChangeForm_Admin(UserChangeForm):

    class Meta(UserChangeForm):
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email','user_type', 'volunteer_role','volunteer_token', 'parent_ngo',  'parent_business')
        

#Volunteer
class CustomUserCreationForm_Volunteer(UserCreationForm):

    volunteer_donate = 'DO'
    volunteer_discount = 'DI'
    volunteer_choices = {
        (volunteer_donate,'Donator'),
        (volunteer_discount,'Discounter')
    }
    
    volunteer_role = forms.CharField(help_text='Choose whether you would like to donate your tokens or recieve discounts for them', widget=forms.Select(choices=volunteer_choices ))
    
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email','volunteer_role')
        
    def clean(self):
        self.instance.volunteer_token = 0
        self.instance.user_type = 'VO'
        return super(CustomUserCreationForm_Volunteer, self).clean()
        
class CustomUserChangeForm_Volunteer(UserChangeForm):

    class Meta(UserChangeForm):
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email','volunteer_role')
        
        
#NGO
class CustomUserCreationForm_NGO(UserCreationForm):
    
    
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email')
        
    def clean(self):
        self.instance.user_type = 'NG'
        return super(CustomUserCreationForm_NGO, self).clean()

class CustomUserChangeForm_NGO(UserChangeForm):

    class Meta(UserChangeForm):
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email')
    
#Business    
class CustomUserCreationForm_Business(UserCreationForm):
        
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email')
        
    def clean(self):
        self.instance.user_type = 'BU'
        return super(CustomUserCreationForm_Business, self).clean()

class CustomUserChangeForm_Businesss(UserChangeForm):

    class Meta(UserChangeForm):
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email')