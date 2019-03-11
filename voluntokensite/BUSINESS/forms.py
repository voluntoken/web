# users/forms.py
from django.db import models
from django.forms import ModelForm
from .models import coupon



EXCHANGE_RATE            = 5.0 #1 Token = 5 USD

#coupon Discount
#----------------------------------------------------------------------------------------------------------------------------------------------------
class couponDiscountCreationForm(ModelForm):
    def __init__(self,*args,**kwargs):
        self.parent_business_name = kwargs.pop('parent_business_name')
        super(couponDiscountCreationForm,self).__init__(*args,**kwargs)
        
    class Meta:
        model  = coupon
        fields = ('name', 'description', 'token_cost')
        
    def clean(self):
        self.instance.parent_business = self.parent_business_name
        self.is_donation              = False
        self.donation_val             = 0.0
        return super(couponDiscountCreationForm, self).clean()

class couponDiscountChangeForm(ModelForm):
    class Meta:
        model  = coupon
        fields = ('name', 'description', 'token_cost')
#----------------------------------------------------------------------------------------------------------------------------------------------------

#coupon Donation
#----------------------------------------------------------------------------------------------------------------------------------------------------
class couponDonationCreationForm(ModelForm):
    def __init__(self,*args,**kwargs):
        self.parent_business_name = kwargs.pop('parent_business_name')
        super(couponDonationCreationForm,self).__init__(*args,**kwargs)
    
    class Meta:
        model  = coupon
        fields = ('name', 'description', 'donation_val')
        
    def clean(self):
        self.instance.parent_business = self.parent_business_name
        self.is_donation              = True
        self.token_cost               = 1.0/EXCHANGE_RATE*self.donation_val
        return super(couponDonationCreationForm, self).clean()

class couponDonationChangeForm(ModelForm):
    class Meta:
        model  = coupon
        fields = ('name', 'description', 'donation_val')

    def clean(self):
        self.token_cost               = 1.0/EXCHANGE_RATE*self.donation_val
        return super(couponDonationChangeForm, self).clean()

#----------------------------------------------------------------------------------------------------------------------------------------------------
