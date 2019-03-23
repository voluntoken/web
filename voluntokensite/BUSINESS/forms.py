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


        cleaned_data  = super(couponDiscountCreationForm, self).clean()
        token_cost    = cleaned_data['token_cost']
        item_cost     = cleaned_data['item_cost']

        if token_cost:
            if token_cost < 0:
                self.add_error('token_cost', "Please enter a non-negative token cost for this coupon!")

        if item_cost:
            if item_cost < 0:
                self.add_error('item_cost', "Please enter a non-negative item revenue estimate for this couoon!")

        return cleaned_data



class couponDiscountChangeForm(ModelForm):
    class Meta:
        model  = coupon
        fields = ('name', 'description', 'token_cost', 'item_cost', 'is_active')


    def clean(self):
        cleaned_data  = super(couponDiscountChangeForm, self).clean()
        token_cost    = cleaned_data['token_cost']
        item_cost     = cleaned_data['item_cost']

        if token_cost:
            if token_cost < 0:
                self.add_error('token_cost', "Please enter a non-negative token cost for this coupon!")

        if item_cost:
            if item_cost < 0:
                self.add_error('item_cost', "Please enter a non-negative item revenue estimate for this couoon!")

        return cleaned_data


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

        cleaned_data    = super(couponDonationCreationForm, self).clean()
        donation_val    = cleaned_data['donation_val']
        item_cost       = cleaned_data['item_cost']

        if donation_val:
            if donation_val < 0:
                self.add_error('donation_val', "Please enter a non-negative donation value for this coupon!")

        if item_cost:
            if item_cost < 0:
                self.add_error('item_cost', "Please enter a non-negative item revenue estimate for this couoon!")

        return cleaned_data

class couponDonationChangeForm(ModelForm):
    class Meta:
        model  = coupon
        fields = ('name', 'description', 'donation_val', 'item_cost', 'is_active')

    def clean(self):
        self.instance.token_cost               = 1.0/EXCHANGE_USD_TOKEN*self.cleaned_data.get('donation_val')
        return super(couponDonationChangeForm, self).clean()


    def clean(self):
        self.instance.token_cost               = 1.0/EXCHANGE_USD_TOKEN*self.cleaned_data.get('donation_val')

        cleaned_data    = super(couponDonationChangeForm, self).clean()
        donation_val    = cleaned_data['donation_val']
        item_cost       = cleaned_data['item_cost']

        if donation_val:
            if donation_val < 0:
                self.add_error('donation_val', "Please enter a non-negative donation value for this coupon!")

        if item_cost:
            if item_cost < 0:
                self.add_error('item_cost', "Please enter a non-negative item revenue estimate for this couoon!")

        return cleaned_data
#----------------------------------------------------------------------------------------------------------------------------------------------------
