# users/forms.py
from django.db import models
from django.forms import ModelForm
from .models import org, event, checks_stub, event_registration_stub

#event
#----------------------------------------------------------------------------------------------------------------------------------------------------
class eventCreationForm(ModelForm):
    def __init__(self,*args,**kwargs):
        self.parent_ngo_name = kwargs.pop('parent_ngo_name')
        super(eventCreationForm,self).__init__(*args,**kwargs)
        
    class Meta:
        model  = event
        fields = ('name', 'description', 'is_active', 'start_time', 'end_time','pin_checkin', 'pin_checkout')
        
    def clean(self):
        self.instance.parent_ngo = self.parent_ngo_name
        return super(eventCreationForm, self).clean()

class eventChangeForm(ModelForm):
    class Meta:
        model  = event
        fields = ('name', 'description', 'is_active', 'start_time', 'end_time', 'pin_checkin', 'pin_checkout')
        
#----------------------------------------------------------------------------------------------------------------------------------------------------









# #checks_stub
# #----------------------------------------------------------------------------------------------------------------------------------------------------
# class checks_stubCreationForm(check_in_or_out, parent_event_name, parent_volunteer_name, ModelForm):

#     class Meta:
#         model  = checks_stub
        
#     def clean(self):
#         self.instance.is_check_in      = check_in_or_out
#         self.instance.time             = models.DateTimeField(auto_now=True)
#         self.instance.parent_event     = parent_event_name
#         self.instance.parent_volunteer = parent_volunteer_name
#         return super(checks_stubCreationForm, self).clean()
# #----------------------------------------------------------------------------------------------------------------------------------------------------

# #event_registration_stub
# #----------------------------------------------------------------------------------------------------------------------------------------------------
# class event_registration_stubCreationForm(parent_event_name, parent_volunteer_name, ModelForm):
#     class Meta:
#         model  = event_registration_stub
#         fields = ('is_active')
        
#     def clean(self):
#         self.instance.parent_event     = parent_event_name
#         self.instance.parent_volunteer = parent_volunteer_name
#         return super(event_registration_stubCreationForm, self).clean()

# class event_registration_stubChangeForm(ModelForm):
#     class Meta:
#         model = event_registration_stub
#         fields = ('is_active')
# #----------------------------------------------------------------------------------------------------------------------------------------------------