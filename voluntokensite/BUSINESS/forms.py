# users/forms.py
from django.db import models
from django.forms import ModelForm
from .models import coupon, EXCHANGE_USD_TOKEN


#coupon Discount
#----------------------------------------------------------------------------------------------------------------------------------------------------
class couponDiscountCreationForm(ModelForm):
    def __init__(self,*args,**kwargs):
        self.parent_business_name = kwargs.pop('parent_business_name')
        super(couponDiscountCreationForm,self).__init__(*args,**kwargs)
        
    class Meta:
        model  = coupon
        fields = ('name', 'description', 'token_cost', 'item_cost', 'is_active')
        
    def clean(self):
        self.instance.parent_business          = self.parent_business_name
        self.instance.is_donation              = False
        return super(couponDiscountCreationForm, self).clean()

class couponDiscountChangeForm(ModelForm):
    class Meta:
        model  = coupon
        fields = ('name', 'description', 'token_cost', 'item_cost', 'is_active')
#----------------------------------------------------------------------------------------------------------------------------------------------------

#coupon Donation
#----------------------------------------------------------------------------------------------------------------------------------------------------
class couponDonationCreationForm(ModelForm):
    def __init__(self,*args,**kwargs):
        self.parent_business_name = kwargs.pop('parent_business_name')
        super(couponDonationCreationForm,self).__init__(*args,**kwargs)
    
    class Meta:
        model  = coupon
        fields = ('name', 'description', 'donation_val', 'item_cost', 'is_active')
        
    def clean(self):
        self.instance.parent_business          = self.parent_business_name
        self.instance.is_donation              = True
        self.instance.token_cost               = 1.0/EXCHANGE_USD_TOKEN*self.cleaned_data.get('donation_val')
        return super(couponDonationCreationForm, self).clean()

class couponDonationChangeForm(ModelForm):
    class Meta:
        model  = coupon
        fields = ('name', 'description', 'donation_val', 'item_cost', 'is_active')

    def clean(self):
        self.instance.token_cost               = 1.0/EXCHANGE_USD_TOKEN*self.cleaned_data.get('donation_val')
        return super(couponDonationChangeForm, self).clean()

#----------------------------------------------------------------------------------------------------------------------------------------------------
