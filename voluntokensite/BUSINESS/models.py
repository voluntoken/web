from django.db import models
from users.models  import CustomUser
import os


def get_image_path(instance, filename):
	return os.path.join('photos', str(instance.id), filename)


# class businesses_manager(models.businesses):


class businesses(models.Model):
	name           = models.CharField(max_length = 50)
	description    = models.CharField(max_length = 2500)
	email          = models.EmailField(max_length = 200)
	address        = models.CharField(max_length = 500)
	#picture        = models.ImageField(upload_to=get_image_path, blank=True, null=True)

	Donation_tokens = models.FloatField()
	Discount_tokens = models.FloatField()
	QR_code        = models.ImageField(upload_to= get_image_path, blank=True, null=True)

	def __str__(self):
		return self.name


# class coupon_manager(models.coupon):
# 	def get_business_coupons(self, business_name):
# 			return self.objects.filter(parent_business.name = business_name)
	

class coupon(models.Model):
	name                 = models.CharField(max_length = 50)
	description          = models.CharField(max_length = 100)
	Donation_or_Discount = models.BooleanField(default = True) #True: Donation, False: Discount
	token_cost           = models.FloatField(default = 0.0)
	donation_val         = models.FloatField(default = 0.0)
	parent_business      = models.ForeignKey(businesses, on_delete=models.CASCADE)
	def __str__(self):
		return self.name

class transaction_stub(models.Model):
	Donation_or_Discount = models.BooleanField(default = True) #True: Donation, False: Discount
	tokens_transferred   = models.FloatField(default = 0.0)
	parent_business      = models.ForeignKey(businesses, on_delete=models.CASCADE)
	parent_volunteer     = models.ForeignKey(CustomUser, on_delete=models.CASCADE)