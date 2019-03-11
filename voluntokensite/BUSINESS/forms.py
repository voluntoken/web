# users/forms.py
from django.db import models
from django.forms import ModelForm
from .models import coupon



EXCHANGE_RATE            = 5.0 #1 Token = 5 USD

#coupon Discount
#----------------------------------------------------------------------------------------------------------------------------------------------------
class couponDiscountCreationForm(parent_business_name, ModelForm):
    class Meta:
        model  = coupon
        fields = ('name', 'description', 'token_cost')
        
    def clean(self):
        self.instance.parent_business = parent_business_name
        self.is_donation              = False
        self.donation_val             = 0.0
        return super(eventCreationForm, self).clean()

class couponDiscountChangeForm(parent_business_name, ModelForm):
    class Meta:
        model  = coupon
        fields = ('name', 'description', 'token_cost')
#----------------------------------------------------------------------------------------------------------------------------------------------------

#coupon Donation
#----------------------------------------------------------------------------------------------------------------------------------------------------
class couponDonationCreationForm(parent_business_name, ModelForm):
    class Meta:
        model  = coupon
        fields = ('name', 'description', 'donation_val')
        
    def clean(self):
        self.instance.parent_business = parent_business_name
        self.is_donation              = True
        self.token_cost               = 1.0/EXCHANGE_RATE*self.donation_val
        return super(eventCreationForm, self).clean()

class couponDonationChangeForm(parent_business_name, ModelForm):
    class Meta:
        model  = coupon
        fields = ('name', 'description', 'donation_val')

    def clean(self):
        self.token_cost               = 1.0/EXCHANGE_RATE*self.donation_val
        return super(eventCreationForm, self).clean()

#----------------------------------------------------------------------------------------------------------------------------------------------------
