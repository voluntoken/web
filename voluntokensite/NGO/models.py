from django.db import models
from users.models import CustomUser
import os


def get_image_path(instance, filename):
	return os.path.join('photos', str(instance.id), filename)

#org class - 
#----------------------------------------------------------------------------------------------------------------------------------------------------
class org(models.Model):
	#Profile Info
	name        = models.CharField(max_length = 50)
	description = models.CharField(max_length = 2500)
	email       = models.EmailField(max_length = 200)
	address     = models.CharField(max_length = 500)
	#picture     = models.ImageField(upload_to=get_image_path, blank=True, null=True)

	def __str__(self):
		return self.name
#----------------------------------------------------------------------------------------------------------------------------------------------------

#event class
#----------------------------------------------------------------------------------------------------------------------------------------------------
class event(models.Model):
	#Profile Info
	name        = models.CharField(max_length = 200)
	description = models.CharField(max_length = 2500)
	#picture     = models.ImageField(upload_to=get_image_path, blank=True, null=True)
	parent_ngo  = models.ForeignKey(org, on_delete=models.CASCADE)
	qr_code     = models.ImageField(upload_to=get_image_path, blank=True, null=True)
	is_active   = models.BooleanField(default=True)

	#Timing
	start_time  = models.DateTimeField()
	end_time    = models.DateTimeField()


	# #NEEDS TESTING -------------------------------------------------
	# #Check ifstop_time - start_time is positive
	# if (end_time - start_time).hours <= 0:
	# 	raise forms.ValidationError("The end time of your event must be after the start time!")

	# #---------------------------------------------------------------

	def __str__(self):
		return self.name
#----------------------------------------------------------------------------------------------------------------------------------------------------

#checks_stub class - check in, check out stub
#----------------------------------------------------------------------------------------------------------------------------------------------------
class checks_stub(models.Model):
	is_check_in      = models.BooleanField(default = True) #True: Check IN, False: Check OUT
	time             = models.DateTimeField()
	parent_event     = models.ForeignKey(event, on_delete=models.CASCADE)
	parent_volunteer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

	# def __str__(self):
	# 	return __str__(self.time)
#----------------------------------------------------------------------------------------------------------------------------------------------------

#event registrsation is different from checking in or out
#----------------------------------------------------------------------------------------------------------------------------------------------------
class event_registration_stub(models.Model):
	is_active        = models.BooleanField(default=True)
	parent_event     = models.ForeignKey(event, on_delete=models.CASCADE)
	parent_volunteer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#----------------------------------------------------------------------------------------------------------------------------------------------------
	# def __str__(self):
	# 	return __str__(self.parent_event)