from django.db import models
from users.models  import CustomUser
import os

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
	email          = models.EmailField(max_length = 200)
	address        = models.CharField(max_length = 500)
	#picture        = models.ImageField(upload_to=get_image_path, blank=True, null=True)

	#Donations, Discounts Metrics
	donation_tokens = models.FloatField() 
	discount_tokens = models.FloatField()
	qr_code         = models.ImageField(upload_to= get_image_path, blank=True, null=True)

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
	donation_or_discount = models.BooleanField(default = True) #True: Donation, False: Discount
	token_cost           = models.FloatField(default = 0.0)
	parent_business      = models.ForeignKey(business, on_delete=models.CASCADE)

	donation_val         = models.FloatField(default = 0.0) #only relevant if donation_or_discount is true (coupon is donation)
	
	
	def __str__(self):
		return self.name
#----------------------------------------------------------------------------------------------------------------------------------------------------


#transcation_stub class - keeps track of transcations between businesses and volunteers
#----------------------------------------------------------------------------------------------------------------------------------------------------
class transaction_stub(models.Model):
	donation_or_discount = models.BooleanField(default = True) #True: Donation, False: Discount
	tokens_transferred   = models.FloatField(default = 0.0) #tokens given to business for donation/discount
	parent_business      = models.ForeignKey(business, on_delete=models.CASCADE)
	parent_volunteer     = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#----------------------------------------------------------------------------------------------------------------------------------------------------	