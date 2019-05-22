# users/forms.py
from django.db import models
from django.forms import ModelForm
from django import forms as formsimport
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
        cleaned_data = super(eventCreationForm, self).clean()
        start_time  = cleaned_data.get('start_time')
        end_time    = cleaned_data.get('end_time')

        if start_time and end_time:
            if start_time > end_time:
                self.add_error('start_time', "The end time of your event must be after the start time!")
        
        return cleaned_data

class eventChangeForm(ModelForm):
    class Meta:
        model  = event
        fields = ('name', 'description', 'is_active', 'start_time', 'end_time', 'pin_checkin', 'pin_checkout')

    def clean(self):
        cleaned_data = super(eventChangeForm, self).clean()
        start_time  = cleaned_data.get('start_time')
        end_time    = cleaned_data.get('end_time')

        if start_time and end_time:
            if start_time > end_time:
                self.add_error('start_time', "The end time of your event must be after the start time!")
        
        return cleaned_data
        
#----------------------------------------------------------------------------------------------------------------------------------------------------