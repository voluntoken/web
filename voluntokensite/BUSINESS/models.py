from django.db import models
from users.models  import CustomUser
from NGO.models  import org
from random import randint
import os

#exchange rate
EXCHANGE_TOKEN_HOUR = 1.0 #units = token/hour

#image stuff
def get_image_path(instance, filename):
	return os.path.join('photos', str(instance.id), filename)


#business class - CustomUser of Business user_type has a ForeignKey referring to a Business 
#----------------------------------------------------------------------------------------------------------------------------------------------------
# class businesses_manager(models.businesses):

class business(models.Model):
	#Profile Information
	name           = models.CharField(max_length = 50)
	description    = models.CharField(max_length = 2500)
	website        = models.URLField(null=True)
	email          = models.EmailField(max_length = 200)
	address        = models.CharField(max_length = 500)
	is_active      = models.BooleanField(default=True)
	#picture        = models.ImageField(upload_to=get_image_path, blank=True, null=True)

	#Donations, Discounts Metrics
	total_hours     = models.FloatField(default=0.0) 
	donation_tokens = models.FloatField(default=0.0) 
	discount_tokens = models.FloatField(default=0.0)
	qr_code         = models.ImageField(upload_to= get_image_path, blank=True, null=True)
	pin             = models.IntegerField(default=randint(1000,9999))
	def __str__(self):
		return self.name
#----------------------------------------------------------------------------------------------------------------------------------------------------




#coupon class - coupons that are created by business 
#----------------------------------------------------------------------------------------------------------------------------------------------------
# class coupon_manager(models.coupon):
# 	def get_business_coupons(self, business_name):
# 			return self.objects.filter(parent_business.name = business_name)
	

#Coupons
class coupon(models.Model):
	#Profile 
	name                 = models.CharField(max_length = 50)
	description          = models.CharField(max_length = 100)
	is_donation          = models.BooleanField(default = True) #True: Donation, False: Discount
	token_cost           = models.FloatField(default = 0.0)
	parent_business      = models.ForeignKey(business, on_delete=models.CASCADE)
	is_active            = models.BooleanField(default=True)
	donation_val         = models.FloatField(default = 0.0) #only relevant if donation_or_discount is true (coupon is donation)
	item_cost            = models.FloatField(default = 0.0)
	
	
	def __str__(self):
		return self.name
#----------------------------------------------------------------------------------------------------------------------------------------------------


#transcation_stub class - keeps track of transcations between businesses and volunteers
#----------------------------------------------------------------------------------------------------------------------------------------------------
class transaction_stub(models.Model):
	is_donation          = models.BooleanField(default = True) #True: Donation, False: Discount
	tokens_transferred   = models.FloatField(default = 0.0) #tokens given to business for donation/discount
	item_cost            = models.FloatField(default = 0.0) #estimated item cost 
	parent_business      = models.ForeignKey(business, on_delete=models.CASCADE)
	parent_volunteer     = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#----------------------------------------------------------------------------------------------------------------------------------------------------	

#Keeps track of how many hours of volunteering at an NGO a business has supported and how much they have pledged to donate
#----------------------------------------------------------------------------------------------------------------------------------------------------
class total_support_stub(models.Model):
    parent_business       = models.ForeignKey(business, on_delete=models.CASCADE)
    parent_ngo            = models.ForeignKey(org, on_delete=models.CASCADE)
    total_hours           = models.FloatField(default=0.0)
    total_discount_tokens = models.FloatField(default=0.0)
    total_donation_tokens = models.FloatField(default=0.0)

    #number of transactions through which businesses have supported this NGO
    total_transactions    = models.IntegerField(default=0.0)
#----------------------------------------------------------------------------------------------------------------------------------------------------

#Keeps track of how many hours of volunteering, discount tokens, and donation tokens a user has spent at a business to support a specific NGO
#----------------------------------------------------------------------------------------------------------------------------------------------------
class user_support_stub(models.Model):
    parent_business       = models.ForeignKey(business, on_delete=models.CASCADE)
    parent_ngo            = models.ForeignKey(org, on_delete=models.CASCADE)
    parent_volunteer      = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    total_hours           = models.FloatField(default=0.0)
    total_discount_tokens = models.FloatField(default=0.0)
    total_donation_tokens = models.FloatField(default=0.0)
#----------------------------------------------------------------------------------------------------------------------------------------------------